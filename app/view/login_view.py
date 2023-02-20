from flask import request, render_template, url_for
from flask_login import login_user, LoginManager
from werkzeug.utils import redirect

from app.forms.login_form import LoginForm
from controller import login_controller
from flask import flash
from app import app
from controller.conexion_controller import Conexion
from controller.gestor_controller import Gestor
from model.usuario import Usuario

login_manager = LoginManager(app)
login_manager.login_view = "login"


@app.route('/login.html', methods=['GET', 'POST'])
def login():
    params = []
    loginForm = LoginForm()

    if loginForm.validate_on_submit():
        user = login_controller.get_user(loginForm.user.data)
        if user is not None and user.check_password(loginForm.password.data):
            if user.activo:
                login_user(user, remember=loginForm.recuerdame.data)
                flash('Bienvenido ' + loginForm.user.data, 'exito')
                return redirect(url_for('index'))
            else:
                flash('El usuario no esta activo','error')
        else:
            flash('Credenciales incorrectas', 'error')

    params.append(loginForm)
    return render_template('login.html', segment='login', params=params)


@login_manager.user_loader
def load_user(user_id):
    try:
        g = Gestor()
        db = Conexion.db
        db.connect()
        users = Usuario.select()
        for user in users:
            if user.id == int(user_id):
                db.close()
                return user
        db.close()
        return None
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)

