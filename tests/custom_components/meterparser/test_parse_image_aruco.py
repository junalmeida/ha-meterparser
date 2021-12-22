from custom_components.meter_parser.image_utils import crop_image, rotate_image
import os
import cv2

from custom_components.meter_parser.parser_dial import parse_dials
from custom_components.meter_parser.parser_digits import parse_digits
from custom_components.meter_parser.sensor import zoom_to_roi

ocr_key = "890a9b9b8388957"
entity_id = "test.test"
dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..", "results")


def test_parse_aruco_digits():
    samplepath = os.path.join(os.path.dirname(__file__), 'sample_water-aruco.jpg')
    inputFrame = cv2.imread(samplepath)
    inputFrame = zoom_to_roi(inputFrame)
    reading = parse_digits(inputFrame, 6, 1, ocr_key, entity_id, debug_path=dir_path)
    assert reading == 2813.0
