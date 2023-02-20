from peewee import *
from model.basemodel import BaseModel


class PerfilDeCarga(BaseModel):
    path_perfil = CharField(100)
    nombre_archivo = CharField(100)
