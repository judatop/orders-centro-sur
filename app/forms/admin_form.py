from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length


class AdministracionForm(FlaskForm):

    archivoCliente = FileField()
    archivoHistorialConsumos = FileField()
    archivoOrden = FileField()
    archivoMarcasMedidores = FileField()
    cargar = SubmitField('Cargar')
