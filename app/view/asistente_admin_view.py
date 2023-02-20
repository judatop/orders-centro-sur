from flask import flash, render_template, request, url_for
from flask_login import login_required
from werkzeug.utils import redirect
from app.forms.asistente_administrativo_form import AsistenteAdminForm

from controller import asistente_admin_controller
from controller import usuarios_controller
from app.forms.crear_asistente_admin_form import CrearAsistenteAdminForm
from app.forms.modificar_asistente_admin_form import ModificarAsistenteAdminForm
from app import app
from model.asistenteadministrativo import AsistenteAdministrativo


@app.route('/asistenteadmin.html', methods=['GET', 'POST'])
@login_required
def asistenteadmin():

    privilegio = usuarios_controller.verificar_privilegios("AsistenteAdmin")
    if privilegio:
        params = []

        asistente_admin_Form = AsistenteAdminForm()
        asistentes = asistente_admin_controller.obtener_asistentes_administrativos()

        params.append(asistentes) # params[0]
        params.append(asistente_admin_Form) # params[1]

        if asistente_admin_Form.crear.data:
            return redirect(url_for('crear_asistente_admin'))

        if asistente_admin_Form.modificar.data:
            id_asistente_admin = request.form['input_asistente_administrativo_modificar']

            if id_asistente_admin == "0":
                flash('Debe seleccionar un asistente administrativo','error')
            else:
                return redirect(url_for('modificar_asistente_admin', id_asistente=id_asistente_admin)) 


        return render_template('asistenteadmin.html', segment='asistenteadmin', params=params)
    return redirect(url_for('index'))

@app.route('/crear_asistente_admin', methods=['GET', 'POST'])
@login_required
def crear_asistente_admin():
    params = []
    crear_asistente_admin = CrearAsistenteAdminForm()
    crear_asistente_admin.usuario_crear.choices = usuarios_controller.obtener_usuarios_choices()
    if crear_asistente_admin.validate_on_submit():
        if crear_asistente_admin.crear.data:
            nombre = crear_asistente_admin.nombre_crear.data
            usuario = crear_asistente_admin.usuario_crear.data

            asistente_admin = AsistenteAdministrativo(nombre=nombre)

            bandera_creado = asistente_admin_controller.crear_asistente(asistente_admin, usuario)

            if bandera_creado:
                return redirect(url_for('asistenteadmin'))

        if crear_asistente_admin.cancelar_crear.data:
            return redirect(url_for('asistenteadmin'))

    params.append(crear_asistente_admin)
    return render_template('crear_asistente_admin.html', segment='crear_asistente_admin', params=params)

@app.route('/modificar_asistente_admin/<int:id_asistente>', methods=['GET', 'POST'])
@login_required
def modificar_asistente_admin(id_asistente):
    params = []
    modificar_asistente_form = ModificarAsistenteAdminForm()
    modificar_asistente_form.usuario_modificar.choices = usuarios_controller.obtener_usuarios_choices()
    bandera = 1

    if modificar_asistente_form.validate_on_submit():
        if modificar_asistente_form.modificar.data:
            nombre = modificar_asistente_form.nombre_modificar.data
            usuario = modificar_asistente_form.usuario_modificar.data

            asistente_admin = AsistenteAdministrativo(id=id_asistente, nombre=nombre)

            bandera_creado = asistente_admin_controller.modificar_asistente(asistente_admin, usuario)

            if bandera_creado:
                return redirect(url_for('asistenteadmin'))
            else:
                bandera = 0

        if modificar_asistente_form.cancelar_modificar.data:
            return redirect(url_for('asistenteadmin'))

    params.append(modificar_asistente_form)

    asistente = asistente_admin_controller.obtener_asistente(id_asistente)
    usuario = usuarios_controller.obtener_usuario(asistente.usuario_id)
    if usuario and bandera == 1:
        modificar_asistente_form.nombre_modificar.data = asistente.nombre
        modificar_asistente_form.usuario_modificar.data = usuario.usuario

    return render_template('modificar_asistente_admin.html', segment='modificar_asistente_admin', params=params)
