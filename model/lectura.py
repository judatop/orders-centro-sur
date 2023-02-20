from peewee import *
from model.basemodel import BaseModel


class Lectura(BaseModel):
    path_lectura = CharField(100)
    nombre_archivo = CharField(100)
