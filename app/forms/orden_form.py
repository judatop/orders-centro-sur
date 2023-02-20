from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, Label
from wtforms.validators import DataRequired


class OrdenForm(FlaskForm):
    ver_ordenes = SubmitField('Mapa de ordenes')
    generar_kml = SubmitField('Generar archivo kml')
    realizar_orden = SubmitField('Realizar')