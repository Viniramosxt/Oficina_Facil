# models.py
from datetime import datetime
from extensions import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    foto_perfil = db.Column(db.String(255))  # Caminho para a foto de perfil
    foto_crlv = db.Column(db.String(255))    # Caminho para a foto do CRLV
    marca = db.Column(db.String(100))  # Marca do veículo
    modelo = db.Column(db.String(100)) # Modelo do veículo
    ano_fabricacao = db.Column(db.Integer)        # Ano de fabricação
    cor = db.Column(db.String(50))     # Cor do veículo
    placa = db.Column(db.String(20))   # Placa do veículo
    renavam = db.Column(db.String(20)) # Número do Renavam
