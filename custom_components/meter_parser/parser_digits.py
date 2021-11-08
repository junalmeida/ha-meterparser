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
import requests
import cv2

_LOGGER = logging.getLogger(__name__)

OCR_API = "https://api.ocr.space/parse/image"


def parse_digits(frame, digits_count: int, ocr_key: str, debug_path: str = None):
    # Displaying digits and OCR
    # curl -H "apikey:helloworld" --form "base64Image=data:image/jpeg;base64,/9j/AAQSk [Long string here ]" --form "language=eng" --form "isOverlayRequired=false" https://api.ocr.space/parse/image
    imencoded = cv2.imencode(".jpg", frame)[1]
    files = {
        "file": ("image.jpg", imencoded.tostring(), "image/jpeg", {"Expires": "0"})
    }
    payload = {"apikey": ocr_key, "language": "eng", "scale": True, "OCREngine": 2}
    _LOGGER.debug("OCR image: %s" % OCR_API)
    response = requests.post(OCR_API, files=files, data=payload, timeout=60)

    if response.status_code == 200:
        result = response.json()
        if "ParsedResults" in result and len(result["ParsedResults"]) > 0:
            result = result["ParsedResults"][0]
            if (
                "ErrorMessage" in result
                and result["ErrorMessage"] is not None
                and result["ErrorMessage"] != ""
            ):
                raise Exception(result["ErrorMessage"])
            else:
                return parse_result(
                    result["ParsedText"] if "ParsedText" in result else None,
                    digits_count,
                )
        if "ErrorMessage" in result:
            raise Exception(result["ErrorMessage"])

    raise Exception(response.text)


def parse_result(ocr: str, digits: int):
    if ocr is not None and ocr != "":
        array = ocr.strip().split("\n")
        for x_str in array:
            x_str = x_str.replace(" ", "").replace(".", "").replace(",", "")
            if len(x_str) == digits and x_str.isnumeric():
                _LOGGER.debug("Final reading: %s" % x_str)
                return x_str
    raise Exception("Unable to OCR image or no text found.")
