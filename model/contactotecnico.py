from peewee import *
from model.basemodel import BaseModel


class ContactoTecnico(BaseModel):
    nombre = CharField(50, null=True)
    telefono = CharField(50, null=True)
    correo = CharField(50, null=True)
    cargo = CharField(50, null=True)