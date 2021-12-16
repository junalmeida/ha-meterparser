""" Digits Parser with trained tensorflow """

#    Copyright 2021 Marcos Junior
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import os
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
from keras_preprocessing.image.utils import _PIL_INTERPOLATION_METHODS
from numpy import argmax
import cv2
import time
import logging
from PIL import Image as pil_image
_LOGGER = logging.getLogger(__name__)


# load model
model_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "tf-models", "digits.h5")
_LOGGER.debug("Loading pre-trained model...")
model = load_model(model_path)
_LOGGER.debug("Model loaded")


def load_img(np_arr, color_mode='rgb', target_size=None,
             interpolation='nearest'):
    """Loads an image into PIL format.

    # Arguments
        path: Path to image file.
        grayscale: DEPRECATED use `color_mode="grayscale"`.
        color_mode: The desired image format. One of "grayscale", "rgb", "rgba".
            "grayscale" supports 8-bit images and 32-bit signed integer images.
            Default: "rgb".
        target_size: Either `None` (default to original size)
            or tuple of ints `(img_height, img_width)`.
        interpolation: Interpolation method used to resample the image if the
            target size is different from that of the loaded image.
            Supported methods are "nearest", "bilinear", and "bicubic".
            If PIL version 1.1.3 or newer is installed, "lanczos" is also
            supported. If PIL version 3.4.0 or newer is installed, "box" and
            "hamming" are also supported.
            Default: "nearest".

    # Returns
        A PIL Image instance.

    # Raises
        ImportError: if PIL is not available.
        ValueError: if interpolation method is not supported.
    """
    if pil_image is None:
        raise ImportError('Could not import PIL.Image. '
                          'The use of `load_img` requires PIL.')

    img = pil_image.fromarray(np_arr)
    if color_mode == 'grayscale':
        # if image is not already an 8-bit, 16-bit or 32-bit grayscale image
        # convert it to an 8-bit grayscale image.
        if img.mode not in ('L', 'I;16', 'I'):
            img = img.convert('L')
    elif color_mode == 'rgba':
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
    elif color_mode == 'rgb':
        if img.mode != 'RGB':
            img = img.convert('RGB')
    else:
        raise ValueError('color_mode must be "grayscale", "rgb", or "rgba"')
    if target_size is not None:
        width_height_tuple = (target_size[1], target_size[0])
        if img.size != width_height_tuple:
            if interpolation not in _PIL_INTERPOLATION_METHODS:
                raise ValueError(
                    'Invalid interpolation method {} specified. Supported '
                    'methods are {}'.format(
                        interpolation,
                        ", ".join(_PIL_INTERPOLATION_METHODS.keys())))
            resample = _PIL_INTERPOLATION_METHODS[interpolation]
            img = img.resize(width_height_tuple, resample)
    return img


def parse_digits(
    digits: list(),
    entity_id: str,
    debug_path: str = None,
):
    """Displaying digits and OCR with tensor_flow"""
    debugfile = time.strftime(entity_id + "-%Y-%m-%d_%H-%M-%S")
    result = ""
    for i, image_np in enumerate(digits):

        img = load_img(image_np, color_mode="grayscale", target_size=(28, 28))
        # convert to array
        img = img_to_array(img)
        if debug_path is not None:
            cv2.imwrite(os.path.join(debug_path, "%s-%s.png" % (debugfile, i)), img)

        # reshape into a single sample with 1 channel
        img = img.reshape(1, 28, 28, 1)

        # prepare pixel data
        img = img.astype('float32')
        img = img / 255.0

        predict_value = model.predict(img)
        digit = argmax(predict_value)
        result = result + str(digit)
    return result
