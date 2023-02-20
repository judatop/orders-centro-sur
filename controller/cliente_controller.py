from controller.conexion_controller import Conexion
from controller.gestor_controller import Gestor
from model.cliente import Cliente
from model.cliente_instalacion import Cliente_Instalacion


def obtener_cliente_por_instalacion(numero_instalacion):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        cliente_instalacion = Cliente_Instalacion.get_or_none(Cliente_Instalacion.instalacion == numero_instalacion)

        if cliente_instalacion:
            cliente = Cliente.get_or_none(Cliente.identificacion == cliente_instalacion.cliente)

            if cliente:
                return cliente
        return None

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()
