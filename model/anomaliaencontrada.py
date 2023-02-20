from peewee import *
from model.basemodel import BaseModel
from model.accionanomalia import AccionAnomalia


class AnomaliaEncontrada(BaseModel):
    descripcion = CharField(255, null=True)

