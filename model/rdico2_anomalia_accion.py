from peewee import *
from model.anomaliaencontrada import AnomaliaEncontrada
from model.accionanomalia import AccionAnomalia
from model.rdico2 import RDICO2
from model.basemodel import BaseModel


class RDICO2_Anomalia_Accion(BaseModel):
    rdico2 = ForeignKeyField(RDICO2, backref="rdico2_anomalia_accion", on_update="CASCADE", null=True)
    anomalia = ForeignKeyField(AnomaliaEncontrada, backref="rdico2_anomalia_accion", on_update="CASCADE", null=True)
    accion = ForeignKeyField(AccionAnomalia, backref="rdico2_anomalia_accion", on_update="CASCADE", null=True)