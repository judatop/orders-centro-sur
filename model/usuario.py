from flask_login import UserMixin
from peewee import *
from model.basemodel import BaseModel


class Usuario(UserMixin, BaseModel):
    usuario = CharField(50, unique=True)
    clave = CharField(50)
    admin = BooleanField()
    tipo = CharField(50, null=True) # Contratista o Control de la medición
    activo = BooleanField()



    def check_password(self, password):
        if self.clave == password:
            return True
        else:
            return False

