from peewee import *
from model.basemodel import BaseModel
from model.contactotecnico import ContactoTecnico
from model.medidor import Medidor


class Instalacion(BaseModel):
    numero = CharField(50, null=True, index=True)
    coordenadaX = DecimalField(20, 10, null=True)
    coordenadaY = DecimalField(20, 10, null=True)
    utmX = DecimalField(20, 10, null=True)
    utmY = DecimalField(20, 10, null=True)
    numeroPoste = CharField(50, null=True)
    medidor = CharField(50, null=True)

    # Relacion uno a uno
    contacto_tecnico = ForeignKeyField(ContactoTecnico, backref="instalacion", on_update="CASCADE", null=True)