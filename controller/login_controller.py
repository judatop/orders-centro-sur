from controller.conexion_controller import Conexion
from controller.gestor_controller import Gestor
from model.usuario import Usuario


def get_user(username):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        xuser = Usuario.get_or_none(usuario=username)
        return xuser
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

