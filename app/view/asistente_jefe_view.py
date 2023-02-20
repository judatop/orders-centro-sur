from flask import flash, render_template, request, url_for
from flask_login import login_required
from werkzeug.utils import redirect
from app.forms.asistente_jefe_form import AsistenteJefeForm

from controller import asistente_jefe_controller
from controller import usuarios_controller
from app.forms.crear_asistente_jefe_form import CrearAsistenteJefeForm
from app.forms.modificar_asistente_jefe_form import ModificarAsistenteJefeForm
from app import app
from model.asistentejefe import AsistenteJefe


@app.route('/asistentejefe.html', methods=['GET', 'POST'])
@login_required
def asistentejefe():

    privilegio = usuarios_controller.verificar_privilegios("AsistenteJefe")
    if privilegio:
        params = []

        asistente_jefe_form = AsistenteJefeForm()
        asistentes = asistente_jefe_controller.obtener_asistentes_jefes()

        params.append(asistentes) # params[0]
        params.append(asistente_jefe_form) # params[1]

        if asistente_jefe_form.crear.data:
            return redirect(url_for('crear_asistente_jefe'))

        if asistente_jefe_form.modificar.data:
            id_asistente_jefe = request.form['input_asistente_jefe_modificar']

            if id_asistente_jefe == "0":
                flash('Debe seleccionar un asistente jefe','error')
            else:
                return redirect(url_for('modificar_asistente_jefe', id_asistente=id_asistente_jefe)) 

        return render_template('asistentejefe.html', segment='asistentejefe', params=params)
    return redirect(url_for('index'))

@app.route('/crear_asistente_jefe', methods=['GET', 'POST'])
@login_required
def crear_asistente_jefe():
    params = []
    crear_asistente_jefe_form = CrearAsistenteJefeForm()
    crear_asistente_jefe_form.usuario_crear.choices = usuarios_controller.obtener_usuarios_choices()
    if crear_asistente_jefe_form.validate_on_submit():
        if crear_asistente_jefe_form.crear.data:
            nombre = crear_asistente_jefe_form.nombre_crear.data
            usuario = crear_asistente_jefe_form.usuario_crear.data

            asistente_jefe = AsistenteJefe(nombre=nombre)

            bandera_creado = asistente_jefe_controller.crear_asistente(asistente_jefe, usuario)

            if bandera_creado:
                return redirect(url_for('asistentejefe'))

        if crear_asistente_jefe_form.cancelar_crear.data:
            return redirect(url_for('asistentejefe'))

    params.append(crear_asistente_jefe_form)
    return render_template('crear_asistente_jefe.html', segment='crear_asistente_jefe', params=params)

@app.route('/modificar_asistente_jefe/<int:id_asistente>', methods=['GET', 'POST'])
@login_required
def modificar_asistente_jefe(id_asistente):
    params = []
    modificar_asistente_jefe_form = ModificarAsistenteJefeForm()
    modificar_asistente_jefe_form.usuario_modificar.choices = usuarios_controller.obtener_usuarios_choices()
    bandera = 1

    if modificar_asistente_jefe_form.validate_on_submit():
        if modificar_asistente_jefe_form.modificar.data:
            nombre = modificar_asistente_jefe_form.nombre_modificar.data
            usuario = modificar_asistente_jefe_form.usuario_modificar.data

            asistente_jefe = AsistenteJefe(id=id_asistente, nombre=nombre)

            bandera_creado = asistente_jefe_controller.modificar_asistente(asistente_jefe, usuario)

            if bandera_creado:
                return redirect(url_for('asistentejefe'))
            else:
                bandera = 0

        if modificar_asistente_jefe_form.cancelar_modificar.data:
            return redirect(url_for('asistentejefe'))

    params.append(modificar_asistente_jefe_form)

    asistente = asistente_jefe_controller.obtener_asistente(id_asistente)
    usuario = usuarios_controller.obtener_usuario(asistente.usuario_id)
    if usuario and bandera == 1:
        modificar_asistente_jefe_form.nombre_modificar.data = asistente.nombre
        modificar_asistente_jefe_form.usuario_modificar.data = usuario.usuario

    return render_template('modificar_asistente_jefe.html', segment='modificar_asistente_jefe', params=params)
