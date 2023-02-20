from peewee import *
from model.basemodel import BaseModel


class TransformadorDeDistribucion(BaseModel):
    numero = CharField(50, null=True)
    marca = CharField(50, null=True)
    tipo = CharField(50, null=True)
    capacidadMaxima = DecimalField(10, 2, null=True)
    voltaje = DecimalField(10, 2, null=True)
    ano = IntegerField(null=True)
    zcc = CharField(50, null=True)
    conexion = CharField(50, null=True)