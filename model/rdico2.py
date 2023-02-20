from peewee import *
from model.basemodel import BaseModel
from model.fotografia import Fotografia
from model.historialrdico2 import HistorialRDICO2
from model.lectura import Lectura
from model.lecturatotal import LecturaTotal
from model.perfildecarga import PerfilDeCarga
from model.parametrizacion import Parametrizacion
from model.usoenergiaverificado import UsoEnergiaVerificado
from model.anomaliaencontrada import AnomaliaEncontrada
from model.prueba import Prueba
from model.verificacion import Verificacion
from model.sello import Sello
from model.transformadordedistribucion import TransformadorDeDistribucion
from model.transformadordemedida import TransformadorDeMedida
from model.medidor import Medidor
from model.gruporevisor import GrupoRevisor


class RDICO2(BaseModel):
    resultadoVerificacion = CharField(100, null=True)
    nuevoTipoDeTarifa = CharField(100, null=True)
    observaciones = TextField(null=True)
    tipoForm = CharField(50, null=True)
    fecha = DateField(null=True)

    # Relaciones 1 a 1
    lectura = ForeignKeyField(Lectura, backref="rdico2", on_update="CASCADE", null=True)
    perfil_carga = ForeignKeyField(PerfilDeCarga, backref="rdico2", on_update="CASCADE", null=True)
    parametrizacion = ForeignKeyField(Parametrizacion, backref="rdico2", on_update="CASCADE", null=True)
    verificacion = ForeignKeyField(Verificacion, backref="rdico2", on_update="CASCADE", null=True)

    # Relaciones varios a varios
    fotografias = ManyToManyField(Fotografia, backref="rdico2", on_update="CASCADE")
    usosEnergiaVerificado = ManyToManyField(UsoEnergiaVerificado, backref="rdico2", on_update="CASCADE")
    pruebas = ManyToManyField(Prueba, backref="rdico2", on_update="CASCADE")
    sellos = ManyToManyField(Sello, backref="rdico2", on_update="CASCADE")
    transformadoresDeDistribucion = ManyToManyField(TransformadorDeDistribucion,
                                                    backref="rdico2", on_update="CASCADE")
    transformadoresDeMedida = ManyToManyField(TransformadorDeMedida, backref="rdico2",
                                              on_update="CASCADE")
    lecturas = ManyToManyField(LecturaTotal, backref="rdico2", on_update="CASCADE")
    historiales = ManyToManyField(HistorialRDICO2, backref="rdico2", on_update="CASCADE")
    anomalias = ManyToManyField(AnomaliaEncontrada, backref="rdico2", on_update="CASCADE")