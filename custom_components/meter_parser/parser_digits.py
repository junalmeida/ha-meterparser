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

_LOGGER = logging.getLogger(__name__)
MS_API = "/vision/v3.2/ocr"


def parse_digits(
    frame,
    digits_count: int,
    ocr_key: str,
    ocr_url: str,
    entity_id: str,
    debug_path: str = None,
):
    """Displaying digits and OCR"""
    # remove red colors
    lower = (200, 0, 0)  # lower bound for each channel
    upper = (255, 0, 0)  # upper bound for each channel
    mask = cv2.inRange(frame, lower, upper)
    frame[mask != 0] = [255, 255, 255]

    # Adjust the exposure
    alpha = float(2.5)
    blur = int(3)
    threshold = 37
    adjustment = 11
    frame = cv2.multiply(frame, np.array([alpha]))
    # Convert to grayscale
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Blur to reduce noise
    frame = cv2.GaussianBlur(frame, (blur, blur), 0)
    # Threshold the image
    frame = cv2.adaptiveThreshold(
        frame,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        threshold,
        adjustment,
    )

    debugfile = time.strftime(entity_id + "-%Y-%m-%d_%H-%M-%S")
    if debug_path is not None:
        cv2.imwrite(os.path.join(debug_path, "%s-in.jpg" % debugfile), frame)

    query_params = {
        # Request parameters
        "language": "en",
        "detectOrientation": "false",
        "model-version": "latest",
    }
    header_params = {
        "Accept": "application/json",
        "Content-Type": "application/octet-stream",
        "Ocp-Apim-Subscription-Key": ocr_key,
    }
    ocr_url = urllib.parse.urljoin(ocr_url, MS_API)

    _LOGGER.debug("%s: OCR image: %s" % (entity_id, ocr_url))
    imencoded = cv2.imencode(".jpg", frame)[1]
    response = requests.post(
        ocr_url,
        data=imencoded.tobytes(),
        params=query_params,
        headers=header_params,
        timeout=9,
    )

    if response.status_code == 200:
        result = response.json()
        if "regions" in result:
            text = ""
            for r in result["regions"]:
                for l in r["lines"]:
                    for w in l["words"]:
                        text = text + w["text"]
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
            x_str = x_str.replace(" ", "").replace(".", "").replace(",", "")
            if len(x_str) == digits and x_str.isnumeric():
                _LOGGER.debug("%s: Final reading: %s" % (entity_id, x_str))
                return x_str
    raise Exception("Unable to OCR image or no text found.")
