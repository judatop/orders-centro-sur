from controller.conexion_controller import Conexion
from controller.gestor_controller import Gestor
from model.asistentejefe import AsistenteJefe
from flask import flash
from model.privilegio import Privilegio

from model.usuario import Usuario


def obtener_asistentes_jefes():
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        asistentes = AsistenteJefe.select().execute()

        lista_asistentes_jefes = []
        for asistente in asistentes:
            usuario = asistente.usuario

            if usuario:
                asistente_temp = AsistenteJefeTemp(asistente.id, asistente.nombre, usuario.usuario)
                lista_asistentes_jefes.append(asistente_temp)

        return lista_asistentes_jefes

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

class AsistenteJefeTemp:
    def __init__(self, id, nombre, usuario):
        self.id = id
        self.nombre = nombre
        self.usuario = usuario

def modificar_asistente(asistente, nombre_usuario):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        if asistente.nombre == "":
            flash('Debe ingresar un nombre', 'error')
            return False

        if nombre_usuario == "":
            flash('Debe seleccionar un usuario', 'error')
            return False

        usuario = Usuario.get_or_none(Usuario.usuario == nombre_usuario)

        if usuario:
            asistente.usuario = usuario

            asistente.save()
            flash('Asistente Jefe modificado correctamente', 'exito')
            return True
        
        return False

    except Exception as ex:
        flash('Error al intentar modificar Asistente Jefe', 'error')
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        return False
    finally:
        db.close()


def crear_asistente(asistente, nombre_usuario):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        if asistente.nombre == "":
            flash('Debe ingresar un nombre', 'error')
            return False

        if nombre_usuario == "":
            flash('Debe seleccionar un usuario', 'error')
            return False

        usuario = Usuario.get_or_none(Usuario.usuario == nombre_usuario)

        if usuario:
            privilegio = Privilegio.get_or_none(Privilegio.tipo == "AsistenteJefe")
            privilegio.usuarios.add(usuario)
            privilegio.save()

            asistente.usuario = usuario

            asistente.save()
            flash('Asistente Jefe creado correctamente', 'exito')
            return True
        
        return False

    except Exception as ex:
        flash('Error al intentar modificar Asistente Jefe', 'error')
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        return False
    finally:
        db.close()

def obtener_asistente(id_asistente):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        asistente = AsistenteJefe.get_or_none(AsistenteJefe.id == id_asistente)

        if asistente:
            return asistente
        return None

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()