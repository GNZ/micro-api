from flask_restful import Resource, fields, marshal_with_field, marshal_with

from project.image.model import Image
from project.image.service import ImageService


class ImageListController(Resource):
    def __init__(self):
        self.image_service = ImageService()

    @marshal_with_field(fields.List(fields.Nested(Image.json_fields)))
    def get(self):
        images = self.image_service.getAll()

        return images

    @marshal_with(Image.json_fields)
    def post(self):
        image = self.image_service.create()

        return image
