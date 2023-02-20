from peewee import *
from model.basemodel import BaseModel
from model.instalacion import Instalacion
from model.medidor import Medidor


class Cliente(BaseModel):
    identificacion = CharField(50, unique=True)
    razonSocial = CharField(100)
    direccion = CharField(null=True)
    correo = CharField(100, null=True)
    telefono = CharField(45, null=True)
    cuenta = CharField(45, null=True)
    tipoTarifa = CharField(45, null=True)
    dminkW = DecimalField(10, 2, null=True)
    dmaxkW = DecimalField(10, 2, null=True)
    fp = DecimalField(10, 2, null=True)
    mru = CharField(50, null=True)
    fm = DecimalField(10, 2, null=True)



