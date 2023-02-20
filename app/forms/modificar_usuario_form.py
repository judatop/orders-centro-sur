from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired
from wtforms.widgets import PasswordInput


class ModificarUsuarioForm(FlaskForm):
    usuario_modificar = StringField('Usuario')
    clave_modificar = PasswordField('Clave', widget=PasswordInput(hide_value=False))
    tipo_modificar = SelectField('Tipo de grupo', choices=[("Control de la medición", "Control de la medición"), ("Contratista", "Contratista")], default=1)
    activo_modificar = BooleanField('Activo', default=True)
    modificar = SubmitField('Modificar')
    cancelar_modificar = SubmitField('Cancelar')