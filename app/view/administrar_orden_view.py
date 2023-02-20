from flask.templating import render_template
from flask_login.utils import login_required
from app import app
from app.forms.administrar_orden_form import AdministrarOrdenForm
from app.forms.admin_orden_form import AdminOrdenForm
from controller import administrar_orden_controller
from decimal import *
from flask import render_template, url_for, request
from flask_login import login_required
from flask import flash
from werkzeug.utils import redirect

from controller import orden_controller
from controller import instalacion_controller
from controller import cliente_controller
from controller import medidor_controller
from controller import usuarios_controller
from app.forms.orden_form import OrdenForm
from app import app
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


import copy
import folium
from datetime import date

from model.verificacion import Verificacion

@app.route('/administrarorden.html', methods=['GET', 'POST'])
@login_required
def administrarorden():
    privilegio = usuarios_controller.verificar_privilegios("AdministrarOrden")
    if privilegio:
        params = []

        administrar_orden_form = AdminOrdenForm()
        ordenes = administrar_orden_controller.obtenerOrdenes()

        params.append(ordenes) # params[0]
        params.append(administrar_orden_form) # params[1]

        if administrar_orden_form.administrar.data:
            numero_orden = request.form['input_orden_administrar']

            if numero_orden == "0":
                flash('Debe seleccionar una orden','error')
            else:
                return redirect(url_for('administrar_orden', numero_orden=numero_orden)) 
        
        return render_template('administrarorden.html', segment='administrarorden', params=params)
    return redirect(url_for('index'))

@app.route('/administrar_orden/<int:numero_orden>', methods=['GET', 'POST'])
@login_required
def administrar_orden(numero_orden):
    params = []
    divActual = ""
    dialogActual = ""
    administrar_orden_form = AdministrarOrdenForm()
    bandera = 1

    orden = orden_controller.obtener_orden(numero_orden)
    instalacion = instalacion_controller.obtener_instalacion(orden.instalacion_id)
    cliente = cliente_controller.obtener_cliente_por_instalacion(instalacion.numero)
    medidor = medidor_controller.obtener_medidor_por_instalacion(instalacion.numero)
    rdico2 = orden_controller.obtener_rdico2(orden)
    rdico5 = orden_controller.obtener_rdico5(orden)

    llenar_grupo_revisor_control_medicion(administrar_orden_form, numero_orden) # Llenamos texto grupo revisor en resultados
    llenar_anomalias_resultados(administrar_orden_form, rdico2) # Llenar choices de anomalias y resultados
    llenar_acciones_rdico5(administrar_orden_form, numero_orden) # Llenar choices de acciones para anomalias    
    llenar_anomalias_agregadas(administrar_orden_form, rdico2) # Llenar lista de anomalias asociadas a la orden 
    llenar_anomalias_acciones_agregadas(administrar_orden_form, rdico2) # Llenar lista de anomalias con sus acciones asociadas a la orden

    if administrar_orden_form.boton_agregar_accion_rdico5.data: # Agregar accion
        divActual = "divRDICO5"
        llenar_campos_no_modificables(numero_orden, administrar_orden_form)
        llenar_datos_medidor_por_marca(administrar_orden_form, administrar_orden_form.marca_medidor_orden.data)
        llenar_choices_caracteristicas(administrar_orden_form)
        
        orden = orden_controller.obtener_orden(numero_orden)
        rdico2 = orden_controller.obtener_rdico2(orden)

        llenar_anomalias_agregadas(administrar_orden_form, rdico2)

        id_anomalia = int(request.form['input_index_anomalia'])
        index_accion =  int(administrar_orden_form.lista_acciones_rdico5_orden.data) -1
        id_accion = administrar_orden_form.lista_acciones_rdico5_orden.choices[index_accion][0]
        
        anomalia = administrar_orden_form.lista_anomalias_orden[id_anomalia]
        accion = orden_controller.obtener_accion(id_accion)

        if anomalia and accion and rdico2 and orden:
            orden_controller.crear_accion(rdico2, anomalia, accion)
        llenar_anomalias_acciones_agregadas(administrar_orden_form, rdico2)
        bandera = 0

    if administrar_orden_form.boton_crear_faltante_rdico5_orden.data: # Crear faltante rdico5
        divActual = "divRDICO5"
        llenar_campos_no_modificables(numero_orden, administrar_orden_form)
        llenar_datos_medidor_por_marca(administrar_orden_form, administrar_orden_form.marca_medidor_orden.data)
        llenar_choices_caracteristicas(administrar_orden_form)
        tipo_caracteristica = administrar_orden_form.tipo_faltante_rdico5_orden.data
        texto_caracteristica = administrar_orden_form.nombre_faltante_rdico5_orden.data

        bandera_creado = orden_controller.anadir_faltante_rdico5(tipo_caracteristica, texto_caracteristica)

        if not bandera_creado:
            dialogActual = "dialogRDICO5"
        else:
            llenar_acciones_rdico5(administrar_orden_form, numero_orden)
            administrar_orden_form.nombre_faltante_rdico5_orden.data = ""
            if tipo_caracteristica == "Acción":
                administrar_orden_form.lista_acciones_rdico5_orden.data = texto_caracteristica 
            bandera = 0

    if administrar_orden_form.boton_eliminar_accion_rdico5_orden.data: # Eliminar accion
        divActual = "divRDICO5"
        llenar_campos_no_modificables(numero_orden, administrar_orden_form)
        llenar_datos_medidor_por_marca(administrar_orden_form, administrar_orden_form.marca_medidor_orden.data)
        llenar_choices_caracteristicas(administrar_orden_form)

        id_anomalia = request.form['input_index_anomalia']
        id_accion = request.form['input_index_accion']

        anomalia = orden_controller.obtener_anomalia_id(id_anomalia)
        accion = orden_controller.obtener_accion(id_accion)

        orden_controller.eliminar_accion(rdico2, anomalia, accion)
        llenar_anomalias_acciones_agregadas(administrar_orden_form, rdico2)
     
        bandera = 0    

    if administrar_orden_form.guardar.data:
        guardar_orden(administrar_orden_form, numero_orden)
        bandera = 0 

    if administrar_orden_form.cerrar_sap.data:
        orden = orden_controller.obtener_orden(numero_orden)
        orden.estado = "Cerrada"
        orden.fechaCierre = date.today()
        orden_controller.guardar_orden(orden)
        flash('Orden cerrada en SAP correctamente','exito')
        return redirect(url_for('administrarorden'))

    if administrar_orden_form.cancelar_administrar.data:
        return redirect(url_for('administrarorden'))

    if bandera == 1:
        inicializar_orden(numero_orden, administrar_orden_form)

    if administrar_orden_form.volver_revision.data:
        orden = orden_controller.obtener_orden(numero_orden)
        orden.estado = "Liberada"
        orden_controller.guardar_orden(orden)
        flash('Orden liberada correctamente','exito')
        return redirect(url_for('administrarorden'))

    params.append(administrar_orden_form)  # params[0]

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

    # Saber si es asistente admin o asistente jefe
    bandera_asistente_admin = orden_controller.obtener_bandera_tipo_asistente_rdico5()
    if bandera_asistente_admin:
        administrar_orden_form.kwh_medidor_rdico5_orden.render_kw = {'disabled': ''}
        administrar_orden_form.kvarh_medidor_rdico5_orden.render_kw = {'disabled': ''}
        administrar_orden_form.kW_medidor_rdico5_orden.render_kw = {'disabled': ''}
        administrar_orden_form.perfildecarga_medidor_rdico5_orden.render_kw = {'disabled': ''}
        administrar_orden_form.compensacion_medidor_rdico5_orden.render_kw = {'disabled': ''}
        administrar_orden_form.descripcion_medidor_rdico5_orden.render_kw = {'disabled': ''}
        administrar_orden_form.aluminio_acometida_rdico5_orden.render_kw = {'disabled': ''}
        administrar_orden_form.antihurto_acometida_rdico5_orden.render_kw = {'disabled': ''}
        administrar_orden_form.subterranea_acometida_rdico5_orden.render_kw = {'disabled': ''}
        administrar_orden_form.descripcion_acometida_rdico5_orden.render_kw = {'disabled': ''}
        administrar_orden_form.tablero_metalico_rdico5_orden.render_kw = {'disabled': ''}
        administrar_orden_form.descripcion_tablero_metalico_rdico5_orden.render_kw = {'disabled': ''}
        administrar_orden_form.cable_numero6_rdico5_orden.render_kw = {'disabled': ''}
        administrar_orden_form.descripcion_cable_numero6_rdico5_orden.render_kw = {'disabled': ''}
        administrar_orden_form.protector_termico_rdico5_orden.render_kw = {'disabled': ''}
        administrar_orden_form.descripcion_protector_termico_rdico5_orden.render_kw = {'disabled': ''}
        administrar_orden_form.tps_rdico5_orden.render_kw = {'disabled': ''}
        administrar_orden_form.descripcion_tps_rdico5_orden.render_kw = {'disabled': ''}
        administrar_orden_form.tarifa_rdico5_orden.render_kw = {'disabled': ''}
        administrar_orden_form.descripcion_tarifa_rdico5_orden.render_kw = {'disabled': ''}
        administrar_orden_form.tablero_antihurto_rdico5_orden.render_kw = {'disabled': ''}
        administrar_orden_form.descripcion_tablero_antihurto_rdico5_orden.render_kw = {'disabled': ''}
        administrar_orden_form.conductor_numero8_rdico5_orden.render_kw = {'disabled': ''}
        administrar_orden_form.descripcion_conductor_numero8_rdico5_orden.render_kw = {'disabled': ''}
        administrar_orden_form.candado_master_rdico5_orden.render_kw = {'disabled': ''}
        administrar_orden_form.descripcion_candado_master_rdico5_orden.render_kw = {'disabled': ''}
        administrar_orden_form.tcs_rdico5_orden.render_kw = {'disabled': ''}
        administrar_orden_form.descripcion_tcs_rdico5_orden.render_kw = {'disabled': ''}
        administrar_orden_form.otros_cambio_materiales_rdico5_orden.render_kw = {'disabled': ''}
        administrar_orden_form.lista_acciones_rdico5_orden.render_kw = {'disabled': ''}
        administrar_orden_form.boton_agregar_accion_rdico5.render_kw = {'disabled': ''}


    params.append(bandera_asistente_admin) # params[5]

    return render_template('administrar_orden.html', segment='administrar_orden', params=params, divActual=divActual, dialogActual= dialogActual)

def inicializar_orden(numero_orden, administrar_orden_form):

    llenar_campos_no_modificables(numero_orden, administrar_orden_form)
    # Obtenemos choices de otras partes del form
    llenar_choices_caracteristicas(administrar_orden_form)

    orden = orden_controller.obtener_orden(numero_orden)
    instalacion = instalacion_controller.obtener_instalacion(orden.instalacion_id)
    cliente = cliente_controller.obtener_cliente_por_instalacion(instalacion.numero)
    medidor = medidor_controller.obtener_medidor_por_instalacion(instalacion.numero)
    rdico2 = orden_controller.obtener_rdico2(orden)
    rdico5 = orden_controller.obtener_rdico5(orden)

    if orden:

        if instalacion:
            administrar_orden_form.coordenada_x_instalacion_orden.data = instalacion.coordenadaX
            administrar_orden_form.coordenada_y_instalacion_orden.data = instalacion.coordenadaY
            administrar_orden_form.utm_x_instalacion_orden.data = instalacion.utmX
            administrar_orden_form.utm_y_instalacion_orden.data = instalacion.utmY
            administrar_orden_form.numero_poste_instalacion_orden.data = instalacion.numeroPoste

            contacto_tecnico = orden_controller.obtener_contacto_tecnico(instalacion)

            if contacto_tecnico:
                administrar_orden_form.nombre_contacto_instalacion_orden.data = contacto_tecnico.nombre
                administrar_orden_form.telefono_contacto_instalacion_orden.data = contacto_tecnico.telefono
                administrar_orden_form.correo_contacto_instalacion_orden.data = contacto_tecnico.correo
                administrar_orden_form.cargo_contacto_instalacion_orden.data = contacto_tecnico.cargo

        if medidor:
            llenar_datos_medidor_por_marca(administrar_orden_form, medidor.marca)
            administrar_orden_form.numero_medidor_orden.data = medidor.numero   
            administrar_orden_form.consumo_kwh_medidor_orden.data = medidor.consumokWh
            administrar_orden_form.marca_medidor_orden.data = medidor.marca
            administrar_orden_form.tipo_medidor_orden.data = medidor.tipo
            administrar_orden_form.ano_medidor_orden.data = medidor.ano
            administrar_orden_form.exactitud_medidor_orden.data = medidor.exactitud
            administrar_orden_form.corriente_medidor_orden.data = medidor.corriente
            administrar_orden_form.voltaje_medidor_orden.data = medidor.voltaje
            administrar_orden_form.constantek_medidor_orden.data = medidor.constanteK
            administrar_orden_form.tipo_medicion_medidor_orden.data = medidor.tipo_medicion
            administrar_orden_form.conexion_medidor_orden.data = medidor.conexion
            administrar_orden_form.disponible_compensacion_medidor_orden.data = medidor.disponible_compensacion
            administrar_orden_form.parametrizado_compensacion_medidor_orden.data = medidor.parametrizado_compensacion
            administrar_orden_form.factor_potencia_medidor_orden.data = medidor.factor_potencia
        
        parametrizacion = orden_controller.obtener_parametrizacion(rdico2)
        if parametrizacion:
            administrar_orden_form.tcs_parametrizacion_orden.data = parametrizacion.tcs  
            administrar_orden_form.tps_parametrizacion_orden.data = parametrizacion.tps  
            administrar_orden_form.multiplicador_parametrizacion_orden.data = parametrizacion.multiplicador  
            administrar_orden_form.compensacion_perdidas_parametrizacion_orden.data = parametrizacion.compensacionPerdidas  
            administrar_orden_form.registros_parametrizacion_orden.data = parametrizacion.registros  
        
        administrar_orden_form.lista_transformadores_medida_orden = orden_controller.obtener_transformadores_medida(rdico2)
        administrar_orden_form.lista_transformadores_distribucion_orden = orden_controller.obtener_transformadores_distribucion(rdico2)
        administrar_orden_form.lista_pruebas_orden = orden_controller.obtener_pruebas(rdico2)

        verificacion = orden_controller.obtener_verificacion(rdico2)
        if verificacion:
            administrar_orden_form.tcs_i_primario_r_verificaciones_orden.data = verificacion.tcsIPrimarioR 
            administrar_orden_form.tcs_i_secundario_r_verificaciones_orden.data = verificacion.tcsISecundarioR 
            administrar_orden_form.relacion_transformacion_i_r_verificaciones_orden.data = verificacion.relacionTransformacionIR 
            administrar_orden_form.tcs_i_primario_s_verificaciones_orden.data = verificacion.tcsIPrimarioS 
            administrar_orden_form.tcs_i_secundario_s_verificaciones_orden.data = verificacion.tcsISecundarioS 
            administrar_orden_form.relacion_transformacion_i_s_verificaciones_orden.data = verificacion.relacionTransformacionIS 
            administrar_orden_form.tcs_i_primario_t_verificaciones_orden.data = verificacion.tcsIPrimarioT 
            administrar_orden_form.tcs_i_secundario_t_verificaciones_orden.data = verificacion.tcsISecundarioT 
            administrar_orden_form.relacion_transformacion_i_t_verificaciones_orden.data = verificacion.relacionTransformacionIT 
            administrar_orden_form.tps_v_primario_r_verificaciones_orden.data = verificacion.tpsVPrimarioR 
            administrar_orden_form.tps_v_secundario_r_verificaciones_orden.data = verificacion.tpsVSecundarioR 
            administrar_orden_form.relacion_transformacion_v_r_verificaciones_orden.data = verificacion.relacionTransformacionVR 
            administrar_orden_form.tps_v_primario_s_verificaciones_orden.data = verificacion.tpsVPrimarioS 
            administrar_orden_form.tps_v_secundario_s_verificaciones_orden.data = verificacion.tpsVSecundarioS 
            administrar_orden_form.relacion_transformacion_v_s_verificaciones_orden.data = verificacion.relacionTransformacionVS 
            administrar_orden_form.tps_v_primario_t_verificaciones_orden.data = verificacion.tpsVPrimarioT 
            administrar_orden_form.tps_v_secundario_t_verificaciones_orden.data = verificacion.tpsVSecundarioT 
            administrar_orden_form.relacion_transformacion_v_t_verificaciones_orden.data = verificacion.relacionTransformacionVT 

        administrar_orden_form.lista_sellos_orden = orden_controller.obtener_sellos(rdico2)
        administrar_orden_form.lista_lecturas_totales_orden = orden_controller.obtener_lecturas(rdico2)

        administrar_orden_form.resultado_verificacion_resultados_orden.data = rdico2.resultadoVerificacion
        administrar_orden_form.nuevo_tipo_tarifa_resultados_orden.data = rdico2.nuevoTipoDeTarifa
        administrar_orden_form.observaciones_resultados_orden.data = rdico2.observaciones

        administrar_orden_form.lista_usos_energia_orden = orden_controller.obtener_usos_energia(rdico2)

        llenar_anomalias_agregadas(administrar_orden_form, rdico2)
        llenar_anomalias_acciones_agregadas(administrar_orden_form, rdico2)

        cambio_material = orden_controller.obtener_cambio_material(rdico5)
        if cambio_material:
            administrar_orden_form.kwh_medidor_rdico5_orden.data = cambio_material.kWh
            administrar_orden_form.kvarh_medidor_rdico5_orden.data = cambio_material.kvarh
            administrar_orden_form.kW_medidor_rdico5_orden.data = cambio_material.kW
            administrar_orden_form.perfildecarga_medidor_rdico5_orden.data = cambio_material.perfilCarga
            administrar_orden_form.compensacion_medidor_rdico5_orden.data = cambio_material.compensacion
            administrar_orden_form.descripcion_medidor_rdico5_orden.data = cambio_material.descripcionMedidor
            administrar_orden_form.aluminio_acometida_rdico5_orden.data = cambio_material.aluminio
            administrar_orden_form.antihurto_acometida_rdico5_orden.data = cambio_material.antihurto
            administrar_orden_form.subterranea_acometida_rdico5_orden.data = cambio_material.subterranea
            administrar_orden_form.descripcion_acometida_rdico5_orden.data = cambio_material.descripcionAcometida
            administrar_orden_form.tablero_metalico_rdico5_orden.data = cambio_material.tableroMetalico
            administrar_orden_form.descripcion_tablero_metalico_rdico5_orden.data = cambio_material.descripcionTableroMetalico
            administrar_orden_form.tablero_antihurto_rdico5_orden.data = cambio_material.tableroAntihurto
            administrar_orden_form.descripcion_tablero_antihurto_rdico5_orden.data = cambio_material.descripciontableroAntihurto
            administrar_orden_form.cable_numero6_rdico5_orden.data = cambio_material.cableNumero6
            administrar_orden_form.descripcion_cable_numero6_rdico5_orden.data = cambio_material.descripcionCableNumero6
            administrar_orden_form.conductor_numero8_rdico5_orden.data = cambio_material.conductorNumero8
            administrar_orden_form.descripcion_conductor_numero8_rdico5_orden.data = cambio_material.descripcionConductorNumero8
            administrar_orden_form.protector_termico_rdico5_orden.data = cambio_material.protectorTermico
            administrar_orden_form.descripcion_protector_termico_rdico5_orden.data = cambio_material.descripcionProtectorTermico
            administrar_orden_form.candado_master_rdico5_orden.data = cambio_material.candadoMaster
            administrar_orden_form.kwh_medidor_rdico5_orden.descripcion_candado_master_rdico5_ordendata = cambio_material.descripcionCandadoMaster
            administrar_orden_form.tps_rdico5_orden.data = cambio_material.TPs
            administrar_orden_form.descripcion_tps_rdico5_orden.data = cambio_material.descripcionTPs
            administrar_orden_form.tcs_rdico5_orden.data = cambio_material.TCs
            administrar_orden_form.descripcion_tcs_rdico5_orden.data = cambio_material.descripcionTCs
            administrar_orden_form.tarifa_rdico5_orden.data = cambio_material.tarfia
            administrar_orden_form.kwh_medidor_rdico5_orden.descripcion_tarifa_rdico5_orden = cambio_material.descripcionTarifa
            administrar_orden_form.otros_cambio_materiales_rdico5_orden.data = cambio_material.otros

def llenar_choices_caracteristicas(administrar_orden_form):
    dict_choices = orden_controller.cargar_choices_caracteristicas()

    administrar_orden_form.multiplicador_parametrizacion_orden.choices = dict_choices[
        'multiplicador']
    administrar_orden_form.registros_parametrizacion_orden.choices = dict_choices['registros']
    administrar_orden_form.marca_transformador_medida_orden.choices = dict_choices['marcatc']
    administrar_orden_form.marca_transformador_distribucion_orden.choices = dict_choices[
        'marcatransdis']
    administrar_orden_form.tipo_transformador_distribucion_orden.choices = dict_choices[
        'tipotransdis']
    administrar_orden_form.tipo_sello_orden.choices = dict_choices['tiposello']
    administrar_orden_form.ubicacion_sello_orden.choices = dict_choices['ubicacionsello']
    administrar_orden_form.estado_sello_orden.choices = dict_choices['estadosello']
    administrar_orden_form.resultado_verificacion_resultados_orden.choices = dict_choices[
        'funcionamientoresultados']
    asistente = orden_controller.obtener_asistente_actual()
    if asistente:
        administrar_orden_form.control_medicion_rdico5_orden.data = asistente.nombre

def llenar_datos_medidor_por_marca(administrar_orden_form, marca_medidor):
    lista_medidores_temp = medidor_controller.obtener_medidores_temp_por_marca(
        marca_medidor)

    lista_marcas = medidor_controller.obtener_todas_marcas_medidor_temp()

    for tupla in administrar_orden_form.lista_marcas_faltantes_creadas:
        lista_marcas.append(tupla)

    administrar_orden_form.marca_medidor_orden.choices = lista_marcas

    if [marca for marca in lista_marcas if marca[0] == marca_medidor]:
        administrar_orden_form.marca_medidor_orden.data = marca_medidor

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

    for tupla in administrar_orden_form.lista_tipos_faltantes_creadas:
        lista_tipos.append(tupla)

    for tupla in administrar_orden_form.lista_anos_faltantes_creadas:
        lista_anos.append(tupla)

    for tupla in administrar_orden_form.lista_exactitud_faltantes_creadas:
        lista_exactitudes.append(tupla)      

    for tupla in administrar_orden_form.lista_corriente_faltantes_creadas:
        lista_corrientes.append(tupla)

    for tupla in administrar_orden_form.lista_voltaje_faltantes_creadas:
        lista_voltajes.append(tupla)

    for tupla in administrar_orden_form.lista_constantek_faltantes_creadas:
        lista_constantesk.append(tupla)  

    for tupla in administrar_orden_form.lista_conexion_faltantes_creadas:
        lista_conexiones.append(tupla)

    administrar_orden_form.tipo_medidor_orden.choices = lista_tipos
    administrar_orden_form.ano_medidor_orden.choices = lista_anos
    administrar_orden_form.corriente_medidor_orden.choices = lista_corrientes
    administrar_orden_form.voltaje_medidor_orden.choices = lista_voltajes
    administrar_orden_form.constantek_medidor_orden.choices = lista_constantesk
    administrar_orden_form.conexion_medidor_orden.choices = lista_conexiones
    administrar_orden_form.exactitud_medidor_orden.choices = lista_exactitudes

def guardar_orden(administrar_orden_form, numero_orden):

    llenar_campos_no_modificables(numero_orden, administrar_orden_form)
    llenar_datos_medidor_por_marca(administrar_orden_form, administrar_orden_form.marca_medidor_orden.data)
    llenar_choices_caracteristicas(administrar_orden_form)

    orden = orden_controller.obtener_orden(numero_orden)
    instalacion = instalacion_controller.obtener_instalacion(orden.instalacion_id)
    cliente = cliente_controller.obtener_cliente_por_instalacion(instalacion.numero)
    medidor = medidor_controller.obtener_medidor_por_instalacion(instalacion.numero)
    rdico2 = orden_controller.obtener_rdico2(orden)
    rdico5 = orden_controller.obtener_rdico5(orden)

    if orden and instalacion and cliente and medidor and rdico2 and rdico5:

        # Orden
        orden.fechaGestion = date.today() 
        orden_controller.guardar_orden(orden)
        
        # RDICO5
        kWh = administrar_orden_form.kwh_medidor_rdico5_orden.data
        kvarh = administrar_orden_form.kvarh_medidor_rdico5_orden.data
        kW = administrar_orden_form.kW_medidor_rdico5_orden.data
        perfilCarga = administrar_orden_form.perfildecarga_medidor_rdico5_orden.data
        compensacion = administrar_orden_form.compensacion_medidor_rdico5_orden.data
        descripcionMedidor = administrar_orden_form.descripcion_medidor_rdico5_orden.data
        aluminio = administrar_orden_form.aluminio_acometida_rdico5_orden.data
        antihurto = administrar_orden_form.antihurto_acometida_rdico5_orden.data
        subterranea = administrar_orden_form.subterranea_acometida_rdico5_orden.data
        descripcionAcometida = administrar_orden_form.descripcion_acometida_rdico5_orden.data
        tableroMetalico = administrar_orden_form.tablero_metalico_rdico5_orden.data
        descripcionTableroMetalico = administrar_orden_form.descripcion_tablero_metalico_rdico5_orden.data
        tableroAntihurto = administrar_orden_form.tablero_antihurto_rdico5_orden.data
        descripciontableroAntihurto = administrar_orden_form.descripcion_tablero_antihurto_rdico5_orden.data
        cableNumero6 = administrar_orden_form.cable_numero6_rdico5_orden.data
        descripcionCableNumero6 = administrar_orden_form.descripcion_cable_numero6_rdico5_orden.data
        conductorNumero8 = administrar_orden_form.conductor_numero8_rdico5_orden.data
        descripcionConductorNumero8 = administrar_orden_form.descripcion_conductor_numero8_rdico5_orden.data
        protectorTermico = administrar_orden_form.protector_termico_rdico5_orden.data
        descripcionProtectorTermico = administrar_orden_form.descripcion_protector_termico_rdico5_orden.data
        candadoMaster = administrar_orden_form.candado_master_rdico5_orden.data
        descripcionCandadoMaster = administrar_orden_form.descripcion_candado_master_rdico5_orden.data
        TPs = administrar_orden_form.tps_rdico5_orden.data
        descripcionTPs = administrar_orden_form.descripcion_tps_rdico5_orden.data
        TCs = administrar_orden_form.tcs_rdico5_orden.data
        descripcionTCs = administrar_orden_form.descripcion_tcs_rdico5_orden.data
        tarfia = administrar_orden_form.tarifa_rdico5_orden.data
        descripcionTarifa = administrar_orden_form.descripcion_tarifa_rdico5_orden.data
        otros = administrar_orden_form.otros_cambio_materiales_rdico5_orden.data

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


def llenar_campos_no_modificables(numero_orden, administrar_orden_form):
    orden = orden_controller.obtener_orden(numero_orden)
    instalacion = instalacion_controller.obtener_instalacion(
        orden.instalacion_id)
    cliente = cliente_controller.obtener_cliente_por_instalacion(
        instalacion.numero)
    medidor = medidor_controller.obtener_medidor_por_instalacion(
        instalacion.numero)
    
    if orden:
        # No se puede moficiar
        administrar_orden_form.numero_orden.data = numero_orden
        administrar_orden_form.estado_orden.data = orden.estado
        administrar_orden_form.comentario_inicial_orden.data = orden.comentarioInicial

        if cliente:  # No se puede moficiar
            administrar_orden_form.identificacion_cliente_orden.data = cliente.identificacion
            administrar_orden_form.razon_social_cliente_orden.data = cliente.razonSocial
            administrar_orden_form.cuenta_cliente_orden.data = cliente.cuenta
            administrar_orden_form.tipo_tarifa_cliente_orden.data = cliente.tipoTarifa
            administrar_orden_form.correo_cliente_orden.data = cliente.correo
            administrar_orden_form.telefono_cliente_orden.data = cliente.telefono
            administrar_orden_form.direccion_cliente_orden.data = cliente.direccion
            administrar_orden_form.mru_cliente_orden.data = cliente.mru
            administrar_orden_form.fm_cliente_orden.data = cliente.fm

        if instalacion:
            administrar_orden_form.numero_instalacion_orden.data = instalacion.numero

        if medidor:
            administrar_orden_form.cc_medidor_orden.data = medidor.cc
    
def vaciar_campos_transformador_medida(administrar_orden_form):
    administrar_orden_form.numero_serie_transformador_medida_orden.data = ""
    administrar_orden_form.numero_empresa_transformador_medida_orden.data = ""
    administrar_orden_form.relacion_transformacion_transformador_medida_orden.data = ""
    administrar_orden_form.s_transformador_medida_orden.data = ""
    administrar_orden_form.exactitud_transformador_medida_orden.data = ""
    administrar_orden_form.ano_transformador_medida_orden.data = ""
    administrar_orden_form.sellos_encontrados_transformador_medida_orden.data = ""

def vaciar_campos_transformador_distribucion(administrar_orden_form):
    administrar_orden_form.numero_transformador_distribucion_orden.data = ""
    administrar_orden_form.s_transformador_distribucion_orden.data = Decimal(0)
    administrar_orden_form.v_transformador_distribucion_orden.data = Decimal(0)
    administrar_orden_form.ano_transformador_distribucion_orden.data = ""

def vaciar_campos_pruebas(administrar_orden_form):
    administrar_orden_form.rfase1_pruebas_orden.data = Decimal(0)
    administrar_orden_form.sfase2_pruebas_orden.data = Decimal(0)
    administrar_orden_form.tfase3_pruebas_orden.data = Decimal(0)
    administrar_orden_form.numero_revoluciones_pruebas_orden.data = Decimal(0)
    administrar_orden_form.tiempo_pruebas_orden.data = Decimal(0)

def vaciar_campos_lecturas(administrar_orden_form):
    administrar_orden_form.a_horarias_lectura_orden.data = Decimal(0)
    administrar_orden_form.b_horarias_lectura_orden.data = Decimal(0)
    administrar_orden_form.c_horarias_lectura_orden.data = Decimal(0)
    administrar_orden_form.d_horarias_lectura_orden.data = Decimal(0)
    administrar_orden_form.a_demandas_lectura_orden.data = Decimal(0)
    administrar_orden_form.b_demandas_lectura_orden.data = Decimal(0)
    administrar_orden_form.c_demandas_lectura_orden.data = Decimal(0)
    administrar_orden_form.d_demandas_lectura_orden.data = Decimal(0)
    administrar_orden_form.kvarh_lectura_orden.data = Decimal(0)

def vaciar_campos_sellos(administrar_orden_form):
    administrar_orden_form.sello_sello_orden.data = ""

def vaciar_campos_anomalia(administrar_orden_form):
    administrar_orden_form.anomalia_encontrada_resultados_orden.data = ""

def vaciar_campos_uso(administrar_orden_form):
    administrar_orden_form.uso_energia_resultados_orden.data = ""

def llenar_grupo_revisor_control_medicion(administrar_orden_form, numero_orden):
    texto_grupo_revisor = ""
    texto_grupo_revisor = orden_controller.obtener_texto_grupo_revisor(numero_orden)
    administrar_orden_form.grupo_revisor_resultados_orden.data = texto_grupo_revisor

def llenar_anomalias_resultados(administrar_orden_form, rdico2):
    administrar_orden_form.uso_energia_resultados_orden.choices = orden_controller.obtener_usos()
    administrar_orden_form.anomalia_encontrada_resultados_orden.choices = orden_controller.obtener_anomalias_choices()

def llenar_acciones_rdico5(administrar_orden_form, numero_orden):
    administrar_orden_form.lista_acciones_rdico5_orden.choices = orden_controller.obtener_acciones()

def llenar_anomalias_agregadas(administrar_orden_form, rdico2):
    administrar_orden_form.lista_anomalias_orden = orden_controller.obtener_anomalias(rdico2)

def llenar_anomalias_acciones_agregadas(administrar_orden_form, rdico2):
    administrar_orden_form.lista_anomalias_acciones_orden = orden_controller.obtener_anomalias_acciones_agregadas(rdico2)