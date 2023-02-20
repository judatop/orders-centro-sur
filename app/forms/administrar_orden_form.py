from html.entities import html5
from typing import Text
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from peewee import IntegerField
from wtforms import StringField, SubmitField, FileField, SelectField, BooleanField, DecimalField, form
from wtforms.fields.choices import SelectMultipleField
from wtforms.fields.datetime import DateTimeField
from wtforms.fields.simple import MultipleFileField, TextAreaField
from wtforms.validators import DataRequired
from wtforms import Form
from controller import administracion_controller


class AdministrarOrdenForm(FlaskForm):

    # ORDEN
    numero_orden = StringField('Número de orden', render_kw={'disabled': ''})
    estado_orden = StringField('Estado', render_kw={'disabled': ''})
    comentario_inicial_orden = StringField('Comentario inicial', render_kw={'disabled': ''})


    # CLIENTE
    identificacion_cliente_orden = StringField('Identificación', render_kw={'disabled': ''})
    razon_social_cliente_orden = StringField('Razón social', render_kw={'disabled': ''})
    cuenta_cliente_orden = StringField('Cuenta', render_kw={'disabled': ''})
    tipo_tarifa_cliente_orden = StringField('Tipo de tarifa', render_kw={'disabled': ''})
    correo_cliente_orden = StringField('Correo Electrónico', render_kw={'disabled': ''})
    telefono_cliente_orden = StringField('Teléfono', render_kw={'disabled': ''})
    direccion_cliente_orden = TextAreaField('Dirección (servicio)', render_kw={'disabled': ''})
    dmin_kw_cliente_orden = DecimalField('Dmín [kW]', render_kw={'disabled': ''})
    dmax_kw_cliente_orden = DecimalField('Dmáx [kW]', render_kw={'disabled': ''})
    fp_cliente_orden = DecimalField('FP', render_kw={'disabled': ''})
    mru_cliente_orden = StringField('MRU', render_kw={'disabled': ''})
    fm_cliente_orden = StringField('FM', render_kw={'disabled': ''})


    # INSTALACION
    numero_instalacion_orden = StringField('Número de instalación', render_kw={'disabled': ''})
    coordenada_x_instalacion_orden = DecimalField('Coordenada X', places=10, render_kw={'disabled': ''})
    coordenada_y_instalacion_orden = DecimalField('Coordenada Y', places=10, render_kw={'disabled': ''})
    utm_x_instalacion_orden = DecimalField('UTM X', places=10, render_kw={'disabled': ''})
    utm_y_instalacion_orden = DecimalField('UTM Y', places=10, render_kw={'disabled': ''})
    numero_poste_instalacion_orden = StringField('Número de poste', render_kw={'disabled': ''})
    actualizar_coordenadas_instalacion_orden = BooleanField('Actualizar coordenadas', render_kw={'disabled': ''})

    # CONTACTO TECNICO
    nombre_contacto_instalacion_orden = StringField('Nombre', render_kw={'disabled': ''})
    telefono_contacto_instalacion_orden = StringField('Teléfono', render_kw={'disabled': ''})
    correo_contacto_instalacion_orden = StringField('Correo', render_kw={'disabled': ''})
    cargo_contacto_instalacion_orden = StringField('Cargo', render_kw={'disabled': ''})

    # MEDIDOR
    cc_medidor_orden = StringField('Cuenta contrato (CC)', render_kw={'disabled': ''})
    consumo_kwh_medidor_orden = DecimalField('Consumo kWh', render_kw={'disabled': ''})
    numero_medidor_orden = StringField('Número de medidor', render_kw={'disabled': ''})
    marca_medidor_orden = SelectField('Marca', choices=[], render_kw={'disabled': ''})
    tipo_medidor_orden = SelectField('Tipo', choices=[], render_kw={'disabled': ''})
    ano_medidor_orden = SelectField('Año', choices=[], render_kw={'disabled': ''})
    exactitud_medidor_orden = SelectField('Exactitud', choices=[], render_kw={'disabled': ''})
    corriente_medidor_orden = SelectField('Corriente', choices=[], render_kw={'disabled': ''})
    voltaje_medidor_orden = SelectField('Voltaje', choices=[], render_kw={'disabled': ''})
    constantek_medidor_orden = SelectField('Constante K', choices=[], render_kw={'disabled': ''})
    factor_potencia_medidor_orden = DecimalField('Factor de potencia', render_kw={'disabled': ''})
    tipo_medicion_medidor_orden = SelectField('Tipo de medición',
                                              choices=[("Directo", "Directo"),
                                                       ("Indirecto", "Indirecto"),
                                                       ("Semidirecto","Semidirecto")], render_kw={'disabled': ''})
    conexion_medidor_orden = SelectField('Conexión', choices=[], render_kw={'disabled': ''})
    disponible_compensacion_medidor_orden = BooleanField('Disponible', render_kw={'disabled': ''})
    parametrizado_compensacion_medidor_orden = BooleanField('Parametrizado', render_kw={'disabled': ''})
    lista_marcas_faltantes_creadas = []
    lista_tipos_faltantes_creadas = []
    lista_anos_faltantes_creadas = []
    lista_exactitud_faltantes_creadas = []
    lista_corriente_faltantes_creadas = []
    lista_voltaje_faltantes_creadas = []
    lista_constantek_faltantes_creadas = []
    lista_tipo_medicion_faltantes_creadas = []
    lista_conexion_faltantes_creadas = []


    # PARAMETRIZACIÓN
    tcs_parametrizacion_orden = DecimalField('TCS', default=0, render_kw={'disabled': ''})
    tps_parametrizacion_orden = DecimalField('TPS', default=0, render_kw={'disabled': ''})
    multiplicador_parametrizacion_orden = SelectField('Multiplicador', choices=[], render_kw={'disabled': ''})
    compensacion_perdidas_parametrizacion_orden = SelectField('Compensación de pérdidas', choices=[(0,0),(1.02, 1.02)], render_kw={'disabled': ''})
    registros_parametrizacion_orden = SelectField('Registros', choices=[], render_kw={'disabled': ''})

    # TRANSFORMADOR DE MEDIDA 
    numero_serie_transformador_medida_orden = StringField('# Serie', render_kw={'disabled': ''})
    numero_empresa_transformador_medida_orden = StringField('# Empresa', render_kw={'disabled': ''})
    marca_transformador_medida_orden = SelectField('Marca', choices=[], render_kw={'disabled': ''})
    relacion_transformacion_transformador_medida_orden = StringField('Relación', render_kw={'disabled': ''})
    s_transformador_medida_orden = StringField('S[VA]', render_kw={'disabled': ''})
    exactitud_transformador_medida_orden = StringField('Exactitud', render_kw={'disabled': ''})
    ano_transformador_medida_orden = StringField('Año', render_kw={'disabled': ''})
    sellos_encontrados_transformador_medida_orden = StringField('Sellos', render_kw={'disabled': ''})
    tipo_transformador_medida_orden = SelectField('Tipo', choices=[("TC","TC"),("TP","TP"),("TCS COMBINADO","TCS COMBINADO"),("TPS COMBINADO","TPS COMBINADO")], render_kw={'disabled': ''})
    anadir_transformador_medida_orden = SubmitField('+', render_kw={'disabled': ''})
    lista_transformadores_medida_orden = []
    index_eliminar_transformador_medida_orden = -1

    # TRANSFORMADOR DE DISTRIBUCIÓN 
    numero_transformador_distribucion_orden = StringField('Número', render_kw={'disabled': ''})
    marca_transformador_distribucion_orden = SelectField('Marca', choices=[], render_kw={'disabled': ''})
    tipo_transformador_distribucion_orden = SelectField('Tipo', choices=[], render_kw={'disabled': ''})
    s_transformador_distribucion_orden = DecimalField('S [kVA]', render_kw={'disabled': ''})
    v_transformador_distribucion_orden = DecimalField('[V]', render_kw={'disabled': ''})
    ano_transformador_distribucion_orden = StringField('Año', render_kw={'disabled': ''})
    zcc_transformador_distribucion_orden = StringField('Zcc', render_kw={'disabled': ''})
    conexion_transformador_distribucion_orden = StringField('Conexión', render_kw={'disabled': ''})

    anadir_transformador_distribucion_orden = SubmitField('+', render_kw={'disabled': ''})
    lista_transformadores_distribucion_orden = []

    # PRUEBAS
    unidad_electrica_pruebas_orden = SelectField('Tipo', choices=[("P[kW]","P[kW]"),("S[kva]","S[kva]"),
    ("Q[kvar]","Q[kvar]"), ("Fp [cosɸ]","Fp [cosɸ]"), ("V[V]","V[V]"), ("I[A]","I[A]")], render_kw={'disabled': ''})
    rfase1_pruebas_orden = DecimalField('R (Fase 1)', places=2, render_kw={'disabled': ''})
    sfase2_pruebas_orden = DecimalField('S (Fase 2)', places=2, render_kw={'disabled': ''})
    tfase3_pruebas_orden = DecimalField('T (Fase 3)', places=2, render_kw={'disabled': ''})
    numero_revoluciones_pruebas_orden = DecimalField('No. Revol', places=2, render_kw={'disabled': ''})
    tiempo_pruebas_orden = DecimalField('Tiempo [s]', places=2, render_kw={'disabled': ''})
    anadir_prueba_pruebas_orden = SubmitField('+', render_kw={'disabled': ''})
    lista_pruebas_orden = []

    # VERIFICACIONES
    tcs_i_primario_r_verificaciones_orden = DecimalField(places=2, render_kw={'disabled': ''})
    tcs_i_secundario_r_verificaciones_orden = DecimalField(places=2, render_kw={'disabled': ''})
    relacion_transformacion_i_r_verificaciones_orden = DecimalField(places=2, render_kw={'disabled': ''})
    tcs_i_primario_s_verificaciones_orden = DecimalField(places=2, render_kw={'disabled': ''})
    tcs_i_secundario_s_verificaciones_orden = DecimalField(places=2, render_kw={'disabled': ''})
    relacion_transformacion_i_s_verificaciones_orden = DecimalField(places=2, render_kw={'disabled': ''})
    tcs_i_primario_t_verificaciones_orden = DecimalField(places=2, render_kw={'disabled': ''})
    tcs_i_secundario_t_verificaciones_orden = DecimalField(places=2, render_kw={'disabled': ''})
    relacion_transformacion_i_t_verificaciones_orden = DecimalField(places=2, render_kw={'disabled': ''})
    tps_v_primario_r_verificaciones_orden = DecimalField(places=2, render_kw={'disabled': ''})
    tps_v_secundario_r_verificaciones_orden = DecimalField(places=2, render_kw={'disabled': ''})
    relacion_transformacion_v_r_verificaciones_orden = DecimalField(places=2, render_kw={'disabled': ''})
    tps_v_primario_s_verificaciones_orden = DecimalField(places=2, render_kw={'disabled': ''})
    tps_v_secundario_s_verificaciones_orden = DecimalField(places=2, render_kw={'disabled': ''})
    relacion_transformacion_v_s_verificaciones_orden = DecimalField(places=2, render_kw={'disabled': ''})
    tps_v_primario_t_verificaciones_orden = DecimalField(places=2, render_kw={'disabled': ''})
    tps_v_secundario_t_verificaciones_orden = DecimalField(places=2, render_kw={'disabled': ''})
    relacion_transformacion_v_t_verificaciones_orden = DecimalField(places=2, render_kw={'disabled': ''})

    # SELLOS
    modelo_sello_orden = SelectField('Modelo', choices=[("Registrados/Encontrados","Registrados/Encontrados"),("Finales/Luego de la revisión","Finales/Luego de la revisión")], render_kw={'disabled': ''})
    sello_sello_orden = StringField('Sello', render_kw={'disabled': ''})
    tipo_sello_orden = SelectField('Tipo', choices=[], render_kw={'disabled': ''})
    ubicacion_sello_orden = SelectField('Ubicación', choices=[], render_kw={'disabled': ''})
    estado_sello_orden = SelectField('Estado', choices=[], render_kw={'disabled': ''})
    anadir_sello_orden = SubmitField('+', render_kw={'disabled': ''})
    lista_sellos_orden = []

    # RESULTADOS
    resultado_verificacion_resultados_orden = SelectField('Funcionamiento del sistema de medición', choices=[], render_kw={'disabled': ''})
    uso_energia_resultados_orden = SelectField('Usos de la energía verificado', choices=[], render_kw={'disabled': ''})
    anadir_uso_energia_resultados_orden = SubmitField('+', render_kw={'disabled': ''})
    anomalia_encontrada_resultados_orden = SelectField('Anomalías encontradas', choices=[], render_kw={'disabled': ''})
    anadir_anomalia_encontrada_resultados_orden = SubmitField('+', render_kw={'disabled': ''})
    nuevo_tipo_tarifa_resultados_orden = StringField('Nuevo tipo de Tarifa', render_kw={'disabled': ''})
    observaciones_resultados_orden = TextAreaField('Observaciones', render_kw={'disabled': ''})
    grupo_revisor_resultados_orden = StringField('Grupo Revisor', render_kw={'disabled': ''} )
    lista_usos_energia_orden = []
    lista_anomalias_orden = []
    
    
    # FOTOGRAFIAS
    archivo_fotografias_fotografia_orden = MultipleFileField(render_kw={'disabled': ''})

    # LECTURAS
    archivo_lectura_lecturas_orden = FileField(render_kw={'disabled': ''})
    tipo_lectura_orden = SelectField('Modelo', choices=[("Previas","Previas"),("Actuales","Actuales")], render_kw={'disabled': ''})
    kvarh_lectura_orden =  DecimalField('kvarh', render_kw={'disabled': ''})
    a_horarias_lectura_orden =  DecimalField('A', places=2, render_kw={'disabled': ''})
    b_horarias_lectura_orden =  DecimalField('B', places=2, render_kw={'disabled': ''})
    c_horarias_lectura_orden =  DecimalField('C', places=2, render_kw={'disabled': ''})
    d_horarias_lectura_orden =  DecimalField('D', places=2, render_kw={'disabled': ''})
    a_demandas_lectura_orden =  DecimalField('A', places=2, render_kw={'disabled': ''})
    b_demandas_lectura_orden =  DecimalField('B', places=2, render_kw={'disabled': ''})
    c_demandas_lectura_orden =  DecimalField('C', places=2, render_kw={'disabled': ''})
    d_demandas_lectura_orden =  DecimalField('D', places=2, render_kw={'disabled': ''})

    anadir_lectura_lectura_orden = SubmitField('+', render_kw={'disabled': ''})
    lista_lecturas_totales_orden = []

    # PERFIL DE CARGA
    archivo_perfil_carga_orden = FileField(render_kw={'disabled': ''})

    # RDICO5
    kwh_medidor_rdico5_orden = BooleanField('kWh', default=False)
    kvarh_medidor_rdico5_orden = BooleanField('kvarh', default=False)
    kW_medidor_rdico5_orden = BooleanField('kW', default=False)
    perfildecarga_medidor_rdico5_orden = BooleanField('Perfil de carga', default=False)
    compensacion_medidor_rdico5_orden = BooleanField('Compensación', default=False)
    descripcion_medidor_rdico5_orden = TextAreaField('Descripción')
    
    aluminio_acometida_rdico5_orden = BooleanField('Aluminio', default=False)
    antihurto_acometida_rdico5_orden = BooleanField('Antihurto', default=False)
    subterranea_acometida_rdico5_orden = BooleanField('Subterránea', default=False)
    descripcion_acometida_rdico5_orden = TextAreaField('Descripción')
    
    tablero_metalico_rdico5_orden = BooleanField('Tablero metálico')
    descripcion_tablero_metalico_rdico5_orden = StringField()
    cable_numero6_rdico5_orden = BooleanField('Cable No. 6 AWG 7 hilos')
    descripcion_cable_numero6_rdico5_orden = StringField()
    protector_termico_rdico5_orden = BooleanField('Protector térmico DIN 35')
    descripcion_protector_termico_rdico5_orden = StringField()
    tps_rdico5_orden = BooleanField('TPs')
    descripcion_tps_rdico5_orden = StringField()
    tarifa_rdico5_orden = BooleanField('Tarifa')
    descripcion_tarifa_rdico5_orden = StringField()
    tablero_antihurto_rdico5_orden = BooleanField('Tablero antihurto')
    descripcion_tablero_antihurto_rdico5_orden = StringField()
    conductor_numero8_rdico5_orden = BooleanField('Conductor No.8 AWG')
    descripcion_conductor_numero8_rdico5_orden = StringField()
    candado_master_rdico5_orden = BooleanField('Candado master')
    descripcion_candado_master_rdico5_orden = StringField()
    tcs_rdico5_orden = BooleanField('TCs')
    descripcion_tcs_rdico5_orden = StringField()
    otros_cambio_materiales_rdico5_orden = TextAreaField('Otros')
    
    control_medicion_rdico5_orden = StringField('Control de la medición', render_kw={'disabled': ''})

    lista_acciones_rdico5_orden = SelectField('Acción', choices=[])
    lista_anomalias_acciones_orden = []
    
    
    # BOTONES ESPECIALES PARA GENERAR SUBMITS
    boton_cambio_marca_orden = SubmitField()
    boton_cambio_marca_transformador_medida_orden = SubmitField()
    boton_agregar_accion_rdico5 = SubmitField()

    boton_eliminar_transformador_medida_orden = SubmitField()    
    boton_eliminar_transformador_distribucion_orden = SubmitField()
    boton_eliminar_pruebas_orden = SubmitField()
    boton_eliminar_sellos_orden = SubmitField()
    boton_eliminar_lecturas_orden = SubmitField()
    boton_eliminar_usos_orden = SubmitField()
    boton_eliminar_anomalias_orden = SubmitField()
    boton_eliminar_accion_rdico5_orden = SubmitField()

    
    # BOTONES PARA CREACION DE CHOICES
    tipo_faltante_medidor_orden = SelectField('Tipo de característica', choices=[("Marca","Marca"),("Tipo","Tipo"),("Año","Año"),("Exactitud","Exactitud"),
    ("Corriente","Corriente"),("Voltaje","Voltaje"),("Constante K","Constante K"), ("Conexión","Conexión")])
    nombre_faltante_medidor_orden = StringField('Valor')
    boton_crear_faltante_medidor_orden = SubmitField('Crear')

    tipo_faltante_parametrizacion_orden = SelectField('Tipo de característica', choices=[("Multiplicador","Multiplicador"),("Registros","Registros")])
    nombre_faltante_parametrizacion_orden = StringField('Valor')
    boton_crear_faltante_parametrizacion_orden = SubmitField('Crear')

    tipo_faltante_transformador_medida_orden = SelectField('Tipo de característica', choices=[("Marca TC","Marca TC"),("Marca TP","Marca TP"),("Marca TCS/TPS","Marca TCS/TPS")])
    nombre_faltante_transformador_medida_orden = StringField('Valor')
    boton_crear_faltante_transformador_medida_orden = SubmitField('Crear')

    tipo_faltante_transformador_distribucion_orden = SelectField('Tipo de característica', choices=[("Marca","Marca"),("Tipo","Tipo")])
    nombre_faltante_transformador_distribucion_orden = StringField('Valor')
    boton_crear_faltante_transformador_distribucion_orden = SubmitField('Crear')

    tipo_faltante_sello_orden = SelectField('Tipo de característica', choices=[("Tipo","Tipo"),("Ubicación","Ubicación"),("Estado","Estado")])
    nombre_faltante_sello_orden = StringField('Valor')
    boton_crear_faltante_sello_orden = SubmitField('Crear')

    tipo_faltante_resultados_orden = SelectField('Tipo de característica', choices=[("Anomalía","Anomalía"),("Uso de la energía","Uso de la energía")])
    nombre_faltante_resultados_orden = StringField('Valor')
    boton_crear_faltante_resultados_orden = SubmitField('Crear')

    tipo_faltante_rdico5_orden = SelectField('Tipo de característica', choices=[("Acción","Acción")])
    nombre_faltante_rdico5_orden = StringField('Valor')
    boton_crear_faltante_rdico5_orden = SubmitField('Crear')


    # BOTONES GENERALES
    guardar = SubmitField('Guardar')
    volver_revision = SubmitField('Enviar a Revisión')
    cancelar_administrar = SubmitField('Aceptar') # Es aceptar porque es el aceptar del dialog de cancelacion!
    cerrar_sap = SubmitField('Cerrar en sap') 