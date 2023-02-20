from flask_login import current_user
from controller.conexion_controller import Conexion
from controller.gestor_controller import Gestor
from model.privilegio import Privilegio
from model.usuario import Usuario
from flask import flash


def obtener_usuarios():
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        usuarios = Usuario.select().execute()

        return usuarios

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def obtener_usuarios_choices():
    try:
        db = Conexion.db
        db.connect()

        usuarios = Usuario.select().execute()

        tuplas = []

        for usuario in usuarios:
            tuplas.append((usuario.usuario, usuario.usuario))

        return tuplas

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()


def obtener_usuario(id_usuario):
    try:
        db = Conexion.db
        db.connect()

        usuario = Usuario.get_or_none(Usuario.id == id_usuario)

        if usuario:
            return usuario
        return None

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()


def modificar_usuario(usuario):
    try:
        db = Conexion.db
        db.connect()

        if usuario.usuario == "":
            flash('Debe ingresar un nombre de usuario', 'error')
            return False

        if usuario.clave == "":
            flash('Debe ingresar una clave', 'error')
            return False

        usuarios = Usuario.select()

        for u in usuarios:
            if u.usuario == usuario.usuario and u.id != usuario.id:
                flash('Ya existe un usuario con el mismo nombre', 'error')
                return False

        usuario.save()
        flash('Usuario modificado correctamente', 'exito')
        return True

    except Exception as ex:
        flash('Error al intentar modificar usuario', 'error')
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        return False
    finally:
        db.close()


def crear_usuario(usuario):
    try:
        db = Conexion.db
        db.connect()

        if usuario.usuario == "":
            flash('Debe ingresar un nombre de usuario', 'error')
            return False

        if usuario.clave == "":
            flash('Debe ingresar una clave', 'error')
            return False

        usuarios = Usuario.select()

        for u in usuarios:
            if u.usuario == usuario.usuario:
                flash('Ya existe un usuario con el mismo nombre', 'error')
                return False

        usuario.save()
        flash('Usuario creado correctamente', 'exito')
        return True

    except Exception as ex:
        flash('Error al intentar crear un usuario', 'error')
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        return False
    finally:
        db.close()


def verificar_privilegios(modulo):
    try:
        db = Conexion.db
        db.connect()

        id_usuario_actual = current_user.id
        usuario = Usuario.get_or_none(Usuario.id == id_usuario_actual)

        if usuario:
            if usuario.admin:
                return True

            if modulo == "Orden":
                privilegio_grupo = Privilegio.get_or_none(Privilegio.tipo == "GrupoRevisor")
                if usuario in privilegio_grupo.usuarios:
                    return True
                else:
                    flash('No tiene privilegios para acceder','error')
                    return False

            if modulo == "AdministrarOrden":
                privilegio_jefe = Privilegio.get_or_none(Privilegio.tipo == "AsistenteJefe")
                privilegio_admin = Privilegio.get_or_none(Privilegio.tipo == "AsistenteAdmin")
                if usuario in privilegio_jefe.usuarios or usuario in privilegio_admin.usuarios:
                    return True
                else:
                    flash('No tiene privilegios para acceder','error')
                    return False
        flash('No tiene privilegios para acceder','error')
        return False
        
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        return False
    finally:
        db.close()