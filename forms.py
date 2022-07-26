from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, IntegerField, DateTimeField, SelectMultipleField, SelectField
from wtforms.fields import DateTimeLocalField, DateTimeField
from wtforms.validators import DataRequired, InputRequired
from models import Mesa

class UsuarioForm(FlaskForm):
    cedula = IntegerField('Cedula', validators=[DataRequired()])
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellido = StringField('Apellido')
    email = EmailField('Email', validators=[DataRequired()])
    telefono = IntegerField('Telefono')
    registrar = SubmitField('Registrar')

class ReservaForm(FlaskForm):
    id_usuario = SelectField('Id Usuario', choices=[], validators=[DataRequired()])
    id_mesa = SelectField('Mesa', choices=[], validators=[DataRequired()])
    fecha_hora = DateTimeLocalField('Fecha', format="%Y-%m-%dT%H:%M", validators=[InputRequired()])
    registrar = SubmitField('Registrar')

    #def __init__(self):
     #   self.id_mesa.choices = [mesa.id_mesa for mesa in Mesa.query.all()]

class FechaForm(FlaskForm):
    fecha_hora = DateTimeLocalField('Fecha', format="%Y-%m-%dT%H:%M", validators=[InputRequired()])
    consultar = SubmitField('Consultar')
