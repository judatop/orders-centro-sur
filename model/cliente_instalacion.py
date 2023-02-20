from peewee import *
from model.basemodel import BaseModel
from model.cliente import Cliente
from model.instalacion import Instalacion


class Cliente_Instalacion(BaseModel):
    cliente = CharField(50)
    instalacion = CharField(50)
