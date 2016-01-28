import os

from flask_restful import abort
from peewee import DoesNotExist

from project.image.model import Image
from project.util.image_utils import ImageUtils


class DatabaseService:

    image_utils = ImageUtils()

    def save_image(self, image):
        image.save()

    def get_images(self):
        # TODO: Should we fetch analyses here?
        result_set = Image.select().execute()

        array_result = []

        for result in result_set:
            array_result.append(result)

        return array_result

    def get_image(self, id):
        try:
            image = Image.get(id=str(id))
        except DoesNotExist:
            abort(404)

        return image

    def delete_image(self, id):
        try:
            image = Image.get(id=str(id))
        except DoesNotExist:
            abort(404)

        image.delete_instance()

        os.remove(self.image_utils.getOutputFilename(id))

        return

    def update_image(self, image):
        image.save()

        return image
