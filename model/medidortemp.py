from peewee import *
from model.basemodel import BaseModel


class MedidorTemp(BaseModel):
    id = PrimaryKeyField()
    ano = CharField(50, null=True)
    exactitud = CharField(50, null=True)
    corriente = CharField(50, null=True)
    voltaje = CharField(50, null=True)
    constanteK = DecimalField(10, 2, null=True)
    tipo_medicion = CharField(50, null=True)
    conexion = CharField(50, null=True)
    marca = CharField(50, null=True)
    tipo = CharField(50, null=True)
