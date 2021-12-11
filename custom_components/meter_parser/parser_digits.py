""" Digits Parser that uses online OCR tool """

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

import logging
import os
import time
import requests
import cv2
import urllib.parse
import numpy as np
import re

_LOGGER = logging.getLogger(__name__)
URL_API = "https://api.ocr.space/parse/image"


def parse_digits(
    image,
    digits_count: int,
    ocr_key: str,
    entity_id: str,
    debug_path: str = None,
):
    """Displaying digits and OCR"""
    debugfile = time.strftime(entity_id + "-%Y-%m-%d_%H-%M-%S")
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # remove red colors
    sensitivity = 30
    lower_red_0 = np.array([0, 100, 100])
    upper_red_0 = np.array([sensitivity, 255, 255])
    lower_red_1 = np.array([180 - sensitivity, 100, 100])
    upper_red_1 = np.array([180, 255, 255])

    mask_0 = cv2.inRange(hsv, lower_red_0, upper_red_0)
    mask_1 = cv2.inRange(hsv, lower_red_1, upper_red_1)

    mask = cv2.bitwise_or(mask_0, mask_1)
    # Change image to white where we found red
    frame = image.copy()
    frame[np.where(mask)] = (255, 255, 255)

    if debug_path is not None:
        cv2.imwrite(os.path.join(debug_path, "%s-in.jpg" % debugfile), frame)

    payload = {
        "apikey": ocr_key,
        "language": "eng",
        "scale": "true",
        "OCREngine": "2"
    }

    _LOGGER.debug("%s: OCR image: %s" % (entity_id, URL_API))
    imencoded = cv2.imencode(".jpg", frame)[1]
    response = requests.post(
        URL_API,
        data=payload,
        files={"file.jpg": imencoded.tobytes()},
        timeout=9,
    )

    if response.status_code == 200:
        result = response.json()
        if "ParsedResults" in result:
            text = ""
            for reg in result["ParsedResults"]:
                if "ParsedText" in reg:
                    text = text + reg["ParsedText"]
                text = text + "\n"
            return parse_result(
                text,
                digits_count,
                entity_id,
            )
        if "ErrorMessage" in result:
            raise Exception(result["ErrorMessage"])

    raise Exception(response.text)


def parse_result(ocr: str, digits: int, entity_id: str):
    """Parse possible results"""
    if ocr is not None and ocr != "":
        array = ocr.strip().split("\n")
        for x_str in array:
            x_str = x_str.replace(" ", "").replace(".", "").replace(",", "").replace("|", "").replace("/", "").replace("\\", "").replace("o", "0").replace("O", "0")  # replace common ocr mistakes
            x_str = re.search("[0-9]{%s}" % digits, x_str)
            if x_str is not None and x_str.group(0) is not None:
                _LOGGER.debug("%s: Final reading: %s" % (entity_id, x_str.group(0)))
                return x_str.group(0)
    raise Exception("Unable to OCR image or no text found.")
