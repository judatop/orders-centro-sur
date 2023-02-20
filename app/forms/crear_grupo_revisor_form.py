from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired


class CrearGrupoRevisorForm(FlaskForm):
    nombre_crear = StringField('Nombre del grupo')
    usuario_crear = SelectField('Usuario', default=0)
    crear = SubmitField('Crear')
    cancelar_crear = SubmitField('Cancelar')
