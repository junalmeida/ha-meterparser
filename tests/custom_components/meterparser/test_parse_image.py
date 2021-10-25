import os
import cv2

from custom_components.meterparser.parser_dial import parse_dials
from custom_components.meterparser.parser_digits import parse_digits


def test_eletricity_dials_1():
    samplepath = os.path.join(os.path.dirname(__file__), 'sample_eletricity-1.jpg')
    inputFrame = cv2.imread(samplepath)
    reading = parse_dials(inputFrame, ["CCW", "CW", "CCW", "CW"], minDiameter=200, maxDiameter=300, debug=True)
    assert reading == '3124'


def test_eletricity_dials_2():
    samplepath = os.path.join(os.path.dirname(__file__), 'sample_eletricity-2.jpg')
    inputFrame = cv2.imread(samplepath)
    reading = parse_dials(inputFrame, ["CCW", "CW", "CCW", "CW"], minDiameter=200, maxDiameter=300, debug=True)
    assert reading == '2211'


def test_eletricity_dials_3():
    samplepath = os.path.join(os.path.dirname(__file__), 'sample_eletricity-3.jpg')
    inputFrame = cv2.imread(samplepath)
    reading = parse_dials(inputFrame, ["CW", "CCW", "CW", "CCW", "CW"], minDiameter=200, maxDiameter=300, debug=True)
    assert reading == '68451'


def test_gas_dials_1():
    samplepath = os.path.join(os.path.dirname(__file__), 'sample_gas-1.jpg')
    inputFrame = cv2.imread(samplepath)
    reading = parse_dials(inputFrame, ["CCW", "CW", "CCW", "CW"], minDiameter=300, maxDiameter=400, debug=True)
    assert reading == '3876'


def test_gas_dials_2():
    samplepath = os.path.join(os.path.dirname(__file__), 'sample_gas-2.jpg')
    inputFrame = cv2.imread(samplepath)
    reading = parse_dials(inputFrame, ["CCW", "CW", "CCW", "CW"], minDiameter=290, maxDiameter=330, debug=True)
    assert reading == '0140'


def test_water_dial_1():
    samplepath = os.path.join(os.path.dirname(__file__), 'sample_water-1.jpg')
    inputFrame = cv2.imread(samplepath)
    reading = parse_dials(inputFrame, ["CW"], minDiameter=640, maxDiameter=840, debug=True)
    assert reading == '0'


def test_water_dial_2():
    samplepath = os.path.join(os.path.dirname(__file__), 'sample_water-2.jpg')
    inputFrame = cv2.imread(samplepath)
    reading = parse_dials(inputFrame, ["CW"], minDiameter=1010, maxDiameter=1400, debug=True)
    assert reading == '1'


def test_water_dial_3():
    samplepath = os.path.join(os.path.dirname(__file__), 'sample_water-3.jpg')
    inputFrame = cv2.imread(samplepath)
    reading = parse_dials(inputFrame, ["CW"], minDiameter=1010, maxDiameter=1230, debug=True)
    assert reading == '5'


def test_water_digits_1():
    samplepath = os.path.join(os.path.dirname(__file__), 'sample_water-1.jpg')
    inputFrame = cv2.imread(samplepath)
    reading = parse_digits(inputFrame, 6)
    assert reading == '000200'


def test_water_digits_2():
    samplepath = os.path.join(os.path.dirname(__file__), 'sample_water-2.jpg')
    inputFrame = cv2.imread(samplepath)
    reading = parse_digits(inputFrame, 6)
    assert reading == '000110'


def test_water_digits_3():
    samplepath = os.path.join(os.path.dirname(__file__), 'sample_water-3.jpg')
    inputFrame = cv2.imread(samplepath)
    reading = parse_digits(inputFrame, 6)
    assert reading == '027795'
