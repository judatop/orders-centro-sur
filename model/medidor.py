from peewee import *
from model.basemodel import BaseModel
from model.historialmedidor import HistorialMedidor


class Medidor(BaseModel):
    cc = CharField(50, index=True)
    numero = CharField(50, null=True, index=True)
    ano = IntegerField(null=True)
    exactitud = CharField(50, null=True)
    consumokWh = DecimalField(10, 2, null=True)
    corriente = CharField(50, null=True)
    voltaje = CharField(50, null=True)
    constanteK = DecimalField(10, 2, null=True)
    tipo_medicion = CharField(50, null=True) # directa o indirecta
    conexion = CharField(50, null=True)
    marca = CharField(50, null=True)
    tipo = CharField(50, null=True)
    disponible_compensacion = BooleanField(null=True)
    parametrizado_compensacion = BooleanField(null=True)
    factor_potencia = DecimalField(10, 2, null=True)

    # Relaciones varios a varios
    historiales = ManyToManyField(HistorialMedidor, backref="medidor", on_update="CASCADE")
