import os
import cv2

from custom_components.meter_parser.parser_dial import parse_dials
from custom_components.meter_parser.parser_digits import parse_digits

ocr_key = "890a9b9b8388957"
entity_id = "test.test"
dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..", "results")


def test_eletricity_dials_1():
    samplepath = os.path.join(os.path.dirname(__file__), 'sample_eletricity-1.jpg')
    inputFrame = cv2.imread(samplepath)
    reading = parse_dials(inputFrame, ["CCW", "CW", "CCW", "CW"], entity_id, minDiameter=200, maxDiameter=300, debug_path=dir_path)
    assert reading == '3124'


def test_eletricity_dials_2():
    samplepath = os.path.join(os.path.dirname(__file__), 'sample_eletricity-2.jpg')
    inputFrame = cv2.imread(samplepath)
    reading = parse_dials(inputFrame, ["CCW", "CW", "CCW", "CW"], entity_id, minDiameter=200, maxDiameter=300, debug_path=dir_path)
    assert reading == '2211'


def test_eletricity_dials_3():
    samplepath = os.path.join(os.path.dirname(__file__), 'sample_eletricity-3.jpg')
    inputFrame = cv2.imread(samplepath)
    reading = parse_dials(inputFrame, ["CW", "CCW", "CW", "CCW", "CW"], entity_id, minDiameter=200, maxDiameter=300, debug_path=dir_path)
    assert reading == '68451'


def test_gas_dials_1():
    samplepath = os.path.join(os.path.dirname(__file__), 'sample_gas-1.jpg')
    inputFrame = cv2.imread(samplepath)
    reading = parse_dials(inputFrame, ["CCW", "CW", "CCW", "CW"], entity_id, minDiameter=300, maxDiameter=400, debug_path=dir_path)
    assert reading == '3876'


def test_gas_dials_2():
    samplepath = os.path.join(os.path.dirname(__file__), 'sample_gas-2.jpg')
    inputFrame = cv2.imread(samplepath)
    reading = parse_dials(inputFrame, ["CCW", "CW", "CCW", "CW"], entity_id, minDiameter=290, maxDiameter=330, debug_path=dir_path)
    assert reading == '0140'


def test_water_dial_1():
    samplepath = os.path.join(os.path.dirname(__file__), 'sample_water-1.jpg')
    inputFrame = cv2.imread(samplepath)
    reading = parse_dials(inputFrame, ["CW"], entity_id, minDiameter=640, maxDiameter=840, debug_path=dir_path)
    assert reading == '0'


def test_water_dial_2():
    samplepath = os.path.join(os.path.dirname(__file__), 'sample_water-2.jpg')
    inputFrame = cv2.imread(samplepath)
    reading = parse_dials(inputFrame, ["CW"], entity_id, minDiameter=1010, maxDiameter=1400, debug_path=dir_path)
    assert reading == '1'


def test_water_dial_3():
    samplepath = os.path.join(os.path.dirname(__file__), 'sample_water-3.jpg')
    inputFrame = cv2.imread(samplepath)
    reading = parse_dials(inputFrame, ["CW"], entity_id, minDiameter=1010, maxDiameter=1230, debug_path=dir_path)
    assert reading == '5'


def test_water_digits_1():
    samplepath = os.path.join(os.path.dirname(__file__), 'sample_water-1.jpg')
    inputFrame = cv2.imread(samplepath)
    inputFrame = crop(inputFrame, [179, 155, 194, 50])
    reading = parse_digits(inputFrame, 6, ocr_key, entity_id, debug_path=dir_path)
    assert reading == '028020'


def test_water_digits_2():
    samplepath = os.path.join(os.path.dirname(__file__), 'sample_water-2.jpg')
    inputFrame = cv2.imread(samplepath)
    inputFrame = crop(inputFrame, [40, 144, 118, 50])
    reading = parse_digits(inputFrame, 6, ocr_key, entity_id, debug_path=dir_path)
    assert reading == '000110'


def test_water_digits_3():
    samplepath = os.path.join(os.path.dirname(__file__), 'sample_water-3.jpg')
    inputFrame = cv2.imread(samplepath)
    inputFrame = crop(inputFrame, [451, 414, 372, 133])
    reading = parse_digits(inputFrame, 6, ocr_key, entity_id, debug_path=dir_path)
    assert reading == '000200'


def crop(image, rect):
    x = rect[0]
    y = rect[1]
    w = rect[2]
    h = rect[3]
    return image[y: y + h, x: x + w]
