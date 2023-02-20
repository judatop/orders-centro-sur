import pymysql
from controller.gestor_controller import Gestor
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine
import pandas

from model.cliente import Cliente
from model.gruporevisor import GrupoRevisor
from model.historialmedidor import HistorialMedidor
from model.instalacion import Instalacion
from model.medidor import Medidor
from model.cliente_instalacion import Cliente_Instalacion
import time
from peewee import *
from controller.conexion_controller import Conexion
from model.medidortemp import MedidorTemp
from model.orden import Orden
from model.revisor import Revisor
from model.usuario import Usuario
from model.rdico2 import RDICO2
from model.rdico5 import RDICO5
from flask import flash
from datetime import date
from datetime import datetime
import numpy as np


def cargarCatastroClientes(rutaCatastroClientes):
        print("************** INICIA CARGA DE CATASTRO CLIENTES **************")
        tic = time.perf_counter()

        g = Gestor()
        db = Conexion.db
        db.connect()
        
        columnasarchivoCliente = ["Nombre", "Direccion", "Email", "Telefono", "Cuen", "Tarifa", "Mru",
                                  "Fm", "Cedula", "Cuentacontrato", "Instalacion", "Medidor", "Zzutm X",
                                  "Zzutm Y", "Latitud", "Longitud"]
        valoresVaciosLlenar = {'razonSocial': '', 'direccion': '', 'correo': '', 'telefono': '',
                               'cuenta': '', 'tipoTarifa': '', 'mru': '', 'fm': '0', 'identificacion': '',
                               'cc': '', 'numeroI': '', 'numeroM': '', 'utmX': '0', 'utmY': '0', 'coordenadaX': '0',
                               'coordenadaY': '0'}
        dfClientes = pandas.read_csv(rutaCatastroClientes, usecols=columnasarchivoCliente,
                                     dtype={"Cedula": "string", "Nombre": "string", "Direccion": "string",
                                            "Email": "string", "Telefono": "string", "Cuen": "string",
                                            "Tarifa": "string", "Mru": "string", "Fm": "string", "Cedula": "string",
                                            "CuentaContrato": "string", "Instalacion": "string", "Medidor": "string",
                                            "Zzutm X": "string", "Zzutm Y": "string", "Latitud": "string", "Longitud":
                                                "string"}).rename(columns={
            'Cedula': 'identificacion', 'Nombre': 'razonSocial', 'Direccion': 'direccion',
            'Email': 'correo', 'Telefono': 'telefono', 'Cuen': 'cuenta', 'Instalacion': 'numeroI', 'Medidor': 'numeroM',
            'Zzutm X': 'utmX', 'Zzutm Y': 'utmY', 'Latitud': 'coordenadaX', 'Longitud': 'coordenadaY', 'Cuentacontrato':
                'cc', 'Tarifa': 'tipoTarifa', 'Mru': 'mru', 'Fm': 'fm'}, inplace=False).fillna(
            value=valoresVaciosLlenar)   
        dfClientes = dfClientes[dfClientes['numeroM'] != 'SINMEDIDOR']
        con = create_engine('mysql+pymysql://' + g.db_user + ':' + g.db_password + '@localhost/orden')

        dicts_clientes = dfClientes.to_dict('records')
        dfMedidorBD = pandas.read_sql('SELECT * FROM medidor', con=con)
        dfClienteBD = pandas.read_sql('SELECT * FROM cliente', con=con)

        db.close()

        lista_dicts_medidores = []
        lista_dicts_instalaciones = []
        lista_dicts_clientes = []
        lista_clientes_update = []
        lista_dicts_cliente_instalaciones = []
        tamano = np.arange(len(dicts_clientes))
    
        print("Inicio del bucle")
        for index in np.nditer(tamano):
            row = dicts_clientes[index]
            identificacion_cliente = row['identificacion']
            numero_medidor = row['numeroM'].lstrip('0')
            cc = str(row['cc'])
            numero_instalacion = row['numeroI']

            medidor_bd = dfMedidorBD.loc[dfMedidorBD['cc'] == cc]
            medidor_dict = list(filter(lambda di: di['cc'] == cc, lista_dicts_medidores))

            if medidor_bd.empty and not medidor_dict:
                lista_dicts_medidores.insert(len(lista_dicts_medidores), {'numero': numero_medidor,
                                                                          'cc': row['cc']})
                lista_dicts_instalaciones.insert(len(lista_dicts_instalaciones), {'numero': numero_instalacion,
                                                                                  'coordenadaX': row['coordenadaX'],
                                                                                  'coordenadaY': row['coordenadaY'],
                                                                                  'utmX': row['utmX'],
                                                                                  'utmY': row['utmY'],
                                                                                  'medidor': numero_medidor})
                lista_dicts_cliente_instalaciones.insert(len(lista_dicts_cliente_instalaciones), {'cliente': identificacion_cliente, 'instalacion': numero_instalacion})                                                          

            cliente_bd = dfClienteBD.loc[dfClienteBD['identificacion'] == identificacion_cliente]
            cliente_dict = list(filter(lambda di: di['identificacion'] == identificacion_cliente,
                                       lista_dicts_clientes))

            if cliente_bd.empty and not cliente_dict:
                lista_dicts_clientes.insert(len(lista_dicts_clientes),
                                            {'identificacion': identificacion_cliente,
                                             'razonSocial': row['razonSocial'],
                                             'direccion': row['direccion'], 'correo': row['correo'],
                                             'telefono': row['telefono'], 'cuenta': row['cuenta'],
                                             'tipoTarifa': row['tipoTarifa'], 'mru': row['mru'], 'fm': row['fm']})
                
            if not cliente_bd.empty:
                lista_clientes_update.insert(len(lista_clientes_update), (row['direccion'], row['correo'], row['telefono'], cliente_bd.iloc[0]['id']))

        print("Fin del bucle")
        db.connect()
        cur = db.cursor()
        with db.atomic():
            cur.executemany("UPDATE cliente SET direccion = %s, correo = %s, telefono = %s WHERE Id = %s ", lista_clientes_update)
            Medidor.insert_many(lista_dicts_medidores).execute()
            Instalacion.insert_many(lista_dicts_instalaciones).execute()
            Cliente.insert_many(lista_dicts_clientes).execute()
            Cliente_Instalacion.insert_many(lista_dicts_cliente_instalaciones).execute()

        flash('Catastro de clientes cargado correctamente', 'exito')
        db.close()
        
        toc = time.perf_counter()
        print(f"Tiempo {toc - tic:0.2f} segundos")
        print("************** TERMINA CARGA DE CATASTRO CLIENTES **************")


def cargarCatastroHistorialConsumos(rutaCatastroHistorial):
    try:
        print("************** INICIA CARGA DE CATASTRO HISTORIAL DE CONSUMOS **************")
        tic = time.perf_counter()

        g = Gestor()
        db = Conexion.db
        db.connect()

        columnasarchivoHistorial = ["Kwh N1", "Kwh N2", "Kwh N3", "Kwh N4", "Kwh N5", "Kwh N6", "Kwh N7", "Kwh N8", "Kwh N9", "Kwh N10", "Kwh N11", "Kwh N12"]
        valoresVaciosLlenar = {'mes1': 0, 'mes2': 0, 'mes3': 0, 'mes4': 0, 'mes5': 0, 'mes6': 0, 'mes7': 0, 'mes8': 0, 'mes9': 0, 'mes10': 0, 'mes11': 0, 'mes12': 0}
        dfHistorial = pandas.read_csv(rutaCatastroHistorial, usecols=columnasarchivoHistorial, decimal=','). \
            rename(columns={'Kwh N1': 'mes1', 'Kwh N2': 'mes2', 'Kwh N3': 'mes3', 'Kwh N4': 'mes4', 'Kwh N5': 'mes5', 'Kwh N6': 'mes6', 'Kwh N7': 'mes7', 'Kwh N8': 'mes8', 'Kwh N9': 'mes9', 'Kwh N10': 'mes10', 'Kwh N11': 'mes11', 'Kwh N12': 'mes12'},
                   inplace=False).fillna(value=valoresVaciosLlenar)
        con = create_engine('mysql+pymysql://' + g.db_user + ':' + g.db_password + '@localhost/orden')

        # Obtenemos promedio y borramos las columnas que no sirven
        dfHistorial['consumokWh'] = dfHistorial.sum(axis=1) / 12

        columnasarchivoHistorial = ["Medidor", "Marca Medidor", 
        "Kw N1","Kw N2","Kw N3","Kw N4","Kw N5","Kw N6","Kw N7","Kw N8","Kw N9","Kw N10","Kw N11","Kw N12",
        "Kvr N1","Kvr N2","Kvr N3","Kvr N4","Kvr N5","Kvr N6","Kvr N7","Kvr N8","Kvr N9","Kvr N10","Kvr N11","Kvr N12", "Factor Potencia N1"]
        valoresVaciosLlenar = {'numero': '', 'marca': '', 
                               'Kw N1': 0,'Kw N2': 0,'Kw N3': 0,'Kw N4': 0,'Kw N5': 0,'Kw N6': 0,'Kw N7': 0,'Kw N8': 0,'Kw N9': 0,'Kw N10': 0,'Kw N11': 0,'Kw N12': 0,
                               'Kvr N1': 0,'Kvr N2': 0,'Kvr N3': 0,'Kvr N4': 0,'Kvr N5': 0,'Kvr N6': 0,'Kvr N7': 0,'Kvr N8': 0,'Kvr N9': 0,'Kvr N10': 0,'Kvr N11': 0,'Kvr N12': 0, 
                               'Factor Potencia N1': 0}
        dfHistorial2 = pandas.read_csv(rutaCatastroHistorial, usecols=columnasarchivoHistorial, decimal=',',
                                      dtype={"Medidor": "string", "Marca Medidor": "string"}). \
            rename(columns={'Medidor': 'numero', 'Marca Medidor': 'marca'},
                   inplace=False).fillna(value=valoresVaciosLlenar)

        df_final = pandas.concat([dfHistorial2, dfHistorial], axis=1, join='inner')

        df_dict = df_final.to_dict('records')
        dfMedidorBD = pandas.read_sql('SELECT * FROM medidor', con=con)
        lista_dicts_medidores = []
        lista_dicts_historiales = []
        db.close()

        print("Inicio del bucle")
        for row in df_dict:
            numero_medidor = row['numero']

            medidor_bd = dfMedidorBD.loc[dfMedidorBD['numero'] == numero_medidor]
            if not medidor_bd.empty:
                lista_dicts_medidores.insert(len(lista_dicts_medidores), (row['consumokWh'],
                                                                          row['marca'], row['Factor Potencia N1'], medidor_bd.iloc[0]['id']))

                lista_dicts_historiales.insert(len(lista_dicts_historiales), {'mes1': row['mes1'], 'mes2': row['mes2'], 'mes3': row['mes3'], 'mes4': row['mes4'], 'mes5': row['mes5'], 'mes6': row['mes6'], 'mes7': row['mes7'], 'mes8': row['mes8'], 'mes9': row['mes9'], 'mes10': row['mes10'], 'mes11': row['mes11'], 'mes12': row['mes12'], 'tipo': 'Consumos', 'numero_medidor': row['numero']})
                lista_dicts_historiales.insert(len(lista_dicts_historiales), {'mes1': row['Kw N1'], 'mes2': row['Kw N2'], 'mes3': row['Kw N3'], 'mes4': row['Kw N4'], 'mes5': row['Kw N5'], 'mes6': row['Kw N6'], 'mes7': row['Kw N7'], 'mes8': row['Kw N8'], 'mes9': row['Kw N9'], 'mes10': row['Kw N10'], 'mes11': row['Kw N11'], 'mes12': row['Kw N12'], 'tipo': 'Demandas', 'numero_medidor': row['numero']})
                lista_dicts_historiales.insert(len(lista_dicts_historiales), {'mes1': row['Kvr N1'], 'mes2': row['Kvr N2'], 'mes3': row['Kvr N3'], 'mes4': row['Kvr N4'], 'mes5': row['Kvr N5'], 'mes6': row['Kvr N6'], 'mes7': row['Kvr N7'], 'mes8': row['Kvr N8'], 'mes9': row['Kvr N9'], 'mes10': row['Kvr N10'], 'mes11': row['Kvr N11'], 'mes12': row['Kvr N12'],'tipo': 'Reactivos', 'numero_medidor': row['numero'] })
        print("Fin del bucle")

        db.connect()
        cur = db.cursor()
        with db.atomic():
            cur.executemany("UPDATE medidor SET consumokWh = %s, marca = %s, factor_potencia = %s WHERE Id = %s ", lista_dicts_medidores)
            HistorialMedidor.insert_many(lista_dicts_historiales).execute()
        flash('Catastro de historial de consumos cargado correctamente', 'exito')

        toc = time.perf_counter()
        print(f"Tiempo {toc - tic:0.2f} segundos")
        print("************** TERMINA CARGA DE CATASTRO HISTORIAL DE CONSUMOS **************")
    except Exception as ex:
        flash('Error al intentar cargar el catastro de historial de consumos', 'error')
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()


def cargarCatastroOrdenes(rutaCatastroOrdenes):
    try:
        print("************** INICIA CARGA DE CATASTRO ORDENES **************")
        tic = time.perf_counter()

        g = Gestor()
        db = Conexion.db
        db.connect()
        
        columnasArchivoOrdenes = ["Orden", "Fe.inic.extrema", "Texto breve", "Instalación", "Descripción Puesto d",
                                  "Status sistema"]
        valoresVaciosLlenar = {'numero': 0, 'fechaCreacion': '', 'comentarioInicial': '', 'instalacion': '',
                               'revisor': '', 'estado': ''}
        dfOrdenes = pandas.read_csv(rutaCatastroOrdenes, usecols=columnasArchivoOrdenes, sep=';', encoding='latin-1',
                                    dtype={"Orden": "string", "Texto breve": "string",
                                           "Instalación": "string", "Descripción Puesto d": "string",
                                           "Status sistema": "string"}). \
            rename(columns={'Orden': 'numero', 'Fe.inic.extrema': 'fechaCreacion', 'Texto breve': 'comentarioInicial',
                            'Descripción Puesto d': 'revisor', 'Instalación': 'instalacion',
                            'Status sistema': 'estado'}, inplace=False). \
            fillna(value=valoresVaciosLlenar)
        dfOrdenes['fechaCreacion'] = pandas.to_datetime(dfOrdenes['fechaCreacion'], dayfirst=True)
        con = create_engine('mysql+pymysql://' + g.db_user + ':' + g.db_password + '@localhost/orden')

        df_dict = dfOrdenes.to_dict('records')
        dfOrdenBD = pandas.read_sql('SELECT * FROM orden', con=con)
        dfInstalacionBD = pandas.read_sql('SELECT * FROM instalacion', con=con)
        dfRevisorBD = pandas.read_sql('SELECT * FROM revisor', con=con)

        lista_dicts_ordenes = []

        for row in df_dict:
            numero_orden = row['numero']
            
            orden_bd = dfOrdenBD.loc[dfOrdenBD['numero'] == numero_orden]
            orden_dict = list(filter(lambda di: di['numero'] == numero_orden, lista_dicts_ordenes))

            if orden_bd.empty and not orden_dict:
                instalacion_bd = dfInstalacionBD.loc[dfInstalacionBD['numero'] == row['instalacion']]
                revisor_bd = dfRevisorBD.loc[dfRevisorBD['razonSocial'] == row['revisor']]
                estado = row['estado'].lower()

                if not instalacion_bd.empty and not revisor_bd.empty and "lib" in estado:

                    lista_dicts_ordenes.insert(len(lista_dicts_ordenes), {'numero': numero_orden,
                                                                            'fechaCreacion': row['fechaCreacion'],
                                                                            'estado': 'Liberada',
                                                                            'comentarioInicial': row['comentarioInicial'],
                                                                            'instalacion_id': instalacion_bd.iloc[0][
                                                                                'id'],
                                                                            'revisor_id': revisor_bd.iloc[0]['id']})

        with db.atomic():
            Orden.insert_many(lista_dicts_ordenes).execute()

        ordenes = Orden.select().execute()

        for orden in ordenes:
            rdico2 = RDICO2()
            rdico5 = RDICO5()
            rdico2.save()
            rdico5.save()
            orden.rdico2_id = rdico2.id
            orden.rdico5_id = rdico5.id
            orden.save()

        flash('Catastro de órdenes cargado correctamente', 'exito')

        toc = time.perf_counter()
        print(f"Tiempo {toc - tic:0.2f} segundos")
        print("************** TERMINA CARGA DE CATASTRO ORDENES **************")

    except Exception as ex:
        flash('Error al intentar cargar el catastro de órdenes', 'error')
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()


def cargarCatastroMarcasMedidores(archivoMarcasMedidores):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()
        rutaCatastroMarcasMedidores = g.rutaCatastros + secure_filename(archivoMarcasMedidores.filename)
        archivoMarcasMedidores.save(rutaCatastroMarcasMedidores)
        columnasArchivoMarcasMedidores = ["Anio Fabricacion", "Clase Precision", "CorrienteBasica", "CorrienteMaxima",
                                          "Voltaje", "Constante", "TipoMedicion", "Forma", "Marca", "Modelo"]
        valoresVaciosLlenar = {'ano': '', 'exactitud': '', 'corriente_basica': '', 'corriente_maxima': '', 'voltaje': '',
                               'constanteK': 0, 'tipo_medicion': '', 'conexion': '', 'marca': '', 'tipo': ''}
        dfMarcasMedidores = pandas.read_csv(rutaCatastroMarcasMedidores, usecols=columnasArchivoMarcasMedidores,
                                            sep=';', encoding='latin-1', dtype={"Anio Fabricacion": "string",
                                                                                "Clase Precision": "string",
                                                                                "CorrienteBasica": "string",
                                                                                "CorrienteMaxima": "string",
                                                                                "Voltaje": "string",
                                                                                "Constante": "float",
                                                                                "TipoMedicion": "string",
                                                                                "Forma": "string",
                                                                                "Marca": "string",
                                                                                "Modelo": "string",
                                                                                }). \
            rename(columns={'Anio Fabricacion': 'ano', 'Clase Precision': 'exactitud',
                            'CorrienteBasica': 'corriente_basica',
                            'CorrienteMaxima': 'corriente_maxima', 'Voltaje': 'voltaje',
                            'Constante': 'constanteK', 'TipoMedicion': 'tipo_medicion', 'Forma': 'conexion',
                            'Marca': 'marca', 'Modelo': 'tipo'}, inplace=False). \
            fillna(value=valoresVaciosLlenar)
        dfMarcasMedidores['corriente'] = dfMarcasMedidores['corriente_basica']+"-"+dfMarcasMedidores['corriente_maxima']
        dfMarcasMedidores = dfMarcasMedidores.drop(['corriente_basica', 'corriente_maxima'], axis=1)

        con = create_engine('mysql+pymysql://' + g.db_user + ':' + g.db_password + '@localhost/orden')

        conn = pymysql.connect(host= g.host, user=g.db_user, password=g.db_password)
        conn.cursor().execute('TRUNCATE TABLE orden.medidortemp')
        conn.close()

        df_dict = dfMarcasMedidores.to_dict('records')
        lista_dicts_marcas = []
        for row in df_dict:
            lista_dicts_marcas.insert(len(lista_dicts_marcas), row)

        with db.atomic():
            MedidorTemp.insert_many(lista_dicts_marcas).execute()

        flash('Catastro de marcas de medidores cargado correctamente', 'exito')

    except Exception as ex:
        flash('Error al intentar cargar el catastro de marcas de medidores', 'error')
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        db.close()
