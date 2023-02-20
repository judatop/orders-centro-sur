from xmlrpc.client import Boolean
from peewee import *
from model.basemodel import BaseModel
from model.usuario import Usuario

class Privilegio(BaseModel):
    usuario = BooleanField(null=True)
    asistente_admin = BooleanField(null=True)
    asistente_jefe = BooleanField(null=True)
    grupo_revisor = BooleanField(null=True)
    revisor = BooleanField(null=True)
    catastro = BooleanField(null=True)
    orden = BooleanField(null=True)
    administrar_orden = BooleanField(null=True)
    tipo = CharField(50, null=True)


    usuarios = ManyToManyField(Usuario, backref="privilegio", on_update="CASCADE")