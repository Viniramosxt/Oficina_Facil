# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FileField
from wtforms.validators import DataRequired

class EditProfileForm(FlaskForm):
    marca = StringField('Marca', validators=[DataRequired()])
    modelo = StringField('Modelo', validators=[DataRequired()])
    ano_fabricacao = IntegerField('Ano de Fabricação', validators=[DataRequired()])
    cor = StringField('Cor', validators=[DataRequired()])
    placa = StringField('Placa', validators=[DataRequired()])
    renavam = StringField('Renavam', validators=[DataRequired()])
    foto_perfil = FileField('Foto de Perfil')
    crlv_foto = FileField('Foto do CRLV')
