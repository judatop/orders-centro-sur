from peewee import *
from model.basemodel import BaseModel


class AccionServicioCliente(BaseModel):

    multaSellosRotos = BooleanField(null=True)
    materialesCostoCliente = BooleanField(null=True)
    retiroMedidor = BooleanField(null=True)
    actualizarCambioMedidor = BooleanField(null=True)
    actualizarDireccion = BooleanField(null=True)
    centralizarMedidores = BooleanField(null=True)
    descripcionCentralizarMedidores = CharField(100, null=True)
    reubicarMedidor = BooleanField(null=True)
    descripcionReubicarMedidor = CharField(100, null=True)
    reliquidarEventual = BooleanField(null=True)
    descripcionReliquidarEventua = CharField(100, null=True)
    unificarCargar = BooleanField(null=True)
    descripcionUnificarCarga = CharField(100, null=True)
    enviarOficioMantenimiento = BooleanField(null=True)
    descripcionEnviarOficioMantenimiento = CharField(100, null=True)
    enviarOficioFP = BooleanField(null=True)
    descripcionEnviarOficioFP = CharField(100, null=True)
    otros = CharField(100, null=True)