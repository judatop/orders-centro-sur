from peewee import *
from model.basemodel import BaseModel
from model.revisor import Revisor
from model.accionserviciocliente import AccionServicioCliente
from model.cambiomaterial import CambioMaterial
from model.asistenteadministrativo import AsistenteAdministrativo
from model.asistentejefe import AsistenteJefe

class RDICO5(BaseModel):
    fecha = DateField(null = True)

    # Relaciones 1 a 1
    asistente_administrativo = ForeignKeyField(AsistenteAdministrativo, backref="rdico5", on_update="CASCADE", null=True)
    asistente_jefe = ForeignKeyField(AsistenteJefe, backref="rdico5", on_update="CASCADE", null=True)
    cambio_material = ForeignKeyField(CambioMaterial, backref="rdico5", on_update="CASCADE", null=True)

