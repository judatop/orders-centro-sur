from peewee import *
from controller.conexion_controller import Conexion


class BaseModel(Model):
    class Meta:
        database = Conexion.db