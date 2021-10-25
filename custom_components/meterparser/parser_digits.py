# digits meter parser based on https://www.pyimagesearch.com/2017/02/13/recognizing-digits-with-opencv-and-python/
# import the necessary packages
import requests
import cv2


API_KEY = ''
OCR_API = 'https://api.ocr.space/parse/image'


def parse_digits(frame, digits_count: int, debug=False):
    # Displaying digits and OCR
    # curl -H "apikey:helloworld" --form "base64Image=data:image/jpeg;base64,/9j/AAQSk [Long string here ]" --form "language=eng" --form "isOverlayRequired=false" https://api.ocr.space/parse/image
    imencoded = cv2.imencode(".jpg", frame)[1]
    files = {'file': ('image.jpg', imencoded.tostring(), 'image/jpeg', {'Expires': '0'})}
    payload = {
        'apikey': API_KEY,
        'language': 'eng',
        'scale': True,
        'OCREngine': 2
    }
    response = requests.post(OCR_API, files=files, data=payload)

    if response.status_code == 200:
        result = response.json()
        if 'ParsedResults' in result and len(result["ParsedResults"]) > 0:
            result = result['ParsedResults'][0]
            if 'ErrorMessage' in result and result["ErrorMessage"] is not None and result["ErrorMessage"] != "":
                raise Exception(result["ErrorMessage"])
            elif result["ParsedText"] == '':
                raise Exception("Unable to OCR image")
            else:
                return parse_result(result["ParsedText"].strip(), digits_count)
        if 'ErrorMessage' in result:
            raise Exception(result["ErrorMessage"])

    raise Exception(response.text)


def parse_result(ocr: str, digits: int):
    array = ocr.split('\n')
    for x in array:
        if len(x) == digits and x.isnumeric():
            return x
    raise Exception("Unable to OCR image")
