from peewee import *
from model.basemodel import BaseModel


class Sello(BaseModel):
    sello = CharField(50, null=True)
    modelo = CharField(50, null=True)
    ubicacion = CharField(50, null=True)
    estado = CharField(50, null=True)
    tipo = CharField(50, null=True)
