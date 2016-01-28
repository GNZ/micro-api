from flask_restful import fields
from peewee import ForeignKeyField, TextField

from project.analysis.type.red_cell_count import RedCellCount
from project.core.db.model import BaseModel
from project.image.model import Image


class Analysis(BaseModel):
    json_fields = {
        'type': fields.String,
        'result': fields.String
    }

    image = ForeignKeyField(Image, related_name='analyses')
    type = TextField(default=RedCellCount.name)
    result = TextField(default='')

    class Meta:
        indexes = (
            # create a unique on image/type
            (('image', 'type'), True),
        )
