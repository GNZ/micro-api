import urllib2

import cv2
import numpy
from flask import current_app


class CameraService:
    def capture_image(self):
        file = urllib2.urlopen(current_app.config.get('CAMERA_ENDPOINT'))

        image = numpy.asarray(bytearray(file.read()), dtype="uint8")

        raw_image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        return raw_image
