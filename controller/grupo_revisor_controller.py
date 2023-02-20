from controller.conexion_controller import Conexion
from controller.gestor_controller import Gestor
from model.gruporevisor import GrupoRevisor
from model.orden import Orden
from model.privilegio import Privilegio
from model.revisor import Revisor
from model.usuario import Usuario
from flask import flash


def obtener_grupos_revisores():
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        lista_grupos_revisores = []

        grupos_revisores = GrupoRevisor.select().execute()
        for grupo in grupos_revisores:

            revisor = Revisor.get_or_none(Revisor.grupo_revisor_id == grupo.id, Revisor.jefeGrupo == 1)

            jefe_grupo = "No asignado"
            if revisor:
                jefe_grupo = revisor.razonSocial

            usuario = Usuario.get_or_none(Usuario.id == grupo.usuario_id)

            g = GrupoRevisorTemp(grupo.id, grupo.nombre, usuario.tipo, jefe_grupo, usuario.usuario)

            lista_grupos_revisores.append(g)

        return lista_grupos_revisores

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()


class GrupoRevisorTemp:

    def __init__(self, id, nombre, tipo, jefe_grupo, usuario):
        self.id = id
        self.nombre = nombre
        self.tipo = tipo
        self.jefe_grupo = jefe_grupo
        self.usuario = usuario


def obtener_grupo_revisor(grupo_revisor_id):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        grupo_revisor = GrupoRevisor.get_or_none(GrupoRevisor.id == grupo_revisor_id)

        if grupo_revisor:
            return grupo_revisor
        return None

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()


def modificar_grupo_revisor(username, grupo_revisor):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        if grupo_revisor.nombre == "":
            flash('Debe ingresar un nombre', 'error')
            return False

        if username == "":
            flash('Debe seleccionar un usuario', 'error')
            return False

        grupos_revisores = GrupoRevisor.select().execute()

        for g in grupos_revisores:
            if g.nombre.lower() == grupo_revisor.nombre.lower() and g.id != grupo_revisor.id:
                flash('Ya existe un grupo revisor con el mismo nombre', 'error')
                return False

        usuario = Usuario.get(Usuario.usuario == username)

        grupo_revisor.usuario = usuario

        grupo_revisor.save()
        flash('Grupo revisor modificado correctamente', 'exito')
        return True

    except Exception as ex:
        flash('Error al intentar modificar grupo revisor', 'error')
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        return False
    finally:
        db.close()


def crear_grupo_revisor(username, grupo_revisor):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        if grupo_revisor.nombre == "":
            flash('Debe ingresar un nombre', 'error')
            return False

        if username == "":
            flash('Debe seleccionar un usuario', 'error')
            return False

        grupos_revisores = GrupoRevisor.select().execute()

        for g in grupos_revisores:
            if g.nombre.lower() == grupo_revisor.nombre.lower():
                flash('Ya existe un grupo revisor con el mismo nombre', 'error')
                return False

        usuario = Usuario.get(Usuario.usuario == username)

        if usuario:
            privilegio = Privilegio.get_or_none(Privilegio.tipo == "GrupoRevisor")
            privilegio.usuarios.add(usuario)
            privilegio.save()
            grupo_revisor.usuario = usuario
            grupo_revisor.save()

        flash('Grupo revisor creado correctamente', 'exito')
        return True

    except Exception as ex:
        flash('Error al intentar crear un grupo revisor', 'error')
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        return False
    finally:
        db.close()


def obtener_choices_usuarios():
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        usuarios = Usuario.select().execute()

        lista_usuarios = []

        for usuario in usuarios:
            lista_usuarios.append((usuario.usuario, usuario.usuario))

        return lista_usuarios

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()


def obtener_grupo_revisor_para_orden(revisor_id):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        revisor = Revisor.get_or_none(Revisor.id == revisor_id)

        if revisor:
            grupo_revisor_id = revisor.grupo_revisor.id

            revisores = Revisor.select().where(Revisor.grupo_revisor_id == grupo_revisor_id)

            grupo_revisor_orden = ""

            for revisor in revisores:
                grupo_revisor_orden += "-"+revisor.razonSocial
                return grupo_revisor_orden

        return None

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()