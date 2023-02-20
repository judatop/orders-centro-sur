from peewee import *
from model.basemodel import BaseModel


class Prueba(BaseModel):
    rfase1 = DecimalField(10, 2, null=True)
    sfase2 = DecimalField(10, 2, null=True)
    tfase3 = DecimalField(10, 2, null=True)
    potencia_total = DecimalField(10, 2, null=True)
    revoluciones = DecimalField(10, 2, null=True)
    tiempo = DecimalField(10, 2, null=True)
    pkw_medidor = DecimalField(10, 2, null=True)
    error = DecimalField(10, 2, null=True)
    unidadElectrica = CharField(50, null=True)
