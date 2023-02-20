from controller.conexion_controller import Conexion
from controller.gestor_controller import Gestor
from model.instalacion import Instalacion


def obtener_instalacion(instalacion_id):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        instalacion = Instalacion.get_or_none(Instalacion.id == instalacion_id)

        if instalacion:
            return instalacion
        return None

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def obtener_contacto_tecnico(instalacion):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        contacto_tecnico = instalacion.contacto_tecnico
        
        if contacto_tecnico:
            return contacto_tecnico
        return None

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()
