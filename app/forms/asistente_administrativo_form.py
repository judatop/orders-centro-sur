from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, Label
from wtforms.validators import DataRequired


class AsistenteAdminForm(FlaskForm):
    crear = SubmitField('Crear')
    modificar = SubmitField('Modificar')