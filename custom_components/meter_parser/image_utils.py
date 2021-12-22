
import cv2
import numpy as np
from dataclasses import dataclass
arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_100)
arucoParams = cv2.aruco.DetectorParameters_create()


def zoom_to_roi(image):
    # # sharpen image
    # image = cv2.filter2D(src=image, ddepth=-1, kernel=sharpen)

    (corners, ids, rejected) = cv2.aruco.detectMarkers(
        image, arucoDict, parameters=arucoParams
    )

    markers = list()
    if len(corners) == 2:
        for (markerCorner, markerID) in zip(corners, ids):
            marker = extractMarker(markerCorner, markerID)
            markers.append(marker)
        avg_angle = sum(int(item.angle) for item in markers) / len(markers)
        image = rotate_image(image, -avg_angle)

        (corners, ids, rejected) = cv2.aruco.detectMarkers(
            image, arucoDict, parameters=arucoParams
        )
        markers = list()
        for (markerCorner, markerID) in zip(corners, ids):
            marker = extractMarker(markerCorner, markerID)
            markers.append(marker)
        markers.sort(key=lambda x: x.id)
        topLeft = markers[0].bottomRight
        bottomRight = markers[1].topLeft

        image = crop_image(image, (topLeft[0], topLeft[1], bottomRight[0] - topLeft[0], bottomRight[1] - topLeft[1]))

    else:
        raise Exception("Could not find ArUco markers. Please print two markers at https://chev.me/arucogen/ and stick to the top-left and bottom-right corners of the region of interest. Order by top-left -> bottom-right")

    return image


def extractMarker(markerCorner, markerID: int):
    # extract the marker corners (which are always returned in
    # top-left, top-right, bottom-right, and bottom-left order)
    corners = markerCorner.reshape((4, 2))
    (topLeft, topRight, bottomRight, bottomLeft) = corners
    # convert each of the (x, y)-coordinate pairs to integers
    topRight = (int(topRight[0]), int(topRight[1]))
    bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
    bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
    topLeft = (int(topLeft[0]), int(topLeft[1]))
    # compute the center (x, y)-coordinates of the ArUco
    # marker
    center = (int((topLeft[0] + bottomRight[0]) / 2.0), int((topLeft[1] + bottomRight[1]) / 2.0))

    # Find angle
    angle1 = angle_between(topLeft, topRight)
    angle2 = angle_between(bottomLeft, bottomRight)
    estimated_angle = round((angle1 + angle2) / 2.0)

    return Marker(markerID, topLeft, topRight, bottomLeft, bottomRight, center, estimated_angle)


@dataclass
class Marker:
    id: int
    topLeft: tuple[int, int]
    topRight: tuple[int, int]
    bottomLeft: tuple[int, int]
    bottomRight: tuple[int, int]
    center: tuple[int, int]
    angle: int


def angle_between(p1: tuple[int, int], p2: tuple[int, int]):  # tuple[x,y]
    (p1x, p1y) = p1
    (p2x, p2y) = p2
    xDiff = p2x - p1x
    yDiff = p2y - p1y
    return np.arctan2(yDiff, xDiff) * 180.0 / np.pi


def rotate_image(image, angle, center=None, scale=1.0):
    # grab the dimensions of the image
    (h, w) = image.shape[:2]

    # if the center is None, initialize it as the center of
    # the image
    if center is None:
        center = (w // 2, h // 2)

    # perform the rotation
    matrix = cv2.getRotationMatrix2D(center, -angle, scale)
    rotated = cv2.warpAffine(image, matrix, (w, h), flags=cv2.INTER_NEAREST)

    # return the rotated image
    return rotated


def crop_image(image, rect):
    x = rect[0]
    y = rect[1]
    w = rect[2]
    h = rect[3]
    return image[y: y + h, x: x + w]
