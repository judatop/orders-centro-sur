from flask import flash, render_template, request, url_for
from flask_login import login_required
from werkzeug.utils import redirect
from app.forms.revisor_form import RevisorForm

from controller import revisor_controller
from controller import grupo_revisor_controller
from app.forms.crear_revisor_form import CrearRevisorForm
from app.forms.modificar_revisor_form import ModificarRevisorForm
from controller import usuarios_controller
from app import app
from model.revisor import Revisor


@app.route('/revisor.html', methods=['GET', 'POST'])
@login_required
def revisor():
    privilegio = usuarios_controller.verificar_privilegios("Revisor")
    if privilegio:
        params = []

        revisor_form = RevisorForm()
        revisores = revisor_controller.obtener_revisores()

        params.append(revisores) # params[0]
        params.append(revisor_form) # params[1]

        if revisor_form.crear.data:
            return redirect(url_for('crear_revisor'))

        if revisor_form.modificar.data:
            id_revisor = request.form['input_revisor_modificar']

            if id_revisor == "0":
                flash('Debe seleccionar un revisor','error')
            else:
                return redirect(url_for('modificar_revisor', id_revisor=id_revisor)) 

        return render_template('revisor.html', segment='revisor', params=params)
    return redirect(url_for('index'))

@app.route('/crear_revisor.html', methods=['GET', 'POST'])
@login_required
def crear_revisor():
    params = []
    crear_revisor_form = CrearRevisorForm()
    crear_revisor_form.grupoRevisor_crear.choices = revisor_controller.obtener_choices_grupos_revisores()
    if crear_revisor_form.validate_on_submit():
        if crear_revisor_form.crear.data:
            identificacion_revisor = crear_revisor_form.identificacion_crear.data
            razon_social_revisor = crear_revisor_form.razonSocial_crear.data
            firma_revisor = crear_revisor_form.firma_crear.data
            jefe_grupo_revisor = crear_revisor_form.jefeGrupo_crear.data
            grupo_revisor_revisor = crear_revisor_form.grupoRevisor_crear.data

            revisor = Revisor(identificacion=identificacion_revisor, razonSocial=razon_social_revisor,
                              firma=firma_revisor, jefeGrupo=jefe_grupo_revisor)

            # Creamos grupo revisor
            bandera_creado = revisor_controller.crear_revisor(grupo_revisor_revisor, revisor)

            if bandera_creado:
                return redirect(url_for('revisor'))

        if crear_revisor_form.cancelar_crear.data:
            return redirect(url_for('revisor'))

    params.append(crear_revisor_form)
    return render_template('crear_revisor.html', segment='crear_revisor', params=params)


@app.route('/modificar_revisor/<int:id_revisor>', methods=['GET', 'POST'])
@login_required
def modificar_revisor(id_revisor):
    params = []
    modificar_revisor_form = ModificarRevisorForm()
    modificar_revisor_form.grupoRevisor_modificar.choices = revisor_controller.obtener_choices_grupos_revisores()
    # Bandera para no llenar con datos del usuario seleccionado en la tabla en el form al presionar modificar
    bandera = 1
    if modificar_revisor_form.validate_on_submit():
        if modificar_revisor_form.modificar.data:
            identificacion_revisor = modificar_revisor_form.identificacion_modificar.data
            razon_social_revisor = modificar_revisor_form.razonSocial_modificar.data
            firma_revisor = modificar_revisor_form.firma_modificar.data
            jefe_grupo_revisor = modificar_revisor_form.jefeGrupo_modificar.data
            grupo_revisor_revisor = modificar_revisor_form.grupoRevisor_modificar.data

            revisor = Revisor(id=id_revisor, identificacion=identificacion_revisor, razonSocial=razon_social_revisor,
                              firma=firma_revisor, jefeGrupo=jefe_grupo_revisor)

            # Creamos grupo revisor
            bandera_modificado = revisor_controller.modificar_revisor(grupo_revisor_revisor, revisor)

            if bandera_modificado:
                return redirect(url_for('revisor'))
            else:
                bandera = 0
        if modificar_revisor_form.cancelar_modificar.data:
            return redirect(url_for('revisor'))

    params.append(modificar_revisor_form)

    revisor = revisor_controller.obtener_revisor(id_revisor)
    grupo_revisor = grupo_revisor_controller.obtener_grupo_revisor(revisor.grupo_revisor_id)
    if revisor and bandera == 1:
        modificar_revisor_form.identificacion_modificar.data = revisor.identificacion
        modificar_revisor_form.razonSocial_modificar.data = revisor.razonSocial
        modificar_revisor_form.firma_modificar.data = revisor.firma
        modificar_revisor_form.jefeGrupo_modificar.data = revisor.jefeGrupo
        modificar_revisor_form.grupoRevisor_modificar.data = grupo_revisor.nombre

    return render_template('modificar_revisor.html', segment='modificar_revisor', params=params)





