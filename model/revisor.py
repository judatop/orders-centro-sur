from peewee import *
from model.basemodel import BaseModel
from model.gruporevisor import GrupoRevisor


class Revisor(BaseModel):
    identificacion = CharField(50, unique=True)
    razonSocial = CharField(50)
    firma = BlobField(null=True)
    jefeGrupo = BooleanField()

    # Relacion uno a uno
    grupo_revisor = ForeignKeyField(GrupoRevisor, backref="revisor", on_update="CASCADE")

