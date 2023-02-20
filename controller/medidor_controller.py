from controller.conexion_controller import Conexion
from controller.gestor_controller import Gestor
from model.instalacion import Instalacion
from model.medidor import Medidor
from model.medidortemp import MedidorTemp
from model.historialmedidor import HistorialMedidor


def obtener_medidor_por_instalacion(numero_instalacion):
    try:
        db = Conexion.db
        db.connect()

        instalacion = Instalacion.get_or_none(Instalacion.numero == numero_instalacion)

        medidor = Medidor.get_or_none(Medidor.numero == instalacion.medidor)

        if medidor:
            return medidor
        return None

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def obtener_medidores_temp_por_marca(nombre_marca):
    try:
        db = Conexion.db
        db.connect()

        lista_medidores_temp = MedidorTemp.select().where(MedidorTemp.marca == nombre_marca)
        lista_tipos = []

        if lista_medidores_temp:
            return lista_medidores_temp
        else:
            return MedidorTemp.select().execute()

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()


def obtener_todas_marcas_medidor_temp():
    try:
        db = Conexion.db
        db.connect()

        lista_medidores_temp = MedidorTemp.select().execute()

        lista_marcas = []
        for medidortemp in lista_medidores_temp:
            if not [marca for marca in lista_marcas if marca[0] == medidortemp.marca]:
                lista_marcas.append((medidortemp.marca, medidortemp.marca))

        return lista_marcas

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()



def obtener_historial_consumos(numero_medidor):
    try:
        db = Conexion.db
        db.connect()

        historia_consumos = HistorialMedidor.get_or_none(HistorialMedidor.numero_medidor == numero_medidor, HistorialMedidor.tipo == "Consumos")

        if historia_consumos:
            return historia_consumos

        return None

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def obtener_historial_demandas(numero_medidor):
    try:
        db = Conexion.db
        db.connect()

        historial_demandas = HistorialMedidor.get_or_none(HistorialMedidor.numero_medidor == numero_medidor, HistorialMedidor.tipo == "Demandas")

        if historial_demandas:
            return historial_demandas

        return None

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def obtener_historial_reactivos(numero_medidor):
    try:
        db = Conexion.db
        db.connect()

        historial_reactivos = HistorialMedidor.get_or_none(HistorialMedidor.numero_medidor == numero_medidor, HistorialMedidor.tipo == "Reactivos")

        if historial_reactivos:
            return historial_reactivos

        return None

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()