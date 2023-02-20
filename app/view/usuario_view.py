from flask import flash, render_template, request, url_for
from flask_login import login_required
from werkzeug.utils import redirect
from app.forms.usuario_form import UsuarioForm

from controller import usuarios_controller
from app.forms.crear_usuario_form import CrearUsuarioForm
from app.forms.modificar_usuario_form import ModificarUsuarioForm
from app import app
from model.usuario import Usuario


@app.route('/usuario.html', methods=['GET', 'POST'])
@login_required
def usuario():
    privilegio = usuarios_controller.verificar_privilegios("Usuario")

    if privilegio:
        params = []

        usuario_form = UsuarioForm()
        usuarios = usuarios_controller.obtener_usuarios()

        params.append(usuarios) # params[0]
        params.append(usuario_form) # params[1]

        if usuario_form.crear.data:
            return redirect(url_for('crearusuario'))

        if usuario_form.modificar.data:
            id_usuario = request.form['input_usuario_modificar']

            if id_usuario == "0":
                flash('Debe seleccionar un usuario','error')
            else:
                return redirect(url_for('modificarusuario', id_usuario=id_usuario)) 

        return render_template('usuario.html', segment='usuarios', params=params)
    return redirect(url_for('index'))


@app.route('/crearusuario', methods=['GET', 'POST'])
@login_required
def crearusuario():
    params = []
    crear_usuario_form = CrearUsuarioForm()
    if crear_usuario_form.validate_on_submit():
        if crear_usuario_form.crear.data:
            username = crear_usuario_form.usuario_crear.data
            password = crear_usuario_form.clave_crear.data
            tipo = crear_usuario_form.tipo_crear.data
            activo = crear_usuario_form.activo.data

            usuario = Usuario(usuario=username, clave=password, admin=0, tipo=tipo, activo=activo)

            bandera_creado = usuarios_controller.crear_usuario(usuario)

            if bandera_creado:
                return redirect(url_for('usuario'))

        if crear_usuario_form.cancelar_crear.data:
            return redirect(url_for('usuario'))

    params.append(crear_usuario_form)
    return render_template('crear_usuario.html', segment='crear_usuario', params=params)


@app.route('/modificarusuario/<int:id_usuario>', methods=['GET', 'POST'])
@login_required
def modificarusuario(id_usuario):
    params = []
    modificar_usuario_form = ModificarUsuarioForm()
    # Bandera para no llenar con datos del usuario seleccionado en la tabla en el form al presionar modificar
    bandera = 1

    if modificar_usuario_form.validate_on_submit():
        if modificar_usuario_form.modificar.data:
            username = modificar_usuario_form.usuario_modificar.data
            password = modificar_usuario_form.clave_modificar.data
            tipo = modificar_usuario_form.tipo_modificar.data
            activo = modificar_usuario_form.activo_modificar.data

            usuario = Usuario(id=id_usuario, usuario=username, clave=password, admin=0, tipo=tipo, activo=activo)
            bandera_modificado = usuarios_controller.modificar_usuario(usuario)

            if bandera_modificado:
                return redirect(url_for('usuario'))
            else:
                bandera = 0

        if modificar_usuario_form.cancelar_modificar.data:
            return redirect(url_for('usuario'))

    params.append(modificar_usuario_form)

    usuario = usuarios_controller.obtener_usuario(id_usuario)
    if usuario and bandera == 1:
        modificar_usuario_form.usuario_modificar.data = usuario.usuario
        modificar_usuario_form.clave_modificar.data = usuario.clave
        modificar_usuario_form.tipo_modificar.data = usuario.tipo
        modificar_usuario_form.activo_modificar.data = usuario.activo

    return render_template('modificar_usuario.html', segment='modificar_usuario', params=params)


