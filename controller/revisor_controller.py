from controller.conexion_controller import Conexion
from controller.gestor_controller import Gestor
from model.gruporevisor import GrupoRevisor
from model.revisor import Revisor
from flask import flash

def obtener_revisores():
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        revisores = Revisor.select().execute()
        lista_revisores = []

        for revisor in revisores:

            grupo_revisor = GrupoRevisor.get_or_none(GrupoRevisor.id == revisor.grupo_revisor_id)

            grupo_revisor_nombre = "No asignado"
            if grupo_revisor:
                grupo_revisor_nombre = grupo_revisor.nombre

            revisortemp = RevisorTemp(revisor.id, revisor.identificacion, revisor.razonSocial,
                                      revisor.jefeGrupo, grupo_revisor_nombre)

            lista_revisores.append(revisortemp)

        return lista_revisores

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()


class RevisorTemp:

    def __init__(self, id, identificacion, razon_social, jefe_grupo, grupo_revisor):
        self.id = id
        self.identificacion = identificacion
        self.razon_social = razon_social
        self.jefe_grupo = jefe_grupo
        self.grupo_revisor = grupo_revisor


def obtener_choices_grupos_revisores():
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        grupos_revisores = GrupoRevisor.select().execute()

        lista_grupos_revisores = []

        for g in grupos_revisores:
            lista_grupos_revisores.append((g.nombre, g.nombre))

        return lista_grupos_revisores

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()


def crear_revisor(grupo_revisor, revisor):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        if revisor.identificacion == "":
            flash('Debe ingresar una identificación', 'error')
            return False

        if revisor.razonSocial == "":
            flash('Debe ingresar una razon social', 'error')
            return False

        if grupo_revisor == "":
            flash('Debe seleccionar un grupo revisor', 'error')
            return False

        revisores = Revisor.select().execute()

        for r in revisores:
            if r.identificacion.lower() == revisor.identificacion.lower():
                flash('Ya existe un revisor con la misma identificación', 'error')
                return False

        xgrupo_revisor = GrupoRevisor.get(GrupoRevisor.nombre == grupo_revisor)

        if revisor.jefeGrupo:
            xrevisor_jefe = Revisor.get_or_none(Revisor.grupo_revisor_id == xgrupo_revisor.id, Revisor.jefeGrupo == 1)
            if xrevisor_jefe:
                flash('Ya existe un jefe de grupo asignado al grupo revisor '+grupo_revisor, 'error')
                return False

        revisor.grupo_revisor = xgrupo_revisor

        revisor.save()
        flash('Revisor creado correctamente', 'exito')
        return True

    except Exception as ex:
        flash('Error al intentar crear un revisor', 'error')
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        return False
    finally:
        db.close()


def modificar_revisor(grupo_revisor, revisor):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        if revisor.identificacion == "":
            flash('Debe ingresar una identificación', 'error')
            return False

        if revisor.razonSocial == "":
            flash('Debe ingresar una razon social', 'error')
            return False

        if grupo_revisor == "":
            flash('Debe seleccionar un grupo revisor', 'error')
            return False

        revisores = Revisor.select().execute()

        for r in revisores:
            if r.identificacion.lower() == revisor.identificacion.lower() and r.id != revisor.id:
                flash('Ya existe un revisor con la misma identificación', 'error')
                return False

        xgrupo_revisor = GrupoRevisor.get(GrupoRevisor.nombre == grupo_revisor)

        if revisor.jefeGrupo:
            xrevisor_jefe = Revisor.get_or_none(Revisor.grupo_revisor_id == xgrupo_revisor.id, Revisor.jefeGrupo == 1)
            if xrevisor_jefe:
                flash('Ya existe un jefe de grupo asignado al grupo revisor '+grupo_revisor, 'error')
                return False

        revisor.grupo_revisor = xgrupo_revisor

        revisor.save()
        flash('Revisor modificado correctamente', 'exito')
        return True

    except Exception as ex:
        flash('Error al intentar modificar un revisor', 'error')
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        return False
    finally:
        db.close()

def obtener_revisor(id_revisor):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        revisor = Revisor.get_or_none(Revisor.id == id_revisor)

        if revisor:
            return revisor
        return None

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()