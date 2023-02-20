from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired

class CrearUsuarioForm(FlaskForm):
    usuario_crear = StringField('Usuario')
    clave_crear = PasswordField('Clave')
    tipo_crear = SelectField('Tipo de grupo', choices=[("Control de la medición", "Control de la medición"), ("Contratista", "Contratista")], default=1)
    activo = BooleanField('Activo', default=True)
    crear = SubmitField('Crear')
    cancelar_crear = SubmitField('Cancelar')