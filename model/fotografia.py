from numpy import size
from peewee import *
from model.basemodel import BaseModel


class Fotografia(BaseModel):
    path_imagen = CharField(100)
    nombre_archivo = CharField(100)
