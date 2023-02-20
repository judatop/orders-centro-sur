from peewee import *
from model.basemodel import BaseModel

class LecturaTotal(BaseModel):
    a_horarias = DecimalField(10, 2, null=True)
    b_horarias = DecimalField(10, 2, null=True)
    c_horarias = DecimalField(10, 2, null=True)
    d_horarias = DecimalField(10, 2, null=True)
    a_demandas = DecimalField(10, 2, null=True)
    b_demandas = DecimalField(10, 2, null=True)
    c_demandas = DecimalField(10, 2, null=True)
    d_demandas = DecimalField(10, 2, null=True)
    kvarh = DecimalField(10, 2, null=True)
    tipo = CharField(50, null=True)
