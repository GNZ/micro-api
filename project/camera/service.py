import urllib2

import cv2
import numpy
from flask import current_app

from project.image.repository import ImageRepository


class CameraService:
    def __init__(self):
        self.image_repository = ImageRepository()

    def capture_image(self):
        if current_app.config.get('DEVELOPMENT'):
            # Read mock image
            raw_image = self.image_repository.read(current_app.config['CAMERA_MOCK_IMAGE_ID'])
        else:
            # Get image from mjpeg server
            file = urllib2.urlopen(current_app.config.get('CAMERA_ENDPOINT'))
            image = numpy.asarray(bytearray(file.read()), dtype="uint8")
            raw_image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        return raw_image
