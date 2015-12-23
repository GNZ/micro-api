import uuid

from flask_restful import fields


class Image:
    json_fields = {
        'id': fields.String
    }

    def __init__(self):
        self.id = uuid.uuid4()
        self.array = None
