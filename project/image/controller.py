from flask import request
from flask_restful import Resource, marshal_with, abort
from peewee import DoesNotExist

from project.image.model import Image
from project.image.service import ImageService


class ImageController(Resource):
    def __init__(self):
        self.image_service = ImageService()

    @marshal_with(Image.json_fields)
    def get(self, id):
        image = self.image_service.get(id)

        return image

    def delete(self, id):
        self.image_service.delete(id)

        return True

    @marshal_with(Image.json_fields)
    def put(self, id):
        image = parse_image(id, request.get_json())

        new_image = self.image_service.update(image)

        return new_image


def parse_image(id, json):
    try:
        image = Image.get(id=id)
    except DoesNotExist:
        abort(404)

    image.description = get_or_abort_bad_request(json, 'description')
    image.name = get_or_abort_bad_request(json, 'name')

    return image


def get_or_abort_bad_request(args, name):
    arg = args[name]

    if arg is None:
        abort(400)

    return arg
