from peewee import Model

from project import micro_db


class BaseModel(Model):
    class Meta:
        database = micro_db
