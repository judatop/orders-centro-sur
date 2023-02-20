from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired

class ModificarAsistenteJefeForm(FlaskForm):
    nombre_modificar = StringField('Nombre')
    usuario_modificar = SelectField('Usuario', default=0)
    modificar = SubmitField('Modificar')
    cancelar_modificar = SubmitField('Cancelar')