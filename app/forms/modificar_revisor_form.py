from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, SelectField, BooleanField
from wtforms.validators import DataRequired
from controller import administracion_controller


class ModificarRevisorForm(FlaskForm):
    identificacion_modificar = StringField('Identificacion')
    razonSocial_modificar = StringField('Razon Social')
    firma_modificar = FileField()
    jefeGrupo_modificar = BooleanField('¿Es jefe de grupo?')
    grupoRevisor_modificar = SelectField('Grupo Revisor', default=1)
    modificar = SubmitField('Modificar')
    cancelar_modificar = SubmitField('Cancelar')
