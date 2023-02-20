from peewee import *
from model.basemodel import BaseModel


class TransformadorDeMedida(BaseModel):
    numeroDeSerie = CharField(50, null=True)
    numeroDeEmpresa = CharField(50, null=True)
    marca = CharField(50, null=True)
    relacionDeTransformacion = CharField(50, null=True)
    burden = CharField(50, null=True)
    exactitud = CharField(50, null=True)
    ano = IntegerField()
    sellosEncontrados = CharField(50, null=True)
    tipo = CharField(50, null=True)