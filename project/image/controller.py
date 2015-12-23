from flask_restful import Resource, marshal_with

from project.image.model import Image
from project.image.service import ImageService


class ImageController(Resource):
    def __init__(self):
        self.image_service = ImageService()

    @marshal_with(Image.json_fields)
    def get(self, id):
        image = self.image_service.get(id)

        return image

    @marshal_with(Image.json_fields)
    def post(self):
        image = self.image_service.create()

        return image

    def delete(self, id):
        result = self.image_service.delete(id)

        return result
