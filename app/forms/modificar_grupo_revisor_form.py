from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired


class ModificarGrupoRevisorForm(FlaskForm):
    nombre_modificar = StringField('Nombre del grupo')
    usuario_modificar = SelectField('Usuario', default=0)
    modificar = SubmitField('Modificar')
    cancelar_modificar = SubmitField('Cancelar')