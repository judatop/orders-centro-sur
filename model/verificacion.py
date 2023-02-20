from peewee import *
from model.basemodel import BaseModel


class Verificacion(BaseModel):
    tcsIPrimarioR = DecimalField(10, 2, null=True)
    tcsISecundarioR = DecimalField(10, 2, null=True)
    relacionTransformacionIR = DecimalField(10, 2, null=True)
    tcsIPrimarioS = DecimalField(10, 2, null=True)
    tcsISecundarioS = DecimalField(10, 2, null=True)
    relacionTransformacionIS = DecimalField(10, 2, null=True)
    tcsIPrimarioT = DecimalField(10, 2, null=True)
    tcsISecundarioT = DecimalField(10, 2, null=True)
    relacionTransformacionIT = DecimalField(10, 2, null=True)
    tpsVPrimarioR = DecimalField(10, 2, null=True)
    tpsVSecundarioR = DecimalField(10, 2, null=True)
    relacionTransformacionVR = DecimalField(10, 2, null=True)
    tpsVPrimarioS = DecimalField(10, 2, null=True)
    tpsVSecundarioS = DecimalField(10, 2, null=True)
    relacionTransformacionVS = DecimalField(10, 2, null=True)
    tpsVPrimarioT = DecimalField(10, 2, null=True)
    tpsVSecundarioT = DecimalField(10, 2, null=True)
    relacionTransformacionVT = DecimalField(10, 2, null=True)
