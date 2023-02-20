# -*- encoding: utf-8 -*-
"""
    desarrollador: juan garcía
"""
import secrets

# import Flask 
from flask import Flask

# Inject Flask magic
from flask_login import LoginManager
from controller.conexion_controller import Conexion
from controller.gestor_controller import Gestor
from model.usuario import Usuario
from flask_jsglue import JSGlue

app = Flask(__name__)

# App Config - the minimal footprint
# app.config['TESTING'] = True

app.config['SECRET_KEY'] = secrets.token_hex(20)
jsglue = JSGlue(app)

# Import routing to render the pages
from app.view import index_view, admin_view, login_view, orden_view, revisor_view, usuario_view, grupo_revisor_view, \
    logout_view, ubicacion_view, asistente_admin_view, asistente_jefe_view, administrar_orden_view