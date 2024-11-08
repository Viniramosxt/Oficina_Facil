from extensions import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Informações do veículo
    marca = db.Column(db.String(50), nullable=True)
    modelo = db.Column(db.String(50), nullable=True)
    ano_fabricacao = db.Column(db.String(4), nullable=True)  # Ano de fabricação
    cor = db.Column(db.String(30), nullable=True)
    placa = db.Column(db.String(7), nullable=True)
    renavam = db.Column(db.String(11), nullable=True)
    
    # Fotos
    foto_perfil = db.Column(db.String(200), nullable=True)  # Caminho para foto de perfil
    foto_crlv = db.Column(db.String(200), nullable=True)  # Caminho para foto do CRLV

    def __repr__(self):
        return f'<User {self.username}>'

class Oficina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    endereco = db.Column(db.String(255), nullable=False)  # Endereço da oficina
    lat = db.Column(db.Float, nullable=False)  # Latitude
    lon = db.Column(db.Float, nullable=False)  # Longitude
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Relaciona a oficina com o usuário (se necessário)
    
    user = db.relationship('User', backref=db.backref('oficinas', lazy=True))  # Relacionamento com a tabela User (se for necessário)

    def __repr__(self):
        return f'<Oficina {self.nome}>'
