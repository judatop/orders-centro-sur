
from decimal import *
from flask import render_template, url_for, request
from flask_login import login_required
from flask import flash
from werkzeug.utils import redirect
from werkzeug.utils import secure_filename

from controller import orden_controller
from controller import instalacion_controller
from controller import cliente_controller
from controller import medidor_controller
from controller import usuarios_controller
from app.forms.modificar_orden_form import ModificarOrdenForm
from app.forms.orden_form import OrdenForm
from app import app
from controller.gestor_controller import Gestor
from model.anomaliaencontrada import AnomaliaEncontrada
from model.cambiomaterial import CambioMaterial
from model.lecturatotal import LecturaTotal
from model.parametrizacion import Parametrizacion
from model.prueba import Prueba
from model.sello import Sello
from model.transformadordedistribucion import TransformadorDeDistribucion
from model.transformadordemedida import TransformadorDeMedida
from model.usoenergiaverificado import UsoEnergiaVerificado
from model.contactotecnico import ContactoTecnico
from datetime import datetime
from datetime import date
import copy
import folium

from model.verificacion import Verificacion


@app.route('/orden.html', methods=['GET', 'POST'])
@login_required
def orden():
    privilegio = usuarios_controller.verificar_privilegios("Orden")
    if privilegio:
        params = []

        orden_form = OrdenForm()
        ordenes = orden_controller.obtenerOrdenes()

        params.append(ordenes) # params[0]
        params.append(orden_form) # params[1]

        if orden_form.realizar_orden.data:
            numero_orden = request.form['input_numero_orden']

            if numero_orden == "0":
                flash('Debe seleccionar una orden','error')
            else:
                return redirect(url_for('modificar_orden', numero_orden=numero_orden))

        if orden_form.ver_ordenes.data:
            ordenes = orden_controller.obtenerOrdenesMapa()
            start_coords = (-2.8752033070, -78.9778660700)
            folium_map = folium.Map(location=start_coords, zoom_start=14, title="Instalaciones de órdenes")
            for orden in ordenes:
                instalacion = instalacion_controller.obtener_instalacion(orden.instalacion_id)
                medidor = medidor_controller.obtener_medidor_por_instalacion(instalacion.numero)

                coordenadaX = instalacion.coordenadaX
                coordenadaY = instalacion.coordenadaY
                tooltip = "Click"
                folium.Marker([coordenadaX, coordenadaY], popup="Instalación "+str(instalacion.numero)+" del medidor "+str(medidor.numero), tooltip=tooltip).add_to(folium_map)

            return folium_map._repr_html_()

        if orden_form.generar_kml.data:
            orden_controller.generar_kml(ordenes)
        return render_template('orden.html', segment='orden', params=params)
    return redirect(url_for('index'))


@app.route('/modificar_orden/<int:numero_orden>', methods=['GET', 'POST'])
@login_required
def modificar_orden(numero_orden):
    params = []
    divActual = ""
    dialogActual = ""
    modificar_orden_form = ModificarOrdenForm()
    bandera = 1
    g = Gestor()

    orden = orden_controller.obtener_orden(numero_orden)
    instalacion = instalacion_controller.obtener_instalacion(orden.instalacion_id)
    cliente = cliente_controller.obtener_cliente_por_instalacion(instalacion.numero)
    medidor = medidor_controller.obtener_medidor_por_instalacion(instalacion.numero)
    rdico2 = orden_controller.obtener_rdico2(orden)
    rdico5 = orden_controller.obtener_rdico5(orden)

    llenar_choices_listas(modificar_orden_form, numero_orden) # Inicializacion de opciones de selectores y de listas

    if modificar_orden_form.boton_cambio_marca_orden.data: # Cambio marca de medidor
        divActual = "divMedidor"
        guardar_orden(modificar_orden_form, numero_orden)
        bandera = 0

    if modificar_orden_form.boton_cambio_marca_transformador_medida_orden.data: # Cambio tipo en transformador de medida
        divActual = "divTransformadorMedida"
        nuevo_tipo = modificar_orden_form.tipo_transformador_medida_orden.data
        dict_choices = orden_controller.cargar_choices_caracteristicas()
        if nuevo_tipo == "TC":
            modificar_orden_form.marca_transformador_medida_orden.choices = dict_choices['marcatc']
        if nuevo_tipo == "TP":
            modificar_orden_form.marca_transformador_medida_orden.choices = dict_choices['marcatp']
        if nuevo_tipo == "TCS COMBINADO" or nuevo_tipo == "TPS COMBINADO":
            modificar_orden_form.marca_transformador_medida_orden.choices = dict_choices['marcatcstps']
        guardar_orden(modificar_orden_form, numero_orden)
        bandera = 0

    if modificar_orden_form.anadir_transformador_medida_orden.data: # Crear transformador de medida
        divActual = "divTransformadorMedida"

        transformador_medida = TransformadorDeMedida()
        transformador_medida.numeroDeSerie = modificar_orden_form.numero_serie_transformador_medida_orden.data
        transformador_medida.numeroDeEmpresa = modificar_orden_form.numero_empresa_transformador_medida_orden.data
        transformador_medida.marca = modificar_orden_form.marca_transformador_medida_orden.data
        transformador_medida.relacionDeTransformacion = modificar_orden_form.relacion_transformacion_transformador_medida_orden.data
        transformador_medida.burden = modificar_orden_form.s_transformador_medida_orden.data
        transformador_medida.exactitud = modificar_orden_form.exactitud_transformador_medida_orden.data
        transformador_medida.ano = modificar_orden_form.ano_transformador_medida_orden.data
        transformador_medida.sellosEncontrados = modificar_orden_form.sellos_encontrados_transformador_medida_orden.data
        transformador_medida.tipo = modificar_orden_form.tipo_transformador_medida_orden.data

        orden_controller.crear_transformador_medida(transformador_medida, rdico2)
        modificar_orden_form.lista_transformadores_medida_orden = orden_controller.obtener_transformadores_medida(rdico2)
        vaciar_campos_transformador_medida(modificar_orden_form)
        bandera = 0
    
    if modificar_orden_form.anadir_transformador_distribucion_orden.data: # Crear transformador de distribucion
        divActual = "divTransformadorDistribucion"
        transformador_distribucion = TransformadorDeDistribucion()
        transformador_distribucion.numero = modificar_orden_form.numero_transformador_distribucion_orden.data
        transformador_distribucion.marca = modificar_orden_form.marca_transformador_distribucion_orden.data
        transformador_distribucion.tipo = modificar_orden_form.tipo_transformador_distribucion_orden.data
        transformador_distribucion.capacidadMaxima = modificar_orden_form.s_transformador_distribucion_orden.data
        transformador_distribucion.voltaje = modificar_orden_form.v_transformador_distribucion_orden.data
        transformador_distribucion.ano = modificar_orden_form.ano_transformador_distribucion_orden.data
        transformador_distribucion.zcc = modificar_orden_form.zcc_transformador_distribucion_orden.data
        transformador_distribucion.conexion = modificar_orden_form.conexion_transformador_distribucion_orden.data

        orden_controller.crear_transformador_distribucion(transformador_distribucion, rdico2)
        modificar_orden_form.lista_transformadores_distribucion_orden = orden_controller.obtener_transformadores_distribucion(rdico2)
        vaciar_campos_transformador_distribucion(modificar_orden_form)
        bandera = 0

    if modificar_orden_form.anadir_prueba_pruebas_orden.data: # Crear prueba
        divActual = "divPruebas"
        prueba = Prueba()    
        prueba.rfase1 = Decimal(0)
        prueba.sfase2 = Decimal(0)
        prueba.tfase3 = Decimal(0)
        prueba.potencia_total = Decimal(0)
        prueba.revoluciones = Decimal(0)
        prueba.tiempo = Decimal(0)
        prueba.pkw_medidor = Decimal(0)
        prueba.error = Decimal(0)
        if modificar_orden_form.rfase1_pruebas_orden.data:  # rfase1
            prueba.rfase1 = modificar_orden_form.rfase1_pruebas_orden.data
        if modificar_orden_form.sfase2_pruebas_orden.data:  # sfase2
            prueba.sfase2 = modificar_orden_form.sfase2_pruebas_orden.data
        if modificar_orden_form.tfase3_pruebas_orden.data:  # tfase3
            prueba.tfase3 = modificar_orden_form.tfase3_pruebas_orden.data
        if not modificar_orden_form.unidad_electrica_pruebas_orden.data == "V[V]" and not modificar_orden_form.unidad_electrica_pruebas_orden.data == "Fp [cosɸ]":
            prueba.potencia_total = prueba.rfase1 + prueba.sfase2 + prueba.tfase3
            if modificar_orden_form.numero_revoluciones_pruebas_orden.data:  # revoluciones
                prueba.revoluciones = modificar_orden_form.numero_revoluciones_pruebas_orden.data
            if modificar_orden_form.tiempo_pruebas_orden.data:  # tiempo
                prueba.tiempo = modificar_orden_form.tiempo_pruebas_orden.data
            constantek = modificar_orden_form.constantek_medidor_orden.data
            if constantek and prueba.tiempo > 0:
                constantek = constantek.replace(",",".")
                constantek_decimal = Decimal(constantek)
                if constantek_decimal > 0:
                    tcs = 0
                    tps = 0
                    if modificar_orden_form.tcs_parametrizacion_orden.data:
                        tcs = modificar_orden_form.tcs_parametrizacion_orden.data
                    if modificar_orden_form.tps_parametrizacion_orden.data:
                        tps = modificar_orden_form.tps_parametrizacion_orden.data
                    prueba.pkw_medidor = ((3600 * prueba.revoluciones * tcs * tps) / (constantek_decimal)) / prueba.tiempo

            if not modificar_orden_form.error_pruebas_orden.data:
                if prueba.potencia_total > 0:
                    prueba.error = ((prueba.pkw_medidor - prueba.potencia_total)/prueba.potencia_total) * 100
            else:
                prueba.error = modificar_orden_form.error_pruebas_orden.data

        prueba.unidadElectrica = modificar_orden_form.unidad_electrica_pruebas_orden.data
        orden_controller.crear_prueba(prueba, rdico2)
        modificar_orden_form.lista_pruebas_orden = orden_controller.obtener_pruebas(rdico2)
        vaciar_campos_pruebas(modificar_orden_form)
        bandera = 0
    
    if modificar_orden_form.anadir_sello_orden.data: # Crear sello
        divActual = "divSellos"
        sello = Sello(sello="", modelo="", ubicacion="", estado="", tipo="")
        sello.sello = modificar_orden_form.sello_sello_orden.data
        sello.modelo = modificar_orden_form.modelo_sello_orden.data
        sello.ubicacion = modificar_orden_form.ubicacion_sello_orden.data
        sello.estado = modificar_orden_form.estado_sello_orden.data
        sello.tipo = modificar_orden_form.tipo_sello_orden.data
        orden_controller.crear_sello(sello, rdico2)
        modificar_orden_form.lista_sellos_orden = orden_controller.obtener_sellos(rdico2)
        vaciar_campos_sellos(modificar_orden_form)
        bandera = 0

    if modificar_orden_form.anadir_uso_energia_resultados_orden.data: # Crear uso
        divActual = "divResultados"
        id_uso = modificar_orden_form.uso_energia_resultados_orden.data
        orden_controller.crear_uso_energia(id_uso, rdico2)
        modificar_orden_form.lista_usos_energia_orden = orden_controller.obtener_usos_energia(rdico2)
        bandera = 0

    if modificar_orden_form.anadir_anomalia_encontrada_resultados_orden.data: # Crear anomalia
        divActual = "divResultados"
        id_anomalia = modificar_orden_form.anomalia_encontrada_resultados_orden.data
        orden_controller.crear_anomalia(id_anomalia, rdico2)
        modificar_orden_form.lista_anomalias_orden = orden_controller.obtener_anomalias(rdico2)
        modificar_orden_form.lista_anomalias_acciones_orden = orden_controller.obtener_anomalias_acciones_agregadas(rdico2)
        bandera = 0    

    if modificar_orden_form.boton_agregar_accion_rdico5.data: # Crear accion
        divActual = "divRDICO5"
        id_anomalia = int(request.form['input_index_anomalia'])
        id_accion =  modificar_orden_form.lista_acciones_rdico5_orden.data
        orden_controller.crear_accion(id_anomalia, id_accion, rdico2)
        modificar_orden_form.lista_anomalias_acciones_orden = orden_controller.obtener_anomalias_acciones_agregadas(rdico2)
        bandera = 0

    if modificar_orden_form.agregar_fotografia.data: # Crear fotografia
        divActual = "divFotografias"
        fotografia = modificar_orden_form.archivo_fotografia_fotografia_orden.data
        if fotografia:
            date_string = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
            ruta_imagen = g.rutaImagenes +  date_string + " " + secure_filename(fotografia.filename)
            fotografia.save(ruta_imagen)
            orden_controller.crear_fotografia(fotografia, secure_filename(fotografia.filename), ruta_imagen, rdico2)
            modificar_orden_form.lista_fotografias = orden_controller.obtener_fotografias(rdico2)
        bandera = 0  

    if modificar_orden_form.agregar_lectura.data: # Crear lectura
        divActual = "divLecturas"
        lectura = modificar_orden_form.archivo_lectura_lecturas_orden.data
        if lectura:
            date_string = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
            ruta_lectura = g.rutaLecturas +  date_string + " " + secure_filename(lectura.filename)
            lectura.save(ruta_lectura)
            orden_controller.crear_archivo_lectura(secure_filename(lectura.filename), ruta_lectura, rdico2)
            modificar_orden_form.lista_archivo_lectura = orden_controller.obtener_archivo_lectura(rdico2)
        bandera = 0  

    if modificar_orden_form.agregar_perfil.data: # Crear perfil
        divActual = "divPerfilesDeCarga"
        perfil_carga = modificar_orden_form.archivo_perfil_carga_orden.data
        if perfil_carga:
            date_string = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
            ruta_perfil = g.rutaPerfiles +  date_string + " " + secure_filename(perfil_carga.filename)
            perfil_carga.save(ruta_perfil)
            orden_controller.crear_perfil(secure_filename(perfil_carga.filename), ruta_perfil, rdico2)
            modificar_orden_form.lista_archivo_perfil = orden_controller.obtener_archivo_perfil(rdico2)
        bandera = 0

    if modificar_orden_form.anadir_lectura_lectura_orden.data: # Crear lectura
        divActual = "divLecturas"
        lectura = LecturaTotal(a_horarias=0, b_horarias=0, c_horarias=0, d_horarias=0, a_demandas=0, b_demandas=0, c_demandas=0, d_demandas=0, kvarh=0)
        lectura.a_horarias = modificar_orden_form.a_horarias_lectura_orden.data
        lectura.b_horarias = modificar_orden_form.b_horarias_lectura_orden.data
        lectura.c_horarias = modificar_orden_form.c_horarias_lectura_orden.data
        lectura.d_horarias = modificar_orden_form.d_horarias_lectura_orden.data
        lectura.a_demandas = modificar_orden_form.a_demandas_lectura_orden.data
        lectura.b_demandas = modificar_orden_form.b_demandas_lectura_orden.data
        lectura.c_demandas = modificar_orden_form.c_demandas_lectura_orden.data
        lectura.d_demandas = modificar_orden_form.d_demandas_lectura_orden.data
        lectura.d_demandas = modificar_orden_form.d_demandas_lectura_orden.data
        lectura.kvarh = modificar_orden_form.kvarh_lectura_orden.data
        lectura.tipo = modificar_orden_form.tipo_lectura_orden.data
        orden_controller.crear_lectura(lectura, rdico2)
        modificar_orden_form.lista_lecturas_totales_orden = orden_controller.obtener_lecturas(rdico2)
        vaciar_campos_lecturas(modificar_orden_form)
        bandera = 0

    if modificar_orden_form.boton_crear_faltante_medidor_orden.data: # Crear faltante medidor
        divActual = "divMedidor"
        tipo_caracteristica = modificar_orden_form.tipo_faltante_medidor_orden.data
        texto_caracteristica = modificar_orden_form.nombre_faltante_medidor_orden.data
        if texto_caracteristica == "":
            flash('Característica vacía','error')
            dialogActual = "dialogMedidor"
        elif tipo_caracteristica == "Marca":
            modificar_orden_form.marca_medidor_orden.choices.append((texto_caracteristica,texto_caracteristica))
            modificar_orden_form.marca_medidor_orden.data = texto_caracteristica
            modificar_orden_form.nombre_faltante_medidor_orden.data = ""
            modificar_orden_form.lista_marcas_faltantes_creadas.append((texto_caracteristica,texto_caracteristica))
        elif tipo_caracteristica == "Tipo":
            modificar_orden_form.tipo_medidor_orden.choices.append((texto_caracteristica,texto_caracteristica))
            modificar_orden_form.tipo_medidor_orden.data = texto_caracteristica
            modificar_orden_form.nombre_faltante_medidor_orden.data = ""
            modificar_orden_form.lista_tipos_faltantes_creadas.append((texto_caracteristica,texto_caracteristica))
        elif tipo_caracteristica == "Año":
            modificar_orden_form.ano_medidor_orden.choices.append((texto_caracteristica,texto_caracteristica))
            modificar_orden_form.ano_medidor_orden.data = texto_caracteristica
            modificar_orden_form.nombre_faltante_medidor_orden.data = ""
            modificar_orden_form.lista_anos_faltantes_creadas.append((texto_caracteristica,texto_caracteristica))
        elif tipo_caracteristica == "Exactitud":
            modificar_orden_form.exactitud_medidor_orden.choices.append((texto_caracteristica,texto_caracteristica))
            modificar_orden_form.exactitud_medidor_orden.data = texto_caracteristica
            modificar_orden_form.nombre_faltante_medidor_orden.data = ""    
            modificar_orden_form.lista_exactitud_faltantes_creadas.append((texto_caracteristica,texto_caracteristica))
        elif tipo_caracteristica == "Corriente":
            modificar_orden_form.corriente_medidor_orden.choices.append((texto_caracteristica,texto_caracteristica))
            modificar_orden_form.corriente_medidor_orden.data = texto_caracteristica
            modificar_orden_form.nombre_faltante_medidor_orden.data = ""
            modificar_orden_form.lista_corriente_faltantes_creadas.append((texto_caracteristica,texto_caracteristica))
        elif tipo_caracteristica == "Voltaje":
            modificar_orden_form.voltaje_medidor_orden.choices.append((texto_caracteristica,texto_caracteristica))
            modificar_orden_form.voltaje_medidor_orden.data = texto_caracteristica
            modificar_orden_form.nombre_faltante_medidor_orden.data = ""
            modificar_orden_form.lista_voltaje_faltantes_creadas.append((texto_caracteristica,texto_caracteristica))
        elif tipo_caracteristica == "Constante K":
            modificar_orden_form.constantek_medidor_orden.choices.append((texto_caracteristica,texto_caracteristica))
            modificar_orden_form.constantek_medidor_orden.data = texto_caracteristica
            modificar_orden_form.nombre_faltante_medidor_orden.data = ""
            modificar_orden_form.lista_constantek_faltantes_creadas.append((texto_caracteristica,texto_caracteristica))
        elif tipo_caracteristica == "Conexión":
            modificar_orden_form.conexion_medidor_orden.choices.append((texto_caracteristica,texto_caracteristica))
            modificar_orden_form.conexion_medidor_orden.data = texto_caracteristica
            modificar_orden_form.nombre_faltante_medidor_orden.data = "" 
            modificar_orden_form.lista_conexion_faltantes_creadas.append((texto_caracteristica,texto_caracteristica))    
        bandera = 0

    if modificar_orden_form.boton_crear_faltante_parametrizacion_orden.data: # Crear faltante parametrizacion
        divActual = "divParametrizacion"
        tipo_caracteristica = modificar_orden_form.tipo_faltante_parametrizacion_orden.data
        texto_caracteristica = modificar_orden_form.nombre_faltante_parametrizacion_orden.data
        bandera_creado = orden_controller.anadir_caracteristica("parametrizacion", tipo_caracteristica, texto_caracteristica)
        if not bandera_creado:
            dialogActual = "dialogParametrizacion"
        else:
            llenar_choices_caracteristicas(modificar_orden_form)
            modificar_orden_form.nombre_faltante_parametrizacion_orden.data = ""
            if tipo_caracteristica == "Multiplicador":
                modificar_orden_form.multiplicador_parametrizacion_orden.data = texto_caracteristica
            if tipo_caracteristica == "Registros":
                modificar_orden_form.registros_parametrizacion_orden.data = texto_caracteristica
            bandera = 0

    if modificar_orden_form.boton_crear_faltante_transformador_medida_orden.data: # Crear faltante transformador de medida
        divActual = "divTransformadorMedida"
        tipo_caracteristica = modificar_orden_form.tipo_faltante_transformador_medida_orden.data
        texto_caracteristica = modificar_orden_form.nombre_faltante_transformador_medida_orden.data
        bandera_creado = orden_controller.anadir_caracteristica("transformador_medida", tipo_caracteristica, texto_caracteristica)
        if not bandera_creado:
            dialogActual = "dialogTransformadorMedida"
        else:
            llenar_choices_caracteristicas(modificar_orden_form)
            modificar_orden_form.nombre_faltante_transformador_medida_orden.data = ""
            if tipo_caracteristica == "Marca TC":
                modificar_orden_form.marca_transformador_medida_orden.data = texto_caracteristica   
            bandera = 0

    if modificar_orden_form.boton_crear_faltante_transformador_distribucion_orden.data: # Crear faltante transformador de distribucion
        divActual = "divTransformadorDistribucion"
        tipo_caracteristica = modificar_orden_form.tipo_faltante_transformador_distribucion_orden.data
        texto_caracteristica = modificar_orden_form.nombre_faltante_transformador_distribucion_orden.data
        bandera_creado = orden_controller.anadir_caracteristica("transformador_distribucion", tipo_caracteristica, texto_caracteristica)
        if not bandera_creado:
            dialogActual = "dialogTransformadorDistribucion"
        else:
            llenar_choices_caracteristicas(modificar_orden_form)
            modificar_orden_form.nombre_faltante_transformador_distribucion_orden.data = ""
            if tipo_caracteristica == "Marca":
                modificar_orden_form.marca_transformador_distribucion_orden.data = texto_caracteristica 
            if tipo_caracteristica == "Tipo":
                modificar_orden_form.tipo_transformador_distribucion_orden.data = texto_caracteristica 
            bandera = 0

    if modificar_orden_form.boton_crear_faltante_sello_orden.data: # Crear faltante sello
        divActual = "divSellos"
        tipo_caracteristica = modificar_orden_form.tipo_faltante_sello_orden.data
        texto_caracteristica = modificar_orden_form.nombre_faltante_sello_orden.data
        bandera_creado = orden_controller.anadir_caracteristica("sello", tipo_caracteristica, texto_caracteristica)
        if not bandera_creado:
            dialogActual = "dialogSello"
        else:
            llenar_choices_caracteristicas(modificar_orden_form)
            modificar_orden_form.nombre_faltante_sello_orden.data = ""
            if tipo_caracteristica == "Tipo":
                modificar_orden_form.tipo_sello_orden.data = texto_caracteristica 
            if tipo_caracteristica == "Ubicación":
                modificar_orden_form.ubicacion_sello_orden.data = texto_caracteristica 
            if tipo_caracteristica == "Estado": 
                modificar_orden_form.estado_sello_orden.data = texto_caracteristica 
            bandera = 0

    if modificar_orden_form.boton_crear_faltante_resultados_orden.data: # Crear faltante resultados
        divActual = "divResultados"
        tipo_caracteristica = modificar_orden_form.tipo_faltante_resultados_orden.data
        texto_caracteristica = modificar_orden_form.nombre_faltante_resultados_orden.data
        bandera_creado = orden_controller.anadir_faltante_resultados(tipo_caracteristica, texto_caracteristica)
        if not bandera_creado:
            dialogActual = "dialogResultados"
        else:
            llenar_anomalias_resultados(modificar_orden_form, numero_orden)
            modificar_orden_form.nombre_faltante_resultados_orden.data = ""
            if tipo_caracteristica == "Anomalía":
                modificar_orden_form.anomalia_encontrada_resultados_orden.data = texto_caracteristica 
            if tipo_caracteristica == "Uso de la energía":
                modificar_orden_form.uso_energia_resultados_orden.data = texto_caracteristica 
            bandera = 0

    if modificar_orden_form.boton_crear_faltante_rdico5_orden.data: # Crear faltante rdico5
        divActual = "divRDICO5"
        tipo_caracteristica = modificar_orden_form.tipo_faltante_rdico5_orden.data
        texto_caracteristica = modificar_orden_form.nombre_faltante_rdico5_orden.data
        bandera_creado = orden_controller.anadir_faltante_rdico5(tipo_caracteristica, texto_caracteristica)
        if not bandera_creado:
            dialogActual = "dialogRDICO5"
        else:
            llenar_acciones_rdico5(modificar_orden_form, numero_orden)
            modificar_orden_form.nombre_faltante_rdico5_orden.data = ""
            if tipo_caracteristica == "Acción":
                modificar_orden_form.lista_acciones_rdico5_orden.data = texto_caracteristica 
            bandera = 0
            
    if modificar_orden_form.boton_eliminar_transformador_medida_orden.data: # Eliminar transformador de medida
        divActual = "divTransformadorMedida"
        id_transformador = int(request.form['input_index_eliminar'])
        orden_controller.eliminar_transformador_medida(id_transformador, rdico2)
        modificar_orden_form.lista_transformadores_medida_orden = orden_controller.obtener_transformadores_medida(rdico2)
        bandera = 0

    if modificar_orden_form.boton_eliminar_transformador_distribucion_orden.data: # Eliminar transformador de distribucion
        divActual = "divTransformadorDistribucion"
        id_transformador = int(request.form['input_index_eliminar'])
        orden_controller.eliminar_transformador_distribucion(id_transformador, rdico2)
        modificar_orden_form.lista_transformadores_distribucion_orden = orden_controller.obtener_transformadores_distribucion(rdico2)
        bandera = 0

    if modificar_orden_form.boton_eliminar_pruebas_orden.data: # Eliminar prueba
        divActual = "divPruebas"
        id_prueba = int(request.form['input_index_eliminar'])
        orden_controller.eliminar_prueba(id_prueba, rdico2)
        modificar_orden_form.lista_pruebas_orden = orden_controller.obtener_pruebas(rdico2)
        bandera = 0
    
    if modificar_orden_form.boton_eliminar_sellos_orden.data: # Eliminar sello
        divActual = "divSellos"
        id_sello = int(request.form['input_index_eliminar'])
        orden_controller.eliminar_sello(id_sello, rdico2)
        modificar_orden_form.lista_sellos_orden = orden_controller.obtener_sellos(rdico2)
        bandera = 0

    if modificar_orden_form.boton_eliminar_lecturas_orden.data: # Eliminar lectura
        divActual = "divLecturas"
        id_lectura = int(request.form['input_index_eliminar'])
        orden_controller.eliminar_lectura(id_lectura, rdico2)
        modificar_orden_form.lista_lecturas_totales_orden = orden_controller.obtener_lecturas(rdico2)
        bandera = 0 

    if modificar_orden_form.boton_eliminar_usos_orden.data: # Eliminar uso
        divActual = "divResultados"
        id_uso = int(request.form['input_index_eliminar'])
        orden_controller.eliminar_uso_energia(id_uso, rdico2)
        modificar_orden_form.lista_usos_energia_orden = orden_controller.obtener_usos_energia(rdico2)
        bandera = 0    

    if modificar_orden_form.boton_eliminar_anomalias_orden.data: # Eliminar anomalia
        divActual = "divResultados"
        id_anomalia = int(request.form['input_index_eliminar'])
        orden_controller.eliminar_anomalia(id_anomalia, rdico2)
        modificar_orden_form.lista_anomalias_orden = orden_controller.obtener_anomalias(rdico2)
        modificar_orden_form.lista_anomalias_acciones_orden = orden_controller.obtener_anomalias_acciones_agregadas(rdico2)
        bandera = 0  

    if modificar_orden_form.boton_eliminar_accion_rdico5_orden.data: # Eliminar accion
        divActual = "divRDICO5"
        id_anomalia = request.form['input_index_anomalia']
        id_accion = request.form['input_index_accion']
        orden_controller.eliminar_accion(id_anomalia, id_accion, rdico2)
        modificar_orden_form.lista_anomalias_acciones_orden = orden_controller.obtener_anomalias_acciones_agregadas(rdico2)
        bandera = 0      

    if modificar_orden_form.boton_eliminar_fotografia_orden.data: # Eliminar fotografia
        divActual = "divFotografias"
        id_fotografia = int(request.form['input_index_eliminar'])
        orden_controller.eliminar_fotografia(id_fotografia, rdico2)
        modificar_orden_form.lista_fotografias = orden_controller.obtener_fotografias(rdico2)
        bandera = 0   

    if modificar_orden_form.guardar.data: # Guardar orden
        guardar_orden(modificar_orden_form, numero_orden)
        bandera = 0

    if modificar_orden_form.cancelar_modificar.data: # Cancelar
        return redirect(url_for('orden'))

    if bandera == 1:
        inicializar_orden(numero_orden, modificar_orden_form) # Inicializar

    if modificar_orden_form.enviar_revision.data: # Enviar a revision orden
        orden = orden_controller.obtener_orden(numero_orden)
        orden.estado = "Revisión"
        orden_controller.guardar_orden(orden)
        flash('Orden enviada a revision','exito')
        return redirect(url_for('orden'))

    params.append(modificar_orden_form)  # params[0]
    llenar_historiales(params, numero_orden)
    return render_template('modificar_orden.html', segment='modificar_orden', params=params, divActual=divActual, dialogActual= dialogActual)

    
def llenar_choices_listas(modificar_orden_form, numero_orden):
    orden = orden_controller.obtener_orden(numero_orden)
    instalacion = instalacion_controller.obtener_instalacion(orden.instalacion_id)
    cliente = cliente_controller.obtener_cliente_por_instalacion(instalacion.numero)
    medidor = medidor_controller.obtener_medidor_por_instalacion(instalacion.numero)
    rdico2 = orden_controller.obtener_rdico2(orden)
    rdico5 = orden_controller.obtener_rdico5(orden)

    llenar_grupo_revisor_control_medicion(modificar_orden_form, numero_orden) # Llenamos texto grupo revisor en resultados
    
    # CHOICES
    llenar_anomalias_resultados(modificar_orden_form, numero_orden) # Llenar choices de anomalias y resultados
    llenar_acciones_rdico5(modificar_orden_form, numero_orden) # Llenar choices de acciones para anomalias    
    llenar_campos_no_modificables(numero_orden, modificar_orden_form)
    llenar_datos_medidor_por_marca(modificar_orden_form, modificar_orden_form.marca_medidor_orden.data)
    llenar_choices_caracteristicas(modificar_orden_form)

    # LISTAS
    modificar_orden_form.lista_transformadores_medida_orden = orden_controller.obtener_transformadores_medida(rdico2)
    modificar_orden_form.lista_transformadores_distribucion_orden = orden_controller.obtener_transformadores_distribucion(rdico2)
    modificar_orden_form.lista_pruebas_orden = orden_controller.obtener_pruebas(rdico2)
    modificar_orden_form.lista_sellos_orden = orden_controller.obtener_sellos(rdico2)
    modificar_orden_form.lista_lecturas_totales_orden = orden_controller.obtener_lecturas(rdico2)
    modificar_orden_form.lista_usos_energia_orden = orden_controller.obtener_usos_energia(rdico2)
    modificar_orden_form.lista_anomalias_orden = orden_controller.obtener_anomalias(rdico2)
    modificar_orden_form.lista_anomalias_acciones_orden = orden_controller.obtener_anomalias_acciones_agregadas(rdico2)
    modificar_orden_form.lista_fotografias = orden_controller.obtener_fotografias(rdico2)
    modificar_orden_form.lista_archivo_lectura = orden_controller.obtener_archivo_lectura(rdico2)
    modificar_orden_form.lista_archivo_perfil = orden_controller.obtener_archivo_perfil(rdico2)

def llenar_historiales(params, numero_orden):
    consumos = []
    demandas = []
    reactivos = []

    orden = orden_controller.obtener_orden(numero_orden)
    instalacion = instalacion_controller.obtener_instalacion(orden.instalacion_id)
    medidor = medidor_controller.obtener_medidor_por_instalacion(instalacion.numero)
    
    if orden and instalacion and medidor:
        consumos = orden_controller.obtener_meses_ordenados(medidor_controller.obtener_historial_consumos(medidor.numero))
        demandas = orden_controller.obtener_meses_ordenados(medidor_controller.obtener_historial_demandas(medidor.numero))
        reactivos = orden_controller.obtener_meses_ordenados(medidor_controller.obtener_historial_reactivos(medidor.numero))

    labels = [row[0] for row in consumos]
    values = [row[1] for row in consumos]
    values2 = [row[1] for row in demandas]
    values3 = [row[1] for row in reactivos]

    params.append(labels)  # params[1]
    params.append(values)  # params[2]
    params.append(values2)  # params[3]
    params.append(values3)  # params[4]

def guardar_orden(modificar_orden_form, numero_orden):
    g = Gestor()

    llenar_campos_no_modificables(numero_orden, modificar_orden_form)
    llenar_datos_medidor_por_marca(modificar_orden_form, modificar_orden_form.marca_medidor_orden.data)
    llenar_choices_caracteristicas(modificar_orden_form)

    orden = orden_controller.obtener_orden(numero_orden)
    instalacion = instalacion_controller.obtener_instalacion(orden.instalacion_id)
    cliente = cliente_controller.obtener_cliente_por_instalacion(instalacion.numero)
    medidor = medidor_controller.obtener_medidor_por_instalacion(instalacion.numero)
    rdico2 = orden_controller.obtener_rdico2(orden)
    rdico5 = orden_controller.obtener_rdico5(orden)

    if orden and instalacion and cliente and medidor and rdico2 and rdico5:

        # Orden
        orden.fechaEjecucion = date.today() 
        orden_controller.guardar_orden(orden)

        # Instalación
        if modificar_orden_form.actualizar_coordenadas_instalacion_orden.data:
            coordenadaX = modificar_orden_form.coordenada_x_instalacion_orden.data
            coordenadaY = modificar_orden_form.coordenada_y_instalacion_orden.data
            utmX = modificar_orden_form.utm_x_instalacion_orden.data
            utmY = modificar_orden_form.utm_y_instalacion_orden.data
            numeroPoste = modificar_orden_form.numero_poste_instalacion_orden.data

            instalacion.coordenadaX = coordenadaX
            instalacion.coordenadaY = coordenadaY
            instalacion.utmX = utmX
            instalacion.utmY = utmY
            instalacion.numeroPoste = numeroPoste

        if modificar_orden_form.nombre_contacto_instalacion_orden.data != "":

            nombre = modificar_orden_form.nombre_contacto_instalacion_orden.data
            telefono = modificar_orden_form.telefono_contacto_instalacion_orden.data
            correo = modificar_orden_form.correo_contacto_instalacion_orden.data
            cargo = modificar_orden_form.cargo_contacto_instalacion_orden.data 

            contacto_tecnico = instalacion_controller.obtener_contacto_tecnico(instalacion)

            if contacto_tecnico:
                contacto_tecnico.nombre = nombre
                contacto_tecnico.telefono = telefono
                contacto_tecnico.correo = correo
                contacto_tecnico.cargo = cargo
            else:
                contacto_tecnico = ContactoTecnico(nombre=nombre, telefono=telefono, correo=correo, cargo=cargo)
                instalacion.contacto_tecnico = contacto_tecnico

        orden_controller.guardar_instalacion(instalacion)

        # Medidor
        numero = modificar_orden_form.numero_medidor_orden.data
        ano = modificar_orden_form.ano_medidor_orden.data
        exactitud = modificar_orden_form.exactitud_medidor_orden.data
        consumokWh = modificar_orden_form.consumo_kwh_medidor_orden.data
        corriente = modificar_orden_form.corriente_medidor_orden.data
        voltaje = modificar_orden_form.voltaje_medidor_orden.data
        constanteK = modificar_orden_form.constantek_medidor_orden.data
        tipo_medicion = modificar_orden_form.tipo_medicion_medidor_orden.data
        conexion = modificar_orden_form.conexion_medidor_orden.data
        marca = modificar_orden_form.marca_medidor_orden.data
        tipo = modificar_orden_form.tipo_medidor_orden.data
        disponible_compensacion = modificar_orden_form.disponible_compensacion_medidor_orden.data
        parametrizado_compensacion = modificar_orden_form.parametrizado_compensacion_medidor_orden.data

        medidor.numero = numero
        medidor.ano = ano
        medidor.exactitud = exactitud
        medidor.consumokWh = consumokWh
        medidor.corriente = corriente
        medidor.voltaje = voltaje
        medidor.constanteK = constanteK
        medidor.tipo_medicion = tipo_medicion
        medidor.conexion = conexion
        medidor.marca = marca
        medidor.tipo = tipo
        medidor.disponible_compensacion = disponible_compensacion
        medidor.parametrizado_compensacion = parametrizado_compensacion


        orden_controller.guardar_medidor(medidor, rdico2)

        # Parametrizacion
        tcs = modificar_orden_form.tcs_parametrizacion_orden.data
        tps = modificar_orden_form.tps_parametrizacion_orden.data
        multiplicador = modificar_orden_form.multiplicador_parametrizacion_orden.data
        compensacionPerdidas = modificar_orden_form.compensacion_perdidas_parametrizacion_orden.data
        registros = modificar_orden_form.registros_parametrizacion_orden.data

        parametrizacion = orden_controller.obtener_parametrizacion(rdico2)

        if parametrizacion:
            parametrizacion.tcs = tcs
            parametrizacion.tps = tps
            parametrizacion.multiplicador = multiplicador
            parametrizacion.compensacionPerdidas = compensacionPerdidas
            parametrizacion.registros = registros
        else:
            parametrizacion = Parametrizacion(tcs = tcs, tps = tps, multiplicador = multiplicador, compensacionPerdidas = compensacionPerdidas, registros = registros)

        orden_controller.guardar_parametrizacion(parametrizacion, rdico2)

        # Verificaciones
        tcsIPrimarioR = modificar_orden_form.tcs_i_primario_r_verificaciones_orden.data
        tcsISecundarioR = modificar_orden_form.tcs_i_secundario_r_verificaciones_orden.data
        relacionTransformacionIR = modificar_orden_form.relacion_transformacion_i_r_verificaciones_orden.data
        tcsIPrimarioS = modificar_orden_form.tcs_i_primario_s_verificaciones_orden.data
        tcsISecundarioS = modificar_orden_form.tcs_i_secundario_s_verificaciones_orden.data
        relacionTransformacionIS = modificar_orden_form.relacion_transformacion_i_s_verificaciones_orden.data
        tcsIPrimarioT = modificar_orden_form.tcs_i_primario_t_verificaciones_orden.data
        tcsISecundarioT = modificar_orden_form.tcs_i_secundario_t_verificaciones_orden.data
        relacionTransformacionIT = modificar_orden_form.relacion_transformacion_i_t_verificaciones_orden.data
        tpsVPrimarioR = modificar_orden_form.tps_v_primario_r_verificaciones_orden.data
        tpsVSecundarioR = modificar_orden_form.tps_v_secundario_r_verificaciones_orden.data
        relacionTransformacionVR = modificar_orden_form.relacion_transformacion_v_r_verificaciones_orden.data
        tpsVPrimarioS = modificar_orden_form.tps_v_primario_s_verificaciones_orden.data
        tpsVSecundarioS = modificar_orden_form.tps_v_secundario_s_verificaciones_orden.data
        relacionTransformacionVS = modificar_orden_form.relacion_transformacion_v_s_verificaciones_orden.data
        tpsVPrimarioT = modificar_orden_form.tps_v_primario_t_verificaciones_orden.data
        tpsVSecundarioT = modificar_orden_form.tps_v_secundario_t_verificaciones_orden.data
        relacionTransformacionVT = modificar_orden_form.relacion_transformacion_v_t_verificaciones_orden.data

        verificacion = orden_controller.obtener_verificacion(rdico2)

        if verificacion:
            verificacion.tcsIPrimarioR = tcsIPrimarioR
            verificacion.tcsISecundarioR = tcsISecundarioR
            verificacion.relacionTransformacionIR = relacionTransformacionIR
            verificacion.tcsIPrimarioS = tcsIPrimarioS
            verificacion.tcsISecundarioS = tcsISecundarioS
            verificacion.relacionTransformacionIS = relacionTransformacionIS
            verificacion.tcsIPrimarioT = tcsIPrimarioT
            verificacion.tcsISecundarioT = tcsISecundarioT
            verificacion.relacionTransformacionIT = relacionTransformacionIT
            verificacion.tpsVPrimarioR = tpsVPrimarioR
            verificacion.tpsVSecundarioR = tpsVSecundarioR
            verificacion.relacionTransformacionVR = relacionTransformacionVR
            verificacion.tpsVPrimarioS = tpsVPrimarioS
            verificacion.tpsVSecundarioS = tpsVSecundarioS
            verificacion.relacionTransformacionVS = relacionTransformacionVS
            verificacion.tpsVPrimarioT = tpsVPrimarioT
            verificacion.tpsVSecundarioT = tpsVSecundarioT
            verificacion.relacionTransformacionVT = relacionTransformacionVT
        else:
            verificacion = Verificacion(tcsIPrimarioR=tcsIPrimarioR, tcsISecundarioR=tcsISecundarioR, relacionTransformacionIR=relacionTransformacionIR,
            tcsIPrimarioS=tcsIPrimarioS, tcsISecundarioS=tcsISecundarioS, relacionTransformacionIS=relacionTransformacionIS,
            tcsIPrimarioT=tcsIPrimarioT, tcsISecundarioT=tcsISecundarioT, relacionTransformacionIT=relacionTransformacionIT,
            tpsVPrimarioR=tpsVPrimarioR, tpsVSecundarioR=tpsVSecundarioR, relacionTransformacionVR=relacionTransformacionVR,
            tpsVPrimarioS=tpsVPrimarioS, tpsVSecundarioS=tpsVSecundarioS, relacionTransformacionVS=relacionTransformacionVS,
            tpsVPrimarioT=tpsVPrimarioT, tpsVSecundarioT=tpsVSecundarioT, relacionTransformacionVT=relacionTransformacionVT)
                
        orden_controller.guardar_verificacion(verificacion, rdico2)

        # Resultados
        resultadoVerificacion =  modificar_orden_form.resultado_verificacion_resultados_orden.data
        nuevoTipoDeTarifa = modificar_orden_form.nuevo_tipo_tarifa_resultados_orden.data
        observaciones = modificar_orden_form.observaciones_resultados_orden.data

        rdico2.resultadoVerificacion = resultadoVerificacion
        rdico2.nuevoTipoDeTarifa = nuevoTipoDeTarifa
        rdico2.observaciones = observaciones
        rdico2.fecha = request.form['fecha_resultados_orden']

        orden_controller.guardar_rdico2(rdico2)

        
        # RDICO5
        kWh = modificar_orden_form.kwh_medidor_rdico5_orden.data
        kvarh = modificar_orden_form.kvarh_medidor_rdico5_orden.data
        kW = modificar_orden_form.kW_medidor_rdico5_orden.data
        perfilCarga = modificar_orden_form.perfildecarga_medidor_rdico5_orden.data
        compensacion = modificar_orden_form.compensacion_medidor_rdico5_orden.data
        descripcionMedidor = modificar_orden_form.descripcion_medidor_rdico5_orden.data
        aluminio = modificar_orden_form.aluminio_acometida_rdico5_orden.data
        antihurto = modificar_orden_form.antihurto_acometida_rdico5_orden.data
        subterranea = modificar_orden_form.subterranea_acometida_rdico5_orden.data
        descripcionAcometida = modificar_orden_form.descripcion_acometida_rdico5_orden.data
        tableroMetalico = modificar_orden_form.tablero_metalico_rdico5_orden.data
        descripcionTableroMetalico = modificar_orden_form.descripcion_tablero_metalico_rdico5_orden.data
        tableroAntihurto = modificar_orden_form.tablero_antihurto_rdico5_orden.data
        descripciontableroAntihurto = modificar_orden_form.descripcion_tablero_antihurto_rdico5_orden.data
        cableNumero6 = modificar_orden_form.cable_numero6_rdico5_orden.data
        descripcionCableNumero6 = modificar_orden_form.descripcion_cable_numero6_rdico5_orden.data
        conductorNumero8 = modificar_orden_form.conductor_numero8_rdico5_orden.data
        descripcionConductorNumero8 = modificar_orden_form.descripcion_conductor_numero8_rdico5_orden.data
        protectorTermico = modificar_orden_form.protector_termico_rdico5_orden.data
        descripcionProtectorTermico = modificar_orden_form.descripcion_protector_termico_rdico5_orden.data
        candadoMaster = modificar_orden_form.candado_master_rdico5_orden.data
        descripcionCandadoMaster = modificar_orden_form.descripcion_candado_master_rdico5_orden.data
        TPs = modificar_orden_form.tps_rdico5_orden.data
        descripcionTPs = modificar_orden_form.descripcion_tps_rdico5_orden.data
        TCs = modificar_orden_form.tcs_rdico5_orden.data
        descripcionTCs = modificar_orden_form.descripcion_tcs_rdico5_orden.data
        tarfia = modificar_orden_form.tarifa_rdico5_orden.data
        descripcionTarifa = modificar_orden_form.descripcion_tarifa_rdico5_orden.data
        otros = modificar_orden_form.otros_cambio_materiales_rdico5_orden.data

        cambio_material = orden_controller.cambio_material(rdico5)
        
        if cambio_material:
            cambio_material.kWh = kWh
            cambio_material.kvarh = kvarh
            cambio_material.kW = kW
            cambio_material.perfilCarga = perfilCarga
            cambio_material.compensacion = compensacion
            cambio_material.descripcionMedidor = descripcionMedidor
            cambio_material.aluminio = aluminio
            cambio_material.antihurto = antihurto
            cambio_material.subterranea = subterranea
            cambio_material.descripcionAcometida = descripcionAcometida
            cambio_material.tableroMetalico = tableroMetalico
            cambio_material.descripcionTableroMetalico = descripcionTableroMetalico
            cambio_material.tableroAntihurto = tableroAntihurto
            cambio_material.descripciontableroAntihurto = descripciontableroAntihurto
            cambio_material.cableNumero6 = cableNumero6
            cambio_material.descripcionCableNumero6 = descripcionCableNumero6
            cambio_material.conductorNumero8 = conductorNumero8
            cambio_material.descripcionConductorNumero8 = descripcionConductorNumero8
            cambio_material.protectorTermico = protectorTermico
            cambio_material.descripcionProtectorTermico = descripcionProtectorTermico
            cambio_material.candadoMaster = candadoMaster
            cambio_material.descripcionCandadoMaster = descripcionCandadoMaster
            cambio_material.TPs = TPs
            cambio_material.descripcionTPs = descripcionTPs
            cambio_material.TCs = TCs
            cambio_material.descripcionTCs = descripcionTCs
            cambio_material.tarfia = tarfia
            cambio_material.descripcionTarifa = descripcionTarifa
            cambio_material.otros = otros
        else:
            cambio_material = CambioMaterial(kWh=kWh, kvarh=kvarh, kW=kW,
            perfilCarga=perfilCarga, compensacion=compensacion, descripcionMedidor=descripcionMedidor,
            aluminio=aluminio, antihurto=antihurto, subterranea=subterranea, descripcionAcometida=descripcionAcometida,
            tableroMetalico=tableroMetalico, descripcionTableroMetalico=descripcionTableroMetalico, tableroAntihurto=tableroAntihurto,
            descripciontableroAntihurto=descripciontableroAntihurto, cableNumero6=cableNumero6,
            descripcionCableNumero6=descripcionCableNumero6, conductorNumero8=conductorNumero8,
            descripcionConductorNumero8=descripcionConductorNumero8, protectorTermico=protectorTermico,
            descripcionProtectorTermico=descripcionProtectorTermico, candadoMaster=candadoMaster,
            descripcionCandadoMaster=descripcionCandadoMaster, TPs=TPs, descripcionTPs=descripcionTPs,
            TCs=TCs, descripcionTCs=descripcionTCs, tarfia=tarfia, descripcionTarifa=descripcionTarifa, otros=otros)

        orden_controller.guardar_cambio_material(cambio_material, rdico5)
        

        rdico5.fecha = request.form['fecha_rdico5_orden']
        orden_controller.guardar_rdico5(rdico5)

    flash('Orden guardada correctamente','exito')


def inicializar_orden(numero_orden, modificar_orden_form):

    llenar_campos_no_modificables(numero_orden, modificar_orden_form)
    # Obtenemos choices de otras partes del form
    llenar_choices_caracteristicas(modificar_orden_form)

    orden = orden_controller.obtener_orden(numero_orden)
    instalacion = instalacion_controller.obtener_instalacion(orden.instalacion_id)
    cliente = cliente_controller.obtener_cliente_por_instalacion(instalacion.numero)
    medidor = medidor_controller.obtener_medidor_por_instalacion(instalacion.numero)
    rdico2 = orden_controller.obtener_rdico2(orden)
    rdico5 = orden_controller.obtener_rdico5(orden)

    if orden:

        if instalacion:
            modificar_orden_form.coordenada_x_instalacion_orden.data = instalacion.coordenadaX
            modificar_orden_form.coordenada_y_instalacion_orden.data = instalacion.coordenadaY
            modificar_orden_form.utm_x_instalacion_orden.data = instalacion.utmX
            modificar_orden_form.utm_y_instalacion_orden.data = instalacion.utmY
            modificar_orden_form.numero_poste_instalacion_orden.data = instalacion.numeroPoste

            contacto_tecnico = orden_controller.obtener_contacto_tecnico(instalacion)

            if contacto_tecnico:
                modificar_orden_form.nombre_contacto_instalacion_orden.data = contacto_tecnico.nombre
                modificar_orden_form.telefono_contacto_instalacion_orden.data = contacto_tecnico.telefono
                modificar_orden_form.correo_contacto_instalacion_orden.data = contacto_tecnico.correo
                modificar_orden_form.cargo_contacto_instalacion_orden.data = contacto_tecnico.cargo

        if medidor:
            llenar_datos_medidor_por_marca(modificar_orden_form, medidor.marca)
            modificar_orden_form.numero_medidor_orden.data = medidor.numero   
            modificar_orden_form.consumo_kwh_medidor_orden.data = medidor.consumokWh
            modificar_orden_form.marca_medidor_orden.data = medidor.marca
            modificar_orden_form.tipo_medidor_orden.data = medidor.tipo
            modificar_orden_form.ano_medidor_orden.data = medidor.ano
            modificar_orden_form.exactitud_medidor_orden.data = medidor.exactitud
            modificar_orden_form.corriente_medidor_orden.data = medidor.corriente
            modificar_orden_form.voltaje_medidor_orden.data = medidor.voltaje
            modificar_orden_form.constantek_medidor_orden.data = medidor.constanteK
            modificar_orden_form.tipo_medicion_medidor_orden.data = medidor.tipo_medicion
            modificar_orden_form.conexion_medidor_orden.data = medidor.conexion
            modificar_orden_form.disponible_compensacion_medidor_orden.data = medidor.disponible_compensacion
            modificar_orden_form.parametrizado_compensacion_medidor_orden.data = medidor.parametrizado_compensacion
            modificar_orden_form.factor_potencia_medidor_orden.data = medidor.factor_potencia
        
        parametrizacion = orden_controller.obtener_parametrizacion(rdico2)
        if parametrizacion:
            modificar_orden_form.tcs_parametrizacion_orden.data = parametrizacion.tcs  
            modificar_orden_form.tps_parametrizacion_orden.data = parametrizacion.tps  
            modificar_orden_form.multiplicador_parametrizacion_orden.data = parametrizacion.multiplicador  
            modificar_orden_form.compensacion_perdidas_parametrizacion_orden.data = parametrizacion.compensacionPerdidas  
            modificar_orden_form.registros_parametrizacion_orden.data = parametrizacion.registros  
        
        modificar_orden_form.lista_transformadores_medida_orden = orden_controller.obtener_transformadores_medida(rdico2)
        modificar_orden_form.lista_transformadores_distribucion_orden = orden_controller.obtener_transformadores_distribucion(rdico2)
        modificar_orden_form.lista_pruebas_orden = orden_controller.obtener_pruebas(rdico2)

        verificacion = orden_controller.obtener_verificacion(rdico2)
        if verificacion:
            modificar_orden_form.tcs_i_primario_r_verificaciones_orden.data = verificacion.tcsIPrimarioR 
            modificar_orden_form.tcs_i_secundario_r_verificaciones_orden.data = verificacion.tcsISecundarioR 
            modificar_orden_form.relacion_transformacion_i_r_verificaciones_orden.data = verificacion.relacionTransformacionIR 
            modificar_orden_form.tcs_i_primario_s_verificaciones_orden.data = verificacion.tcsIPrimarioS 
            modificar_orden_form.tcs_i_secundario_s_verificaciones_orden.data = verificacion.tcsISecundarioS 
            modificar_orden_form.relacion_transformacion_i_s_verificaciones_orden.data = verificacion.relacionTransformacionIS 
            modificar_orden_form.tcs_i_primario_t_verificaciones_orden.data = verificacion.tcsIPrimarioT 
            modificar_orden_form.tcs_i_secundario_t_verificaciones_orden.data = verificacion.tcsISecundarioT 
            modificar_orden_form.relacion_transformacion_i_t_verificaciones_orden.data = verificacion.relacionTransformacionIT 
            modificar_orden_form.tps_v_primario_r_verificaciones_orden.data = verificacion.tpsVPrimarioR 
            modificar_orden_form.tps_v_secundario_r_verificaciones_orden.data = verificacion.tpsVSecundarioR 
            modificar_orden_form.relacion_transformacion_v_r_verificaciones_orden.data = verificacion.relacionTransformacionVR 
            modificar_orden_form.tps_v_primario_s_verificaciones_orden.data = verificacion.tpsVPrimarioS 
            modificar_orden_form.tps_v_secundario_s_verificaciones_orden.data = verificacion.tpsVSecundarioS 
            modificar_orden_form.relacion_transformacion_v_s_verificaciones_orden.data = verificacion.relacionTransformacionVS 
            modificar_orden_form.tps_v_primario_t_verificaciones_orden.data = verificacion.tpsVPrimarioT 
            modificar_orden_form.tps_v_secundario_t_verificaciones_orden.data = verificacion.tpsVSecundarioT 
            modificar_orden_form.relacion_transformacion_v_t_verificaciones_orden.data = verificacion.relacionTransformacionVT 

        modificar_orden_form.lista_sellos_orden = orden_controller.obtener_sellos(rdico2)
        modificar_orden_form.lista_lecturas_totales_orden = orden_controller.obtener_lecturas(rdico2)

        modificar_orden_form.resultado_verificacion_resultados_orden.data = rdico2.resultadoVerificacion
        modificar_orden_form.nuevo_tipo_tarifa_resultados_orden.data = rdico2.nuevoTipoDeTarifa
        modificar_orden_form.observaciones_resultados_orden.data = rdico2.observaciones

        modificar_orden_form.lista_usos_energia_orden = orden_controller.obtener_usos_energia(rdico2)

        modificar_orden_form.lista_anomalias_orden = orden_controller.obtener_anomalias(rdico2)
        modificar_orden_form.lista_anomalias_acciones_orden = orden_controller.obtener_anomalias_acciones_agregadas(rdico2)

        modificar_orden_form.lista_fotografias = orden_controller.obtener_fotografias(rdico2)
        modificar_orden_form.lista_archivo_lectura = orden_controller.obtener_archivo_lectura(rdico2)
        modificar_orden_form.lista_archivo_perfil = orden_controller.obtener_archivo_perfil(rdico2)


        cambio_material = orden_controller.obtener_cambio_material(rdico5)
        if cambio_material:
            modificar_orden_form.kwh_medidor_rdico5_orden.data = cambio_material.kWh
            modificar_orden_form.kvarh_medidor_rdico5_orden.data = cambio_material.kvarh
            modificar_orden_form.kW_medidor_rdico5_orden.data = cambio_material.kW
            modificar_orden_form.perfildecarga_medidor_rdico5_orden.data = cambio_material.perfilCarga
            modificar_orden_form.compensacion_medidor_rdico5_orden.data = cambio_material.compensacion
            modificar_orden_form.descripcion_medidor_rdico5_orden.data = cambio_material.descripcionMedidor
            modificar_orden_form.aluminio_acometida_rdico5_orden.data = cambio_material.aluminio
            modificar_orden_form.antihurto_acometida_rdico5_orden.data = cambio_material.antihurto
            modificar_orden_form.subterranea_acometida_rdico5_orden.data = cambio_material.subterranea
            modificar_orden_form.descripcion_acometida_rdico5_orden.data = cambio_material.descripcionAcometida
            modificar_orden_form.tablero_metalico_rdico5_orden.data = cambio_material.tableroMetalico
            modificar_orden_form.descripcion_tablero_metalico_rdico5_orden.data = cambio_material.descripcionTableroMetalico
            modificar_orden_form.tablero_antihurto_rdico5_orden.data = cambio_material.tableroAntihurto
            modificar_orden_form.descripcion_tablero_antihurto_rdico5_orden.data = cambio_material.descripciontableroAntihurto
            modificar_orden_form.cable_numero6_rdico5_orden.data = cambio_material.cableNumero6
            modificar_orden_form.descripcion_cable_numero6_rdico5_orden.data = cambio_material.descripcionCableNumero6
            modificar_orden_form.conductor_numero8_rdico5_orden.data = cambio_material.conductorNumero8
            modificar_orden_form.descripcion_conductor_numero8_rdico5_orden.data = cambio_material.descripcionConductorNumero8
            modificar_orden_form.protector_termico_rdico5_orden.data = cambio_material.protectorTermico
            modificar_orden_form.descripcion_protector_termico_rdico5_orden.data = cambio_material.descripcionProtectorTermico
            modificar_orden_form.candado_master_rdico5_orden.data = cambio_material.candadoMaster
            modificar_orden_form.kwh_medidor_rdico5_orden.descripcion_candado_master_rdico5_ordendata = cambio_material.descripcionCandadoMaster
            modificar_orden_form.tps_rdico5_orden.data = cambio_material.TPs
            modificar_orden_form.descripcion_tps_rdico5_orden.data = cambio_material.descripcionTPs
            modificar_orden_form.tcs_rdico5_orden.data = cambio_material.TCs
            modificar_orden_form.descripcion_tcs_rdico5_orden.data = cambio_material.descripcionTCs
            modificar_orden_form.tarifa_rdico5_orden.data = cambio_material.tarfia
            modificar_orden_form.kwh_medidor_rdico5_orden.descripcion_tarifa_rdico5_orden = cambio_material.descripcionTarifa
            modificar_orden_form.otros_cambio_materiales_rdico5_orden.data = cambio_material.otros

def llenar_choices_caracteristicas(modificar_orden_form):
    dict_choices = orden_controller.cargar_choices_caracteristicas()

    modificar_orden_form.multiplicador_parametrizacion_orden.choices = dict_choices[
        'multiplicador']
    modificar_orden_form.registros_parametrizacion_orden.choices = dict_choices['registros']
    modificar_orden_form.marca_transformador_medida_orden.choices = dict_choices['marcatc']
    modificar_orden_form.marca_transformador_distribucion_orden.choices = dict_choices[
        'marcatransdis']
    modificar_orden_form.tipo_transformador_distribucion_orden.choices = dict_choices[
        'tipotransdis']
    modificar_orden_form.tipo_sello_orden.choices = dict_choices['tiposello']
    modificar_orden_form.ubicacion_sello_orden.choices = dict_choices['ubicacionsello']
    modificar_orden_form.estado_sello_orden.choices = dict_choices['estadosello']
    modificar_orden_form.resultado_verificacion_resultados_orden.choices = dict_choices[
        'funcionamientoresultados']
    asistente = orden_controller.obtener_asistente_actual()
    if asistente:
        modificar_orden_form.control_medicion_rdico5_orden.data = asistente.nombre

def llenar_datos_medidor_por_marca(modificar_orden_form, marca_medidor):
    lista_medidores_temp = medidor_controller.obtener_medidores_temp_por_marca(
        marca_medidor)

    lista_marcas = medidor_controller.obtener_todas_marcas_medidor_temp()

    for tupla in modificar_orden_form.lista_marcas_faltantes_creadas:
        lista_marcas.append(tupla)

    modificar_orden_form.marca_medidor_orden.choices = lista_marcas

    if [marca for marca in lista_marcas if marca[0] == marca_medidor]:
        modificar_orden_form.marca_medidor_orden.data = marca_medidor

    lista_tipos = []
    lista_anos = []
    lista_corrientes = []
    lista_voltajes = []
    lista_constantesk = []
    lista_conexiones = []
    lista_exactitudes = []

    for medidortemp in lista_medidores_temp:
        if not [tipo for tipo in lista_tipos if tipo[0] == medidortemp.tipo]:
            lista_tipos.append((medidortemp.tipo, medidortemp.tipo))
        if not [ano for ano in lista_anos if ano[0] == medidortemp.ano]:
            lista_anos.append((medidortemp.ano, medidortemp.ano))
        if not [corriente for corriente in lista_corrientes if corriente[0] == medidortemp.corriente]:
            lista_corrientes.append(
                    (medidortemp.corriente, medidortemp.corriente))
        if not [voltaje for voltaje in lista_voltajes if voltaje[0] == medidortemp.voltaje]:
            lista_voltajes.append(
                    (medidortemp.voltaje, medidortemp.voltaje))
        if not [constantek for constantek in lista_constantesk if constantek[0] == medidortemp.constanteK]:
            lista_constantesk.append(
                    (medidortemp.constanteK, medidortemp.constanteK))
        if not [conexion for conexion in lista_conexiones if conexion[0] == medidortemp.conexion]:
            lista_conexiones.append(
                    (medidortemp.conexion, medidortemp.conexion))
        if not [exactitud for exactitud in lista_exactitudes if exactitud[0] == medidortemp.exactitud]:
            lista_exactitudes.append((medidortemp.exactitud, medidortemp.exactitud))

    for tupla in modificar_orden_form.lista_tipos_faltantes_creadas:
        lista_tipos.append(tupla)

    for tupla in modificar_orden_form.lista_anos_faltantes_creadas:
        lista_anos.append(tupla)

    for tupla in modificar_orden_form.lista_exactitud_faltantes_creadas:
        lista_exactitudes.append(tupla)      

    for tupla in modificar_orden_form.lista_corriente_faltantes_creadas:
        lista_corrientes.append(tupla)

    for tupla in modificar_orden_form.lista_voltaje_faltantes_creadas:
        lista_voltajes.append(tupla)

    for tupla in modificar_orden_form.lista_constantek_faltantes_creadas:
        lista_constantesk.append(tupla)  

    for tupla in modificar_orden_form.lista_conexion_faltantes_creadas:
        lista_conexiones.append(tupla)

    modificar_orden_form.tipo_medidor_orden.choices = lista_tipos
    modificar_orden_form.ano_medidor_orden.choices = lista_anos
    modificar_orden_form.corriente_medidor_orden.choices = lista_corrientes
    modificar_orden_form.voltaje_medidor_orden.choices = lista_voltajes
    modificar_orden_form.constantek_medidor_orden.choices = lista_constantesk
    modificar_orden_form.conexion_medidor_orden.choices = lista_conexiones
    modificar_orden_form.exactitud_medidor_orden.choices = lista_exactitudes




def llenar_campos_no_modificables(numero_orden, modificar_orden_form):
    orden = orden_controller.obtener_orden(numero_orden)
    instalacion = instalacion_controller.obtener_instalacion(
        orden.instalacion_id)
    cliente = cliente_controller.obtener_cliente_por_instalacion(
        instalacion.numero)
    medidor = medidor_controller.obtener_medidor_por_instalacion(
        instalacion.numero)
    
    if orden:
        # No se puede moficiar
        modificar_orden_form.numero_orden.data = numero_orden
        modificar_orden_form.estado_orden.data = orden.estado
        modificar_orden_form.comentario_inicial_orden.data = orden.comentarioInicial

        if cliente:  # No se puede moficiar
            modificar_orden_form.identificacion_cliente_orden.data = cliente.identificacion
            modificar_orden_form.razon_social_cliente_orden.data = cliente.razonSocial
            modificar_orden_form.cuenta_cliente_orden.data = cliente.cuenta
            modificar_orden_form.tipo_tarifa_cliente_orden.data = cliente.tipoTarifa
            modificar_orden_form.correo_cliente_orden.data = cliente.correo
            modificar_orden_form.telefono_cliente_orden.data = cliente.telefono
            modificar_orden_form.direccion_cliente_orden.data = cliente.direccion
            modificar_orden_form.mru_cliente_orden.data = cliente.mru
            modificar_orden_form.fm_cliente_orden.data = cliente.fm

        if instalacion:
            modificar_orden_form.numero_instalacion_orden.data = instalacion.numero

        if medidor:
            modificar_orden_form.cc_medidor_orden.data = medidor.cc
    
def vaciar_campos_transformador_medida(modificar_orden_form):
    modificar_orden_form.numero_serie_transformador_medida_orden.data = ""
    modificar_orden_form.numero_empresa_transformador_medida_orden.data = ""
    modificar_orden_form.relacion_transformacion_transformador_medida_orden.data = ""
    modificar_orden_form.s_transformador_medida_orden.data = ""
    modificar_orden_form.exactitud_transformador_medida_orden.data = ""
    modificar_orden_form.ano_transformador_medida_orden.data = ""
    modificar_orden_form.sellos_encontrados_transformador_medida_orden.data = ""

def vaciar_campos_transformador_distribucion(modificar_orden_form):
    modificar_orden_form.numero_transformador_distribucion_orden.data = ""
    modificar_orden_form.s_transformador_distribucion_orden.data = 0.00
    modificar_orden_form.v_transformador_distribucion_orden.data = 0.00
    modificar_orden_form.ano_transformador_distribucion_orden.data = ""
    modificar_orden_form.zcc_transformador_distribucion_orden.data = ""
    modificar_orden_form.conexion_transformador_distribucion_orden.data = ""

def vaciar_campos_pruebas(modificar_orden_form):
    modificar_orden_form.rfase1_pruebas_orden.data = Decimal(0)
    modificar_orden_form.sfase2_pruebas_orden.data = Decimal(0)
    modificar_orden_form.tfase3_pruebas_orden.data = Decimal(0)
    modificar_orden_form.numero_revoluciones_pruebas_orden.data = Decimal(0)
    modificar_orden_form.tiempo_pruebas_orden.data = Decimal(0)

def vaciar_campos_lecturas(modificar_orden_form):
    modificar_orden_form.a_horarias_lectura_orden.data = Decimal(0)
    modificar_orden_form.b_horarias_lectura_orden.data = Decimal(0)
    modificar_orden_form.c_horarias_lectura_orden.data = Decimal(0)
    modificar_orden_form.d_horarias_lectura_orden.data = Decimal(0)
    modificar_orden_form.a_demandas_lectura_orden.data = Decimal(0)
    modificar_orden_form.b_demandas_lectura_orden.data = Decimal(0)
    modificar_orden_form.c_demandas_lectura_orden.data = Decimal(0)
    modificar_orden_form.d_demandas_lectura_orden.data = Decimal(0)
    modificar_orden_form.kvarh_lectura_orden.data = Decimal(0)

def vaciar_campos_sellos(modificar_orden_form):
    modificar_orden_form.sello_sello_orden.data = ""

def vaciar_campos_anomalia(modificar_orden_form):
    modificar_orden_form.anomalia_encontrada_resultados_orden.data = ""

def vaciar_campos_uso(modificar_orden_form):
    modificar_orden_form.uso_energia_resultados_orden.data = ""

def llenar_grupo_revisor_control_medicion(modificar_orden_form, numero_orden):
    texto_grupo_revisor = ""
    texto_grupo_revisor = orden_controller.obtener_texto_grupo_revisor(numero_orden)
    modificar_orden_form.grupo_revisor_resultados_orden.data = texto_grupo_revisor

def llenar_anomalias_resultados(modificar_orden_form, numero_orden):
    modificar_orden_form.uso_energia_resultados_orden.choices = orden_controller.obtener_usos()
    modificar_orden_form.anomalia_encontrada_resultados_orden.choices = orden_controller.obtener_anomalias_choices()

def llenar_acciones_rdico5(modificar_orden_form, numero_orden):
    modificar_orden_form.lista_acciones_rdico5_orden.choices = orden_controller.obtener_acciones()