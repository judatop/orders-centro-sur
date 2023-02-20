from peewee import *
from model.basemodel import BaseModel


class AccionAnomalia(BaseModel):
    descripcion = CharField(255, null=True)

