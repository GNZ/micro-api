import uuid
from flask_restful import fields


class Analysis:
    json_fields = {
        'id': fields.String,
        'image_id': fields.String,
        'name': fields.String,
        'count': fields.Integer
    }

    def __init__(self, image_id):
        self.id = uuid.uuid4()
        self.image_id = image_id
