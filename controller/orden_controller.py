from datetime import date
from werkzeug.utils import secure_filename
from controller.gestor_controller import Gestor
from controller.conexion_controller import Conexion
from model.accionanomalia import AccionAnomalia
from model.anomaliaencontrada import AnomaliaEncontrada
from model.asistenteadministrativo import AsistenteAdministrativo
from model.asistentejefe import AsistenteJefe
from model.fotografia import Fotografia
from model.gruporevisor import GrupoRevisor
from model.instalacion import Instalacion
from model.lectura import Lectura
from model.lecturatotal import LecturaTotal
from model.medidor import Medidor
from model.orden import Orden
from model.perfildecarga import PerfilDeCarga
from model.prueba import Prueba
from model.revisor import Revisor
from model.sello import Sello
from model.transformadordedistribucion import TransformadorDeDistribucion
from model.transformadordemedida import TransformadorDeMedida
from model.usoenergiaverificado import UsoEnergiaVerificado
from model.usuario import Usuario
from flask_login import current_user
from model.cliente import Cliente
from model.rdico2 import RDICO2
from model.cliente_instalacion import Cliente_Instalacion
from model.historialrdico2 import HistorialRDICO2
from model.rdico2_anomalia_accion import RDICO2_Anomalia_Accion
from controller import medidor_controller
from controller import instalacion_controller
from flask import flash
import pandas
import simplekml


def obtenerOrdenes():
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()
        lista_ordenes = []

        id_usuario_actual = current_user.id

        grupo_revisor = GrupoRevisor.get_or_none(GrupoRevisor.usuario_id == id_usuario_actual)

        # Validamos que exista grupo revisor
        if grupo_revisor:

            revisor = Revisor.get_or_none(Revisor.grupo_revisor_id == grupo_revisor.id, Revisor.jefeGrupo == 1)

            if revisor:
                ordenes = Orden.select().where(Orden.revisor_id == revisor.id, Orden.estado == "Liberada").execute()

                for orden in ordenes:                          
                    instalacion = Instalacion.get(Instalacion.id == orden.instalacion_id)
                    #cliente_instalacion = Cliente_Instalacion.get(Cliente_Instalacion.instalacion == instalacion.numero)
                    #cliente = Cliente.get(Cliente.identificacion == cliente_instalacion.cliente)
                    orden_temp = OrdenTemp(orden.id, orden.numero, instalacion.numero, instalacion.medidor, orden.fechaEjecucion)
                    lista_ordenes.append(orden_temp)
            else:
                flash('El grupo revisor no tiene asignado un revisor como jefe de grupo', 'advertencia')
        else:
            flash('El usuario actual no esta asignado a un grupo revisor', 'advertencia')

        return lista_ordenes

    except Exception as ex:
        flash('Error recuperando órdenes', 'error')
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

class OrdenTemp:

    def __init__(self, id, numeroOrden, instalacion, medidor, fechaEjecucion):
        self.id = id
        self.numeroOrden = numeroOrden
        self.instalacion = instalacion
        self.medidor = medidor
        self.fechaEjecucion = fechaEjecucion

def obtenerOrdenesMapa():
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()
        lista_ordenes = []

        id_usuario_actual = current_user.id

        grupo_revisor = GrupoRevisor.get_or_none(GrupoRevisor.usuario_id == id_usuario_actual)

        # Validamos que exista grupo revisor
        if grupo_revisor:

            revisor = Revisor.get_or_none(Revisor.grupo_revisor_id == grupo_revisor.id, Revisor.jefeGrupo == 1)

            if revisor:
                ordenes = Orden.select().where(Orden.revisor_id == revisor.id).execute()

                for orden in ordenes:
                    # validamos que este en estado libreada
                    if orden.estado == "Liberada":                            
                        lista_ordenes.append(orden)
            else:
                flash('El grupo revisor no tiene asignado un revisor como jefe de grupo', 'advertencia')
        else:
            flash('El usuario actual no esta asignado a un grupo revisor', 'advertencia')

        return lista_ordenes

    except Exception as ex:
        flash('Error recuperando órdenes', 'error')
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()


def obtenerClientes(ordenes):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        listaClientes = []

        for orden in ordenes:
            xcliente = Cliente.get_or_none(id=orden.idCliente_id)
            if xcliente:
                orden.cliente = xcliente
        db.close()

        return ordenes

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)


def obtener_orden(numero_orden):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        orden = Orden.get_or_none(Orden.numero == numero_orden)

        if orden:
            return orden
        return None

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()


def cargar_choices_caracteristicas():
    try:
        g = Gestor()
        rutaCatastrosCaracteristicas = g.rutaCatastros + "caracteristicas.csv"
        columnasArchivoMarcasMedidores = ["MULTIPLICADOR", "REGISTROS", "MARCA TCS", "MARCA TPS", "MARCA TRAFO COMBINADO DE MEDIDA", 
        "MARCA TRAFO DSITRIBUCION", "TIP. TRAFO", "TIPO SELLO", "UBICACIÓN", "ESTADO", "Func. Del sist. De medición:"]
        valoresVaciosLlenar = {'MULTIPLICADOR': '', 'REGISTROS': '', 'MARCA TCS': '', 'MARCA TPS': '', 'MARCA TRAFO COMBINADO DE MEDIDA': '',
                               'MARCA TRAFO DSITRIBUCION': '', 'TIP. TRAFO': '', 'TIPO SELLO': '', 'UBICACIÓN': '', 'ESTADO': '', 'Func. Del sist. De medición:': ''}
        dfCaracteristicas = pandas.read_csv(rutaCatastrosCaracteristicas, usecols=columnasArchivoMarcasMedidores,
                                            sep=';', encoding='latin-1', dtype={"MULTIPLICADOR": "string",
                                                                                "REGISTROS": "string",
                                                                                "MARCA TCS": "string",
                                                                                "MARCA TPS": "string",
                                                                                "MARCA TRAFO COMBINADO DE MEDIDA": "string",
                                                                                "MARCA TRAFO DSITRIBUCION": "string",
                                                                                "TIP. TRAFO": "string",
                                                                                "TIPO SELLO": "string",
                                                                                "UBICACIÓN": "string",
                                                                                "ESTADO": "string",
                                                                                "Func. Del sist. De medición:": "string"
                                                                                }). fillna(value=valoresVaciosLlenar)
        df_historial = dfCaracteristicas.to_dict('records')
        
        historial_choices = {}
        lista_multiplicadores_parametrizacion_choices = []
        lista_registros_parametrizacion_choices = []
        lista_marcas_tc_transformadores_medida_choices = []
        lista_marcas_tp_transformadores_medida_choices = []
        lista_marcas_tcstps_transformadores_medida_choices = []
        lista_marcas_transformadores_distribucion_choices = []
        lista_tipos_transformadores_distribucion_choices = []
        lista_tipos_sellos_choices = []
        lista_ubicacion_sellos_choices = []
        lista_estado_sellos_choices = []
        lista_funcionamiento_resultados_choices = []

        for row in df_historial:

            if row['MULTIPLICADOR'] != "":
                lista_multiplicadores_parametrizacion_choices.append(row["MULTIPLICADOR"])
            if row['REGISTROS'] != "":
                lista_registros_parametrizacion_choices.append(row["REGISTROS"])
            if row['MARCA TCS'] != "":
                lista_marcas_tc_transformadores_medida_choices.append(row["MARCA TCS"])
            if row['MARCA TPS'] != "":
                lista_marcas_tp_transformadores_medida_choices.append(row["MARCA TPS"])
            if row['MARCA TRAFO COMBINADO DE MEDIDA'] != "":
                lista_marcas_tcstps_transformadores_medida_choices.append(row["MARCA TRAFO COMBINADO DE MEDIDA"])
            if row['MARCA TRAFO DSITRIBUCION'] != "":
                lista_marcas_transformadores_distribucion_choices.append(row["MARCA TRAFO DSITRIBUCION"])
            if row['TIP. TRAFO'] != "":
                lista_tipos_transformadores_distribucion_choices.append(row["TIP. TRAFO"])
            if row['TIPO SELLO'] != "":
                lista_tipos_sellos_choices.append(row["TIPO SELLO"])
            if row['UBICACIÓN'] != "":
                lista_ubicacion_sellos_choices.append(row["UBICACIÓN"])
            if row['ESTADO'] != "":
                lista_estado_sellos_choices.append(row["ESTADO"])
            if row['Func. Del sist. De medición:'] != "":
                lista_funcionamiento_resultados_choices.append(row["Func. Del sist. De medición:"])            

        historial_choices['multiplicador'] = lista_multiplicadores_parametrizacion_choices
        historial_choices['registros'] = lista_registros_parametrizacion_choices
        historial_choices['marcatc'] = lista_marcas_tc_transformadores_medida_choices
        historial_choices['marcatp'] = lista_marcas_tp_transformadores_medida_choices
        historial_choices['marcatcstps'] = lista_marcas_tcstps_transformadores_medida_choices
        historial_choices['marcatransdis'] = lista_marcas_transformadores_distribucion_choices
        historial_choices['tipotransdis'] = lista_tipos_transformadores_distribucion_choices
        historial_choices['tiposello'] = lista_tipos_sellos_choices
        historial_choices['ubicacionsello'] = lista_ubicacion_sellos_choices
        historial_choices['estadosello'] = lista_estado_sellos_choices
        historial_choices['funcionamientoresultados'] = lista_funcionamiento_resultados_choices

        return historial_choices

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)


def usuarios_choices():
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        usuarios = Usuario.select().execute()

        choices = []

        for usuario in usuarios:
            choices.append((usuario.usuario, usuario.usuario))

        return choices

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def anomalias_choices(numero_orden):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        choices = []

        orden = Orden.get_or_none(Orden.numero == numero_orden)

        if orden:
            id_rdico2 = orden.rdico2_id
            rdico2 = RDICO2.get_or_none(RDICO2.id == id_rdico2)

            if rdico2:
                anomalias = rdico2.anomaliasEncontradas
                for anomalia in anomalias:
                    choices.append(anomalia)

        return choices

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()
      

def usos_energia_choices(numero_orden):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        choices = []

        orden = Orden.get_or_none(Orden.numero == numero_orden)

        if orden:
            id_rdico2 = orden.rdico2_id
            rdico2 = RDICO2.get_or_none(RDICO2.id == id_rdico2)

            if rdico2:
                usosEnergiaVerificado = rdico2.usosEnergiaVerificado
                for uso in usosEnergiaVerificado:
                    choices.append(uso)

        return choices

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def obtener_anomalia(id_anomalia):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        anomalia = AnomaliaEncontrada.get_or_none(AnomaliaEncontrada.id == id_anomalia)

        if anomalia:
            return anomalia

        return None

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()    

def obtener_anomalia_id(id_anomalia):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        anomalia = AnomaliaEncontrada.get_or_none(AnomaliaEncontrada.id == id_anomalia)

        if anomalia:
            return anomalia

        return None

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()   

def obtener_uso(id_uso):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        uso = UsoEnergiaVerificado.get_or_none(UsoEnergiaVerificado.id == id_uso)

        if uso:
            return uso

        return None

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()   

def obtener_accion(id_accion):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        accion = AccionAnomalia.get_or_none(AccionAnomalia.id == id_accion)

        if accion:
            return accion

        return None

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()  

def anadir_uso_energia(numero_orden, uso_energia):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        if uso_energia.descripcion == "":
            flash('Debe ingresar una descripción del uso de la energía', 'error')
            return False

        orden = Orden.get_or_none(Orden.numero == numero_orden)

        if orden:
            rdico2 = RDICO2.get_or_none(RDICO2.id == orden.rdico2_id)
            uso_energia.save()
            uso_energia.rdico2.add(rdico2)
            return True

        return False

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def obtener_texto_grupo_revisor(numero_orden):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        texto_grupo_revisor = ""

        orden = Orden.get_or_none(Orden.numero == numero_orden)

        if orden:
            revisor = Revisor.get_or_none(Revisor.id == orden.revisor_id)

            grupo_revisor = GrupoRevisor.get_or_none(GrupoRevisor.id == revisor.grupo_revisor_id)

            if grupo_revisor:

                revisores = Revisor.select().where(Revisor.grupo_revisor_id == grupo_revisor.id)

                texto_grupo_revisor += "-"+grupo_revisor.nombre+"-"

                for r in revisores:
                    texto_grupo_revisor += r.razonSocial +"-" 

        return texto_grupo_revisor

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()


def anadir_caracteristica(modulo, tipo_caracteristica, texto_caracteristica):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        if texto_caracteristica == "":
            flash('Característica vacía','error')
            return False

        rutaCatastrosCaracteristicas = g.rutaCatastros + "caracteristicas.csv"
        columnasArchivoMarcasMedidores = ["MULTIPLICADOR", "REGISTROS", "MARCA TCS", "MARCA TPS", "MARCA TRAFO COMBINADO DE MEDIDA", 
        "MARCA TRAFO DSITRIBUCION", "TIP. TRAFO", "TIPO SELLO", "UBICACIÓN", "ESTADO", "Func. Del sist. De medición:"]
        valoresVaciosLlenar = {'MULTIPLICADOR': '', 'REGISTROS': '', 'MARCA TCS': '', 'MARCA TPS': '', 'MARCA TRAFO COMBINADO DE MEDIDA': '',
                               'MARCA TRAFO DSITRIBUCION': '', 'TIP. TRAFO': '', 'TIPO SELLO': '', 'UBICACIÓN': '', 'ESTADO': '', 'Func. Del sist. De medición:': ''}
        dfCaracteristicas = pandas.read_csv(rutaCatastrosCaracteristicas, usecols=columnasArchivoMarcasMedidores,
                                            sep=';', encoding='latin-1', dtype={"MULTIPLICADOR": "string",
                                                                                "REGISTROS": "string",
                                                                                "MARCA TCS": "string",
                                                                                "MARCA TPS": "string",
                                                                                "MARCA TRAFO COMBINADO DE MEDIDA": "string",
                                                                                "MARCA TRAFO DSITRIBUCION": "string",
                                                                                "TIP. TRAFO": "string",
                                                                                "TIPO SELLO": "string",
                                                                                "UBICACIÓN": "string",
                                                                                "ESTADO": "string",
                                                                                "Func. Del sist. De medición:": "string"
                                                                                }). fillna(value=valoresVaciosLlenar)
    
        df_empty = pandas.DataFrame({'MULTIPLICADOR': [''], 'REGISTROS': [''], 'MARCA TCS': [''], 'MARCA TPS': [''], 'MARCA TRAFO COMBINADO DE MEDIDA': [''],
                               'MARCA TRAFO DSITRIBUCION': [''], 'TIP. TRAFO': [''], 'TIPO SELLO': [''], 'UBICACIÓN': [''], 'ESTADO': [''], 'Func. Del sist. De medición:': ['']}) 
        if modulo == "parametrizacion":
            if tipo_caracteristica == "Multiplicador":
                df_empty['MULTIPLICADOR'] = texto_caracteristica
                df = pandas.concat([dfCaracteristicas, df_empty], ignore_index = True, axis = 0)
            if tipo_caracteristica == "Registros":
                df_empty['REGISTROS'] = texto_caracteristica
                df = pandas.concat([dfCaracteristicas, df_empty], ignore_index = True, axis = 0)

        if modulo == "transformador_medida":
            if tipo_caracteristica == "Marca TC":
                df_empty['MARCA TCS'] = texto_caracteristica
                df = pandas.concat([dfCaracteristicas, df_empty], ignore_index = True, axis = 0)
            if tipo_caracteristica == "Marca TP":
                df_empty['MARCA TPS'] = texto_caracteristica
                df = pandas.concat([dfCaracteristicas, df_empty], ignore_index = True, axis = 0)
            if tipo_caracteristica == "Marca TCS/TPS":
                df_empty['MARCA TRAFO COMBINADO DE MEDIDA'] = texto_caracteristica
                df = pandas.concat([dfCaracteristicas, df_empty], ignore_index = True, axis = 0)
            
        if modulo == "transformador_distribucion":
            if tipo_caracteristica == "Marca":
                df_empty['MARCA TRAFO DSITRIBUCION'] = texto_caracteristica
                df = pandas.concat([dfCaracteristicas, df_empty], ignore_index = True, axis = 0)
            if tipo_caracteristica == "Tipo":
                df_empty['TIP. TRAFO'] = texto_caracteristica
                df = pandas.concat([dfCaracteristicas, df_empty], ignore_index = True, axis = 0)

        if modulo == "sello":
            if tipo_caracteristica == "Tipo":
                df_empty['TIPO SELLO'] = texto_caracteristica
                df = pandas.concat([dfCaracteristicas, df_empty], ignore_index = True, axis = 0)
            if tipo_caracteristica == "Ubicación":
                df_empty['UBICACIÓN'] = texto_caracteristica
                df = pandas.concat([dfCaracteristicas, df_empty], ignore_index = True, axis = 0)
            if tipo_caracteristica == "Estado":
                df_empty['ESTADO'] = texto_caracteristica
                df = pandas.concat([dfCaracteristicas, df_empty], ignore_index = True, axis = 0)

        df.to_csv(rutaCatastrosCaracteristicas, sep=";", encoding='latin-1', index=False)
        return True


    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def obtener_meses_ordenados(historial):

    lista_tuplas_meses = []

    today = date.today()
    mes = today.month

    mes_anterior = mes -1
    if mes_anterior == 0:
        mes_anterior = 12

    if historial:
        if mes_anterior == 1:
            lista_tuplas_meses.append(('enero', historial.mes1))
            lista_tuplas_meses.append(('febrero', historial.mes12))
            lista_tuplas_meses.append(('marzo', historial.mes11))
            lista_tuplas_meses.append(('abril', historial.mes10))
            lista_tuplas_meses.append(('mayo', historial.mes9))
            lista_tuplas_meses.append(('junio', historial.mes8))
            lista_tuplas_meses.append(('julio', historial.mes7))
            lista_tuplas_meses.append(('agosto', historial.mes6))
            lista_tuplas_meses.append(('septiembre', historial.mes5))
            lista_tuplas_meses.append(('octubre', historial.mes4))
            lista_tuplas_meses.append(('noviembre', historial.mes3))
            lista_tuplas_meses.append(('diciembre', historial.mes2))
        elif mes_anterior == 2:
            lista_tuplas_meses.append(('enero', historial.mes2))
            lista_tuplas_meses.append(('febrero', historial.mes1))
            lista_tuplas_meses.append(('marzo', historial.mes12))
            lista_tuplas_meses.append(('abril', historial.mes11))
            lista_tuplas_meses.append(('mayo', historial.mes10))
            lista_tuplas_meses.append(('junio', historial.mes9))
            lista_tuplas_meses.append(('julio', historial.mes8))
            lista_tuplas_meses.append(('agosto', historial.mes7))
            lista_tuplas_meses.append(('septiembre', historial.mes6))
            lista_tuplas_meses.append(('octubre', historial.mes5))
            lista_tuplas_meses.append(('noviembre', historial.mes4))
            lista_tuplas_meses.append(('diciembre', historial.mes3))
        elif mes_anterior == 3:
            lista_tuplas_meses.append(('enero', historial.mes3))
            lista_tuplas_meses.append(('febrero', historial.mes2))
            lista_tuplas_meses.append(('marzo', historial.mes1))
            lista_tuplas_meses.append(('abril', historial.mes12))
            lista_tuplas_meses.append(('mayo', historial.mes11))
            lista_tuplas_meses.append(('junio', historial.mes10))
            lista_tuplas_meses.append(('julio', historial.mes9))
            lista_tuplas_meses.append(('agosto', historial.mes8))
            lista_tuplas_meses.append(('septiembre', historial.mes7))
            lista_tuplas_meses.append(('octubre', historial.mes6))
            lista_tuplas_meses.append(('noviembre', historial.mes5))
            lista_tuplas_meses.append(('diciembre', historial.mes4))
        elif mes_anterior == 4:
            lista_tuplas_meses.append(('enero', historial.mes4))
            lista_tuplas_meses.append(('febrero', historial.mes3))
            lista_tuplas_meses.append(('marzo', historial.mes2))
            lista_tuplas_meses.append(('abril', historial.mes1))
            lista_tuplas_meses.append(('mayo', historial.mes12))
            lista_tuplas_meses.append(('junio', historial.mes11))
            lista_tuplas_meses.append(('julio', historial.mes10))
            lista_tuplas_meses.append(('agosto', historial.mes9))
            lista_tuplas_meses.append(('septiembre', historial.mes8))
            lista_tuplas_meses.append(('octubre', historial.mes7))
            lista_tuplas_meses.append(('noviembre', historial.mes6))
            lista_tuplas_meses.append(('diciembre', historial.mes5))
        elif mes_anterior == 5:
            lista_tuplas_meses.append(('enero', historial.mes5))
            lista_tuplas_meses.append(('febrero', historial.mes4))
            lista_tuplas_meses.append(('marzo', historial.mes3))
            lista_tuplas_meses.append(('abril', historial.mes2))
            lista_tuplas_meses.append(('mayo', historial.mes1))
            lista_tuplas_meses.append(('junio', historial.mes12))
            lista_tuplas_meses.append(('julio', historial.mes11))
            lista_tuplas_meses.append(('agosto', historial.mes10))
            lista_tuplas_meses.append(('septiembre', historial.mes9))
            lista_tuplas_meses.append(('octubre', historial.mes8))
            lista_tuplas_meses.append(('noviembre', historial.mes7))
            lista_tuplas_meses.append(('diciembre', historial.mes6)) 
        elif mes_anterior == 6:
            lista_tuplas_meses.append(('enero', historial.mes6))
            lista_tuplas_meses.append(('febrero', historial.mes5))
            lista_tuplas_meses.append(('marzo', historial.mes4))
            lista_tuplas_meses.append(('abril', historial.mes3))
            lista_tuplas_meses.append(('mayo', historial.mes2))
            lista_tuplas_meses.append(('junio', historial.mes1))
            lista_tuplas_meses.append(('julio', historial.mes12))
            lista_tuplas_meses.append(('agosto', historial.mes11))
            lista_tuplas_meses.append(('septiembre', historial.mes10))
            lista_tuplas_meses.append(('octubre', historial.mes9))
            lista_tuplas_meses.append(('noviembre', historial.mes8))
            lista_tuplas_meses.append(('diciembre', historial.mes7)) 
        elif mes_anterior == 7:
            lista_tuplas_meses.append(('enero', historial.mes7))
            lista_tuplas_meses.append(('febrero', historial.mes6))
            lista_tuplas_meses.append(('marzo', historial.mes5))
            lista_tuplas_meses.append(('abril', historial.mes4))
            lista_tuplas_meses.append(('mayo', historial.mes3))
            lista_tuplas_meses.append(('junio', historial.mes2))
            lista_tuplas_meses.append(('julio', historial.mes1))
            lista_tuplas_meses.append(('agosto', historial.mes12))
            lista_tuplas_meses.append(('septiembre', historial.mes11))
            lista_tuplas_meses.append(('octubre', historial.mes10))
            lista_tuplas_meses.append(('noviembre', historial.mes9))
            lista_tuplas_meses.append(('diciembre', historial.mes8)) 
        elif mes_anterior == 8:
            lista_tuplas_meses.append(('enero', historial.mes8))
            lista_tuplas_meses.append(('febrero', historial.mes7))
            lista_tuplas_meses.append(('marzo', historial.mes6))
            lista_tuplas_meses.append(('abril', historial.mes5))
            lista_tuplas_meses.append(('mayo', historial.mes4))
            lista_tuplas_meses.append(('junio', historial.mes3))
            lista_tuplas_meses.append(('julio', historial.mes2))
            lista_tuplas_meses.append(('agosto', historial.mes1))
            lista_tuplas_meses.append(('septiembre', historial.mes12))
            lista_tuplas_meses.append(('octubre', historial.mes11))
            lista_tuplas_meses.append(('noviembre', historial.mes10))
            lista_tuplas_meses.append(('diciembre', historial.mes9))
        elif mes_anterior == 9:
            lista_tuplas_meses.append(('enero', historial.mes9))
            lista_tuplas_meses.append(('febrero', historial.mes8))
            lista_tuplas_meses.append(('marzo', historial.mes7))
            lista_tuplas_meses.append(('abril', historial.mes6))
            lista_tuplas_meses.append(('mayo', historial.mes5))
            lista_tuplas_meses.append(('junio', historial.mes4))
            lista_tuplas_meses.append(('julio', historial.mes3))
            lista_tuplas_meses.append(('agosto', historial.mes2))
            lista_tuplas_meses.append(('septiembre', historial.mes1))
            lista_tuplas_meses.append(('octubre', historial.mes12))
            lista_tuplas_meses.append(('noviembre', historial.mes11))
            lista_tuplas_meses.append(('diciembre', historial.mes10))
        elif mes_anterior == 10:
            lista_tuplas_meses.append(('enero', historial.mes10))
            lista_tuplas_meses.append(('febrero', historial.mes9))
            lista_tuplas_meses.append(('marzo', historial.mes8))
            lista_tuplas_meses.append(('abril', historial.mes7))
            lista_tuplas_meses.append(('mayo', historial.mes6))
            lista_tuplas_meses.append(('junio', historial.mes5))
            lista_tuplas_meses.append(('julio', historial.mes4))
            lista_tuplas_meses.append(('agosto', historial.mes3))
            lista_tuplas_meses.append(('septiembre', historial.mes2))
            lista_tuplas_meses.append(('octubre', historial.mes1))
            lista_tuplas_meses.append(('noviembre', historial.mes12))
            lista_tuplas_meses.append(('diciembre', historial.mes11))
        elif mes_anterior == 11:
            lista_tuplas_meses.append(('enero', historial.mes11))
            lista_tuplas_meses.append(('febrero', historial.mes10))
            lista_tuplas_meses.append(('marzo', historial.mes9))
            lista_tuplas_meses.append(('abril', historial.mes8))
            lista_tuplas_meses.append(('mayo', historial.mes7))
            lista_tuplas_meses.append(('junio', historial.mes6))
            lista_tuplas_meses.append(('julio', historial.mes5))
            lista_tuplas_meses.append(('agosto', historial.mes4))
            lista_tuplas_meses.append(('septiembre', historial.mes3))
            lista_tuplas_meses.append(('octubre', historial.mes2))
            lista_tuplas_meses.append(('noviembre', historial.mes1))
            lista_tuplas_meses.append(('diciembre', historial.mes12))
        elif mes_anterior == 12:
            lista_tuplas_meses.append(('enero', historial.mes12))
            lista_tuplas_meses.append(('febrero', historial.mes11))
            lista_tuplas_meses.append(('marzo', historial.mes10))
            lista_tuplas_meses.append(('abril', historial.mes9))
            lista_tuplas_meses.append(('mayo', historial.mes8))
            lista_tuplas_meses.append(('junio', historial.mes7))
            lista_tuplas_meses.append(('julio', historial.mes6))
            lista_tuplas_meses.append(('agosto', historial.mes5))
            lista_tuplas_meses.append(('septiembre', historial.mes4))
            lista_tuplas_meses.append(('octubre', historial.mes3))
            lista_tuplas_meses.append(('noviembre', historial.mes2))
            lista_tuplas_meses.append(('diciembre', historial.mes1))

    return lista_tuplas_meses

def obtener_anomalias_acciones_agregadas(rdico2):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        lista_anomalias_acciones = []

        rdico2_anomalia_acciones = RDICO2_Anomalia_Accion.select().where(RDICO2_Anomalia_Accion.rdico2_id == rdico2.id)

        for rdico2_anomalia_accion in rdico2_anomalia_acciones:
            raa_temp = RDICO2AnomaliaAccionTemp(rdico2_anomalia_accion.id, rdico2_anomalia_accion.rdico2_id, rdico2_anomalia_accion.anomalia_id, rdico2_anomalia_accion.accion_id, rdico2_anomalia_accion.accion.descripcion)
            lista_anomalias_acciones.append(raa_temp)

        return lista_anomalias_acciones

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

class RDICO2AnomaliaAccionTemp:
    def __init__(self, id, rdico2_id, anomalia_id, accion_id, accion_descripcion):
        self.id = id
        self.rdico2_id = rdico2_id
        self.anomalia_id = anomalia_id
        self.accion_id = accion_id
        self.accion_descripcion = accion_descripcion

def obtener_usos():
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        usos = UsoEnergiaVerificado.select().execute()

        lista_usos = []

        for uso in usos:
            lista_usos.append((uso.id, uso.descripcion))

        return lista_usos

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def obtener_anomalias_choices():
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        anomalias = AnomaliaEncontrada.select().execute()

        lista_anomalias = []

        for anomalia in anomalias:
            lista_anomalias.append((anomalia.id, anomalia.descripcion))

        return lista_anomalias

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()


def obtener_acciones():
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        acciones = AccionAnomalia.select().execute()

        lista_acciones = []

        for accion in acciones:
            lista_acciones.append((accion.id, accion.descripcion))

        return lista_acciones

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def anadir_faltante_resultados(tipo_caracteristica, texto_caracteristica):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        if texto_caracteristica == "":
            flash('Es necesario ingresar el nombre de la característica faltante','error')
            return False

        if tipo_caracteristica == "Anomalía":
            anomalia = AnomaliaEncontrada(descripcion=texto_caracteristica)
            anomalia.save()
            return True
        else:
            uso = UsoEnergiaVerificado(descripcion=texto_caracteristica)
            uso.save()
            return True
        return False

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def anadir_faltante_rdico5(tipo_caracteristica, texto_caracteristica):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        if texto_caracteristica == "":
            flash('Es necesario ingresar el nombre de la característica faltante','error')
            return False

        if tipo_caracteristica == "Acción":
            accion = AccionAnomalia(descripcion=texto_caracteristica)
            accion.save()
            return True
        return False

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()
    

def guardar_instalacion(instalacion):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        contacto_tecnico = instalacion.contacto_tecnico

        if contacto_tecnico:
            contacto_tecnico.save()
        
        instalacion.save()

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def guardar_cambio_material(cambio_material, rdico5):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        cambio_material.save()

        rdico5.cambio_material = cambio_material
        rdico5.save()

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def guardar_parametrizacion(parametrizacion, rdico2):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()
        
        parametrizacion.save()
        rdico2.parametrizacion = parametrizacion
        rdico2.save()

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def guardar_verificacion(verificacion, rdico2):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()
        
        verificacion.save()
        rdico2.verificacion = verificacion
        rdico2.save()

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def guardar_transformadores_medida(transformadores_medida, rdico2):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()
        
        for transformador in transformadores_medida:
            transformador.save()
            if not transformador in rdico2.transformadoresDeMedida:
                rdico2.transformadoresDeMedida.add(transformador)
        rdico2.save()

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def guardar_transformadores_distribucion(transformadores_distribucion, rdico2):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()
        
        for transformador in transformadores_distribucion:
            transformador.save()
            if not transformador in rdico2.transformadoresDeDistribucion:
                rdico2.transformadoresDeDistribucion.add(transformador)
        rdico2.save()

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def guardar_prueba(pruebas, rdico2):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()
        
        for prueba in pruebas:
            prueba.save()
            if not prueba in rdico2.pruebas:
                rdico2.pruebas.add(prueba)
        rdico2.save()

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def guardar_sello(sellos, rdico2):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()
        
        for sello in sellos:
            sello.save()
            if not sello in rdico2.sellos:
                rdico2.sellos.add(sello)
        rdico2.save()

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()   

def guardar_uso(usos, rdico2):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()
        
        for uso in usos:
            uso.save()
            if uso not in rdico2.usosEnergiaVerificado:
                rdico2.usosEnergiaVerificado.add(uso)
        rdico2.save()

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()  

def guardar_anomalia(anomalias, rdico2):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()
        
        for anomalia in anomalias:
            if anomalia not in rdico2.anomalias:
                rdico2.anomalias.add(anomalia)
        rdico2.save()

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close() 

def guardar_rdico2(rdico2):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()
        
        if rdico2:
            rdico2.save()

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close() 

def guardar_rdico5(rdico5):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()
        
        if rdico5:
            rdico5.save()

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close() 

def agregar_anomalia_resultados(rdico2, anomalia):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        if anomalia not in rdico2.anomalias:
            rdico2.anomalias.add(anomalia)  
            rdico2.save()

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close() 


def guardar_lectura(lecturas, rdico2):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()
        
        for lectura in lecturas:
            lectura.save()
            if not lectura in rdico2.lecturas:
                rdico2.lecturas.add(lectura)
        rdico2.save()

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()     


def guardar_orden(orden):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        if orden:      
            orden.save()

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def obtener_asistente_actual():
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        id_usuario_actual = current_user.id
        asistente_jefe = AsistenteJefe.get_or_none(AsistenteJefe.usuario_id == id_usuario_actual)

        if asistente_jefe:
            return asistente_jefe

        asistente_administrativo = AsistenteAdministrativo.get_or_none(AsistenteAdministrativo.usuario_id == id_usuario_actual)
        if asistente_administrativo:
            return asistente_administrativo

        return None

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def guardar_medidor(medidor, rdico2):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        if medidor:

            db.close()
            historial_consumos = medidor_controller.obtener_historial_consumos(medidor.numero)
            historial_demandas = medidor_controller.obtener_historial_demandas(medidor.numero)
            historial_reactivos = medidor_controller.obtener_historial_reactivos(medidor.numero)

            if historial_consumos:
                historial_consumos_rdico2 = HistorialRDICO2(mes1 = historial_consumos.mes1,
                mes2 = historial_consumos.mes2, mes3 = historial_consumos.mes3, mes4 = historial_consumos.mes4,
                mes5 = historial_consumos.mes5, mes6 = historial_consumos.mes6, mes7 = historial_consumos.mes7,
                mes8 = historial_consumos.mes8, mes9 = historial_consumos.mes9, mes10 = historial_consumos.mes10,
                mes11 = historial_consumos.mes11, mes12 = historial_consumos.mes12, tipo="Consumos")
                rdico2.historiales.add(historial_consumos_rdico2)

            if historial_demandas:
                historial_demandas_rdico2 = HistorialRDICO2(mes1 = historial_demandas.mes1,
                mes2 = historial_demandas.mes2, mes3 = historial_demandas.mes3, mes4 = historial_demandas.mes4,
                mes5 = historial_demandas.mes5, mes6 = historial_demandas.mes6, mes7 = historial_demandas.mes7,
                mes8 = historial_demandas.mes8, mes9 = historial_demandas.mes9, mes10 = historial_demandas.mes10,
                mes11 = historial_demandas.mes11, mes12 = historial_demandas.mes12, tipo="Demandas")
                rdico2.historiales.add(historial_demandas_rdico2)
            
            if historial_reactivos:
                historial_reactivos_rdico2 = HistorialRDICO2(mes1 = historial_reactivos.mes1,
                mes2 = historial_reactivos.mes2, mes3 = historial_reactivos.mes3, mes4 = historial_reactivos.mes4,
                mes5 = historial_reactivos.mes5, mes6 = historial_reactivos.mes6, mes7 = historial_reactivos.mes7,
                mes8 = historial_reactivos.mes8, mes9 = historial_reactivos.mes9, mes10 = historial_reactivos.mes10,
                mes11 = historial_reactivos.mes11, mes12 = historial_reactivos.mes12, tipo="Reactivos")
                rdico2.historiales.add(historial_reactivos_rdico2)
            
            db.connect()
            medidor.save()

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def obtener_rdico2(orden):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        rdico2 = orden.rdico2

        if rdico2:
            return rdico2

        return None

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def obtener_rdico5(orden):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        rdico5 = orden.rdico5

        if rdico5:
            return rdico5

        return None

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def obtener_parametrizacion(rdico2):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        parametrizacion = rdico2.parametrizacion

        if parametrizacion:
            return parametrizacion

        return None

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def obtener_verificacion(rdico2):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        verificacion = rdico2.verificacion

        if verificacion:
            return verificacion

        return None

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def obtener_cambio_material(rdico5):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        cambio_material = rdico5.cambio_material

        if cambio_material:
            return cambio_material

        return None

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def cambio_material(rdico5):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        cambio_material = rdico5.cambio_material

        if cambio_material:
            return cambio_material

        return None

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def obtener_contacto_tecnico(instalacion):
    try:
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

def obtener_bandera_tipo_asistente_rdico5():
    try:
        db = Conexion.db
        db.connect()

        id_usuario_actual = current_user.id

        asistente_administrativo = AsistenteAdministrativo.get_or_none(AsistenteAdministrativo.usuario_id == id_usuario_actual)

        if asistente_administrativo:
            return True
        return False

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def generar_kml(ordenes):
    try:
        db = Conexion.db
        db.connect()

        kml = simplekml.Kml()

        schema = kml.newschema(name='Coordenadas')
        schema.newsimplefield(name="Name", type="string")
        schema.newsimplefield(name="Description", type="string")
        schema.newsimplefield(name="Coord. X (UTM)", type="float")
        schema.newsimplefield(name="Coord. Y (UTM)", type="float")

        document = kml.newfolder(name='Coordenadas')
        
        for orden in ordenes:
            instalacion = Instalacion.get_or_none(Instalacion.numero == orden.instalacion)
            medidor = Medidor.get_or_none(Medidor.numero == instalacion.medidor)

            if instalacion and medidor:
                point = document.newpoint(name=orden.numeroOrden, description=orden.medidor, coords=[(instalacion.coordenadaX,instalacion.coordenadaY)])
                extenddata = point.extendeddata
                schemdata = extenddata.schemadata
                schemdata.schemaurl = "Coordenadas"
                schemdata.newsimpledata(name="Coord. X (UTM)", value=instalacion.utmX)
                schemdata.newsimpledata(name="Coord. Y (UTM)", value=instalacion.utmY)

        fecha_actual = date.today()
        path = "kml/coordenadas_"+str(fecha_actual)+".kml"
        kml.save(path)
        flash('Archivo kml creado correctamente en '+path,'exito')

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def crear_transformador_medida(transformador, rdico2):
    try:
        db = Conexion.db
        db.connect()

        transformador.save()
        rdico2.transformadoresDeMedida.add(transformador)
        rdico2.save()

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def eliminar_transformador_medida(id_transformador, rdico2):
    try:
        db = Conexion.db
        db.connect()

        transformador = TransformadorDeMedida.get_or_none(TransformadorDeMedida.id == id_transformador)

        if transformador and transformador in rdico2.transformadoresDeMedida:
            rdico2.transformadoresDeMedida.remove(transformador)
            transformador.delete_instance()
            rdico2.save()

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def obtener_transformadores_medida(rdico2):
    try:
        db = Conexion.db
        db.connect()

        transformadores_medida = []

        for transformador in rdico2.transformadoresDeMedida:
            transformadores_medida.append(transformador)

        return transformadores_medida

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def crear_transformador_distribucion(transformador, rdico2):
    try:
        db = Conexion.db
        db.connect()

        transformador.save()
        rdico2.transformadoresDeDistribucion.add(transformador)
        rdico2.save()

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def eliminar_transformador_distribucion(id_transformador, rdico2):
    try:
        db = Conexion.db
        db.connect()

        transformador = TransformadorDeDistribucion.get_or_none(TransformadorDeDistribucion.id == id_transformador)

        if transformador and transformador in rdico2.transformadoresDeDistribucion:
            rdico2.transformadoresDeDistribucion.remove(transformador)
            transformador.delete_instance()
            rdico2.save()

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def obtener_transformadores_distribucion(rdico2):
    try:
        db = Conexion.db
        db.connect()

        transformadores_distribucion = []

        for transformador in rdico2.transformadoresDeDistribucion:
            transformadores_distribucion.append(transformador)

        return transformadores_distribucion

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def crear_prueba(prueba, rdico2):
    try:
        db = Conexion.db
        db.connect()

        prueba.save()
        rdico2.pruebas.add(prueba)
        rdico2.save()

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def eliminar_prueba(id_prueba, rdico2):
    try:
        db = Conexion.db
        db.connect()

        prueba = Prueba.get_or_none(Prueba.id == id_prueba)

        if prueba and prueba in rdico2.pruebas:
            rdico2.pruebas.remove(prueba)
            prueba.delete_instance()
            rdico2.save()

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def obtener_pruebas(rdico2):
    try:
        db = Conexion.db
        db.connect()

        pruebas = []

        for prueba in rdico2.pruebas:
            pruebas.append(prueba)

        return pruebas

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def crear_sello(sello, rdico2):
    try:
        db = Conexion.db
        db.connect()

        sello.save()
        rdico2.sellos.add(sello)
        rdico2.save()

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def eliminar_sello(id_sello, rdico2):
    try:
        db = Conexion.db
        db.connect()

        sello = Sello.get_or_none(Sello.id == id_sello)

        if sello and sello in rdico2.sellos:
            rdico2.sellos.remove(sello)
            sello.delete_instance()
            rdico2.save()

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def obtener_sellos(rdico2):
    try:
        db = Conexion.db
        db.connect()

        sellos = []

        for sello in rdico2.sellos:
            sellos.append(sello)

        return sellos

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def crear_lectura(lectura, rdico2):
    try:
        db = Conexion.db
        db.connect()

        lectura.save()
        rdico2.lecturas.add(lectura)
        rdico2.save()

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def eliminar_lectura(id_lectura, rdico2):
    try:
        db = Conexion.db
        db.connect()

        lectura = LecturaTotal.get_or_none(LecturaTotal.id == id_lectura)

        if lectura and lectura in rdico2.lecturas:
            rdico2.lecturas.remove(lectura)
            lectura.delete_instance()
            rdico2.save()

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def obtener_lecturas(rdico2):
    try:
        db = Conexion.db
        db.connect()

        lecturas = []

        for lectura in rdico2.lecturas:
            lecturas.append(lectura)

        return lecturas

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def crear_uso_energia(id_uso, rdico2):
    try:
        db = Conexion.db
        db.connect()

        uso = UsoEnergiaVerificado.get_or_none(UsoEnergiaVerificado.id == id_uso)

        if uso:
            if uso not in rdico2.usosEnergiaVerificado:
                rdico2.usosEnergiaVerificado.add(uso)
                rdico2.save()
            else:
                flash('El uso ya esta agregado', 'error')

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def eliminar_uso_energia(id_uso, rdico2):
    try:
        db = Conexion.db
        db.connect()

        uso = UsoEnergiaVerificado.get_or_none(UsoEnergiaVerificado.id == id_uso)

        if uso and uso in rdico2.usosEnergiaVerificado:
            rdico2.usosEnergiaVerificado.remove(uso)
            rdico2.save()

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def obtener_usos_energia(rdico2):
    try:
        db = Conexion.db
        db.connect()

        usos = []

        for uso in rdico2.usosEnergiaVerificado:
            usos.append(uso)

        return usos

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def crear_anomalia(id_anomalia, rdico2):
    try:
        db = Conexion.db
        db.connect()

        anomalia = AnomaliaEncontrada.get_or_none(AnomaliaEncontrada.id == id_anomalia)

        if anomalia:
            if anomalia not in rdico2.anomalias:
                rdico2.anomalias.add(anomalia)
                rdico2.save()
            else:
                flash('La anomalia ya esta agregado', 'error')

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def eliminar_anomalia(id_anomalia, rdico2):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        anomalia = AnomaliaEncontrada.get_or_none(AnomaliaEncontrada.id == id_anomalia)

        if anomalia and anomalia in rdico2.anomalias:
            rdico2.anomalias.remove(anomalia)
            rdico2.save()
        
        rdico2_anomalia_acciones = RDICO2_Anomalia_Accion.select().where(RDICO2_Anomalia_Accion.rdico2_id == rdico2.id, RDICO2_Anomalia_Accion.anomalia_id == anomalia.id)
        for raa in rdico2_anomalia_acciones:
            raa.delete_instance()

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()


def obtener_anomalias(rdico2):
    try:
        db = Conexion.db
        db.connect()

        anomalias = []

        for anomalia in rdico2.anomalias:
            anomalias.append(anomalia)

        return anomalias

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def crear_accion(rdico2, anomalia, accion):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        id_rdico2 = rdico2.id
        id_anomalia = anomalia.id
        id_accion=accion.id

        rdico2_anomalia_accion = RDICO2_Anomalia_Accion(rdico2_id=id_rdico2, anomalia_id=id_anomalia, accion_id=id_accion)

        rdico2_anomalia_acciones = RDICO2_Anomalia_Accion.select().execute()

        bandera = True
        for raa in rdico2_anomalia_acciones:
            if raa.rdico2_id == id_rdico2 and raa.anomalia_id == id_anomalia and raa.accion_id == int(id_accion):
                bandera = False

        if bandera:
            rdico2_anomalia_accion.save()
        else:
            flash('La accion ya esta agregada','error')

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def eliminar_accion(rdico2, anomalia, accion):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        id_rdico2 = rdico2.id
        id_anomalia = anomalia.id
        id_accion=accion.id

        rdico2_anomalia_accion = RDICO2_Anomalia_Accion.get_or_none(RDICO2_Anomalia_Accion.rdico2_id==rdico2.id, RDICO2_Anomalia_Accion.anomalia_id==id_anomalia, RDICO2_Anomalia_Accion.accion_id==id_accion)

        if rdico2_anomalia_accion:
            rdico2_anomalia_accion.delete_instance()

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def convertir_archivo_a_binario(path):
    bytes = None
    with open(path, "rb") as f:
        bytes = f.read()
    return bytes


def crear_fotografia(fotografia, nombre_archivo, path_imagen, rdico2):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()

        fotografia = Fotografia(nombre_archivo = nombre_archivo, path_imagen = path_imagen)
        fotografia.save()
        rdico2.fotografias.add(fotografia)
        rdico2.save()

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def eliminar_fotografia(id_imagen, rdico2):
    try:
        db = Conexion.db
        db.connect()

        fotografia = Fotografia.get_or_none(Fotografia.id == id_imagen)

        if fotografia and fotografia in rdico2.fotografias:
            rdico2.fotografias.remove(fotografia)
            fotografia.delete_instance()
            rdico2.save()

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def convertir_binario_a_archivo(bytes, path_imagen):
    file = open(path_imagen, "wb")
    file.write(bytes)
    file.close()
    return file

def obtener_fotografias(rdico2):
    try:
        db = Conexion.db
        db.connect()

        fotografias = []

        for fotografia in rdico2.fotografias:
            fotografias.append(fotografia)

        return fotografias

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()


def crear_archivo_lectura(nombre_archivo, path_lectura, rdico2):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()
        
        lectura = Lectura(nombre_archivo = nombre_archivo, path_lectura = path_lectura)
        lectura.save()
        rdico2.lectura = lectura
        rdico2.save()

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def eliminar_archivo_lectura(id_lectura, rdico2):
    try:
        db = Conexion.db
        db.connect()

        lectura = Lectura.get_or_none(Lectura.id == id_lectura)

        if lectura and lectura == rdico2.lectura:
            rdico2.lectura.delete_instance()
            rdico2.save()

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def obtener_archivo_lectura(rdico2):
    try:
        db = Conexion.db
        db.connect()

        lista = []

        if rdico2.lectura:
            lista.append(rdico2.lectura)

        return lista

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def crear_perfil(nombre_archivo, path_perfil, rdico2):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()
        
        perfil = PerfilDeCarga(nombre_archivo = nombre_archivo, path_perfil = path_perfil)
        perfil.save()
        rdico2.perfil_carga = perfil
        rdico2.save()

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def eliminar_perfil(id_perfil, rdico2):
    try:
        db = Conexion.db
        db.connect()

        perfil = PerfilDeCarga.get_or_none(PerfilDeCarga.id == id_perfil)

        if perfil and perfil == rdico2.perfil_carga:
            rdico2.perfil_carga.delete_instance()
            rdico2.save()

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()

def obtener_archivo_perfil(rdico2):
    try:
        db = Conexion.db
        db.connect()

        lista = []

        if rdico2.perfil_carga:
            lista.append(rdico2.perfil_carga)

        return lista

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()