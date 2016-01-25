import cv2
import numpy
from flask import current_app

from project.image.model import Image
from project.util.image_utils import ImageUtils


class ImageRepository:
    def __init__(self):
        self.image_utils = ImageUtils()

    def save(self, image):
        file_name = self.image_utils.getOutputFilename(image.id)
        cv2.imwrite(file_name, image.array)

        print 'Writing to ' + file_name
        return image

    def read(self, id):
        image = Image()

        image.id = id
        image.array = cv2.imread(self.image_utils.getOutputFilename(id))

        return image

    def delete(self, id):
        # TODO: Implement
        return True
