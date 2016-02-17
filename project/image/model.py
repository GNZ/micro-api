import datetime
import uuid

from flask_restful import fields
from peewee import UUIDField, TextField, DateTimeField

from project.db.model import BaseModel


class Image(BaseModel):
    analysis_json_fields = {
        'type': fields.String,
        'result': fields.String
    }

    json_fields = {
        'id': fields.String,
        'analyses': fields.List(fields.Nested(analysis_json_fields)),
        'created_at': fields.DateTime('iso8601'),
        'description': fields.String,
        'name': fields.String
    }

    id = UUIDField(primary_key=True, default=uuid.uuid4)
    description = TextField(default='')
    name = TextField(default='')
    created_at = DateTimeField(default=datetime.datetime.now)
