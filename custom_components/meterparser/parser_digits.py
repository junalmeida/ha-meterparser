# digits meter parser based on https://www.pyimagesearch.com/2017/02/13/recognizing-digits-with-opencv-and-python/
# import the necessary packages
import requests
import cv2


OCR_API = "https://api.ocr.space/parse/image"


def parse_digits(frame, digits_count: int, ocr_key: str, debug_path: str = None):
    # Displaying digits and OCR
    # curl -H "apikey:helloworld" --form "base64Image=data:image/jpeg;base64,/9j/AAQSk [Long string here ]" --form "language=eng" --form "isOverlayRequired=false" https://api.ocr.space/parse/image
    imencoded = cv2.imencode(".jpg", frame)[1]
    files = {
        "file": ("image.jpg", imencoded.tostring(), "image/jpeg", {"Expires": "0"})
    }
    payload = {"apikey": ocr_key, "language": "eng", "scale": True, "OCREngine": 2}
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
                return x_str
    raise Exception("Unable to OCR image or no text found.")
