from datetime import date
from werkzeug.utils import secure_filename
from controller.gestor_controller import Gestor
from controller.conexion_controller import Conexion
from model.accionanomalia import AccionAnomalia
from model.anomaliaencontrada import AnomaliaEncontrada
from model.gruporevisor import GrupoRevisor
from model.instalacion import Instalacion
from model.medidor import Medidor
from model.orden import Orden
from model.revisor import Revisor
from model.usoenergiaverificado import UsoEnergiaVerificado
from model.usuario import Usuario
from flask_login import current_user
from model.cliente import Cliente
from model.rdico2 import RDICO2
from model.cliente_instalacion import Cliente_Instalacion
from model.asistenteadministrativo import AsistenteAdministrativo
from model.asistentejefe import AsistenteJefe
from flask import flash
import pandas


def obtenerOrdenes():
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()
        lista_ordenes = []

        id_usuario_actual = current_user.id

        asistente_jefe = AsistenteJefe.get_or_none(AsistenteJefe.usuario_id == id_usuario_actual)
        asistente_administrativo = AsistenteAdministrativo.get_or_none(AsistenteAdministrativo.usuario_id == id_usuario_actual)

        if asistente_administrativo: # Ordenes para asistente administrativo
            ordenes = Orden.select().where(Orden.estado == "Revisión") 

            for orden in ordenes:
                anomalias = orden.rdico2.anomalias

                for anomalia in anomalias:

                    if anomalia.descripcion.lower() == "sin novedad":
                        instalacion = Instalacion.get(Instalacion.id == orden.instalacion_id)
                        medidor = Medidor.get(Medidor.numero == instalacion.medidor)
                        cliente_instalacion = Cliente_Instalacion.get(Cliente_Instalacion.instalacion == instalacion.numero)
                        cliente = Cliente.get(Cliente.identificacion == cliente_instalacion.cliente)
                        revisor = Revisor.get_or_none(Revisor.id == orden.revisor_id)
                        grupo_revisor = GrupoRevisor.get_or_none(GrupoRevisor.id == revisor.grupo_revisor_id)
                        orden_temp = OrdenTemp(orden.id, orden.numero, cliente.razonSocial, orden.fechaCreacion, orden.estado, orden.comentarioInicial, instalacion.numero, medidor.numero, grupo_revisor.nombre)
                        lista_ordenes.append(orden_temp)
                        break
        elif asistente_jefe:  # Ordenes para asistente jefe

            ordenes = Orden.select().where(Orden.estado == "Revisión")  

            for orden in ordenes:   
                anomalias = orden.rdico2.anomalias

                bandera_agregar = True

                for anomalia in anomalias:
                    if anomalia.descripcion.lower() == "sin novedad":
                        bandera_agregar = False
                        break

                if bandera_agregar:
                    instalacion = Instalacion.get(Instalacion.id == orden.instalacion_id)
                    medidor = Medidor.get(Medidor.numero == instalacion.medidor)
                    cliente_instalacion = Cliente_Instalacion.get(Cliente_Instalacion.instalacion == instalacion.numero)
                    cliente = Cliente.get(Cliente.identificacion == cliente_instalacion.cliente)
                    revisor = Revisor.get_or_none(Revisor.id == orden.revisor_id)
                    grupo_revisor = GrupoRevisor.get_or_none(GrupoRevisor.id == revisor.grupo_revisor_id)
                    orden_temp = OrdenTemp(orden.id, orden.numero, cliente.razonSocial, orden.fechaCreacion, orden.estado, orden.comentarioInicial, instalacion.numero, medidor.numero, grupo_revisor.nombre)
                    lista_ordenes.append(orden_temp)
        else:
            flash('El usuario actual no es asistente jefe o asistente administrativo', 'error')
            
        return lista_ordenes

    except Exception as ex:
        flash('Error recuperando órdenes', 'error')
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

class OrdenTemp:

    def __init__(self, id, numeroOrden, cliente, fechaCreacion, estado, comentarioInicial, instalacion, medidor, grupo):
        self.id = id
        self.numeroOrden = numeroOrden
        self.cliente = cliente
        self.fechaCreacion = fechaCreacion
        self.estado = estado
        self.comentarioInicial = comentarioInicial
        self.instalacion = instalacion
        self.medidor = medidor
        self.grupo = grupo