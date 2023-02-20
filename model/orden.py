from peewee import *
from model.basemodel import BaseModel
from model.instalacion import Instalacion
from model.rdico2 import RDICO2
from model.rdico5 import RDICO5
from model.revisor import Revisor


class Orden(BaseModel):
    numero = CharField(100, null=True, index=True)
    fechaCreacion = DateField(null=True)
    fechaEjecucion = DateField(null=True)
    fechaGestion = DateField(null=True)
    fechaCierre = DateField(null=True)
    estado = CharField(100, null=True)
    comentarioInicial = CharField(100, null=True)

    # Relaciones 1 a 1
    instalacion = ForeignKeyField(Instalacion, backref="orden", on_update="CASCADE", null=True)
    rdico2 = ForeignKeyField(RDICO2, backref="orden", on_update="CASCADE", null=True)
    rdico5 = ForeignKeyField(RDICO5, backref="orden", on_update="CASCADE", null=True)
    revisor = ForeignKeyField(Revisor, backref="orden", on_update="CASCADE", null=True)


