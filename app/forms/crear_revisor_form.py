from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, SelectField, BooleanField
from wtforms.validators import DataRequired
from controller import administracion_controller


class CrearRevisorForm(FlaskForm):
    identificacion_crear = StringField('Identificacion')
    razonSocial_crear = StringField('Razon Social')
    firma_crear = FileField()
    jefeGrupo_crear = BooleanField('¿Es jefe de grupo?')
    grupoRevisor_crear = SelectField('Grupo Revisor', default=1)
    crear = SubmitField('Crear')
    cancelar_crear = SubmitField('Cancelar')
