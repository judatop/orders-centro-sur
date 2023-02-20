from peewee import *
from model.basemodel import BaseModel
from model.usuario import Usuario


class AsistenteJefe(BaseModel):
    nombre = CharField(50, null=True, unique=True)

    # Relacion uno a uno
    usuario = ForeignKeyField(Usuario, backref="asistentejefe", on_update="CASCADE")