from peewee import *
from model.basemodel import BaseModel


class HistorialRDICO2(BaseModel):
    mes1 = DecimalField(10, 2, null=True)
    mes2 = DecimalField(10, 2, null=True)
    mes3 = DecimalField(10, 2, null=True)
    mes4 = DecimalField(10, 2, null=True)
    mes5 = DecimalField(10, 2, null=True)
    mes6 = DecimalField(10, 2, null=True)
    mes7 = DecimalField(10, 2, null=True)
    mes8 = DecimalField(10, 2, null=True)
    mes9 = DecimalField(10, 2, null=True)
    mes10 = DecimalField(10, 2, null=True)
    mes11 = DecimalField(10, 2, null=True)
    mes12 = DecimalField(10, 2, null=True)
    tipo = CharField(50, null=True)
