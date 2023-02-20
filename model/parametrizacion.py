from peewee import *
from model.basemodel import BaseModel


class Parametrizacion(BaseModel):
    tcs = DecimalField(10, 2, null=True)
    tps = DecimalField(10, 2, null=True)
    multiplicador = DecimalField(10, 2, null=True)
    compensacionPerdidas = DecimalField(10, 2, null=True)
    registros = CharField(50, null=True)

