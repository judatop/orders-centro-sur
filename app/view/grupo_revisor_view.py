from flask import flash, render_template, request, url_for
from flask_login import login_required
from werkzeug.utils import redirect
from app.forms.grupo_revisor_form import GrupoRevisorForm
from app.view.usuario_view import usuario

from controller import grupo_revisor_controller, usuarios_controller
from app.forms.crear_grupo_revisor_form import CrearGrupoRevisorForm
from app.forms.modificar_grupo_revisor_form import ModificarGrupoRevisorForm
from app import app
from model.gruporevisor import GrupoRevisor


@app.route('/gruporevisor.html', methods=['GET', 'POST'])
@login_required
def gruporevisor():

    privilegio = usuarios_controller.verificar_privilegios("GrupoRevisor")

    if privilegio:
        params = []

        grupo_revisor_form = GrupoRevisorForm()
        grupos_revisores = grupo_revisor_controller.obtener_grupos_revisores()

        params.append(grupos_revisores) # params[0]
        params.append(grupo_revisor_form) # params[1]

        if grupo_revisor_form.crear.data:
            return redirect(url_for('crear_grupo_revisor'))

        if grupo_revisor_form.modificar.data:
            id_grupo_revisor = request.form['input_grupo_revisor_modificar']

            if id_grupo_revisor == "0":
                flash('Debe seleccionar un grupo revisor','error')
            else:
                return redirect(url_for('modificar_grupo_revisor', id_grupo_revisor=id_grupo_revisor)) 

        return render_template('gruporevisor.html', segment='gruporevisor', params=params)
    return redirect(url_for('index'))

@app.route('/crear_grupo_revisor.html', methods=['GET', 'POST'])
@login_required
def crear_grupo_revisor():
    params = []
    crear_grupo_revisor_form = CrearGrupoRevisorForm()
    crear_grupo_revisor_form.usuario_crear.choices = grupo_revisor_controller.obtener_choices_usuarios()
    if crear_grupo_revisor_form.validate_on_submit():
        if crear_grupo_revisor_form.crear.data:
            nombreGrupo = crear_grupo_revisor_form.nombre_crear.data
            usuarioGrupo = crear_grupo_revisor_form.usuario_crear.data

            grupo_revisor = GrupoRevisor(nombre=nombreGrupo)

            # Creamos grupo revisor
            bandera_creado = grupo_revisor_controller.crear_grupo_revisor(usuarioGrupo, grupo_revisor)

            if bandera_creado:
                return redirect(url_for('gruporevisor'))

        if crear_grupo_revisor_form.cancelar_crear.data:
            return redirect(url_for('gruporevisor'))

    params.append(crear_grupo_revisor_form)
    return render_template('crear_grupo_revisor.html', segment='crear_grupo_revisor', params=params)


@app.route('/modificar_grupo_revisor/<int:id_grupo_revisor>', methods=['GET', 'POST'])
@login_required
def modificar_grupo_revisor(id_grupo_revisor):
    params = []
    modificar_grupo_revisor_form = ModificarGrupoRevisorForm()
    modificar_grupo_revisor_form.usuario_modificar.choices = grupo_revisor_controller.obtener_choices_usuarios()
    # Bandera para no llenar con datos del usuario seleccionado en la tabla en el form al presionar modificar
    bandera = 1
    if modificar_grupo_revisor_form.validate_on_submit():
        if modificar_grupo_revisor_form.modificar.data:
            nombreGrupo = modificar_grupo_revisor_form.nombre_modificar.data
            usuarioGrupo = modificar_grupo_revisor_form.usuario_modificar.data

            grupo_revisor = GrupoRevisor(id=id_grupo_revisor, nombre=nombreGrupo)

            # Creamos grupo revisor
            bandera_modificado = grupo_revisor_controller.modificar_grupo_revisor(usuarioGrupo, grupo_revisor)

            if bandera_modificado:
                return redirect(url_for('gruporevisor'))
            else:
                bandera = 0
        if modificar_grupo_revisor_form.cancelar_modificar.data:
            return redirect(url_for('gruporevisor'))

    params.append(modificar_grupo_revisor_form)

    grupo_revisor = grupo_revisor_controller.obtener_grupo_revisor(id_grupo_revisor)
    usuario = usuarios_controller.obtener_usuario(grupo_revisor.usuario_id)
    if grupo_revisor and bandera == 1:
        modificar_grupo_revisor_form.nombre_modificar.data = grupo_revisor.nombre
        modificar_grupo_revisor_form.usuario_modificar.data = usuario.usuario

    return render_template('modificar_grupo_revisor.html', segment='modificar_grupo_revisor', params=params)


