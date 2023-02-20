from peewee import *
from model.basemodel import BaseModel


class UsoEnergiaVerificado(BaseModel):
    descripcion = CharField(255, null=True)
