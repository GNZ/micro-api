from flask_restful import fields
from peewee import ForeignKeyField, TextField

from project.core.db.model import BaseModel
from project.image.model import Image


class Analysis(BaseModel):
    json_fields = {
        'name': fields.String,
        'result': fields.Integer
    }

    image = ForeignKeyField(Image, related_name='analyses')
    name = TextField(default='')
    result = TextField(default='')
