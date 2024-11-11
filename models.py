from extensions import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

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
    ano_fabricacao = db.Column(db.String(4), nullable=True)
    cor = db.Column(db.String(30), nullable=True)
    placa = db.Column(db.String(7), nullable=True)
    renavam = db.Column(db.String(11), nullable=True)
    
    # Fotos
    foto_perfil = db.Column(db.String(200), nullable=True)
    foto_crlv = db.Column(db.String(200), nullable=True)

    # Relacionamento com o histórico de relatórios do cliente
    relatorios = db.relationship('Relatorio', backref='cliente', lazy=True)

    # Relacionamento com o plano assinado
    plano_assinado_id = db.Column(db.Integer, db.ForeignKey('plano.id'), nullable=True)
    
    oficina = db.relationship('Oficina', backref='user', lazy=True)
    def __repr__(self):
        return f'<User {self.username}>'

class Plano(db.Model):
    __tablename__ = 'plano'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)

    # Relacionamento com o usuário
    usuarios = db.relationship('User', backref='plano_assinado', lazy=True)

    def __repr__(self):
        return f'<Plano {self.nome}>'


class Oficina(db.Model):
    __tablename__ = 'oficina'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha_hash = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(14), unique=True, nullable=False)
    endereco = db.Column(db.String(255))
    contato = db.Column(db.String(50))
    lat = db.Column(db.Float, nullable=True)  # Latitude
    lon = db.Column(db.Float, nullable=True)  # Longitude
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Relacionamento com funcionários
    funcionarios = db.relationship('Funcionario', backref='oficina', lazy=True)

    # Relacionamento com os relatórios gerados pela oficina
    relatorios = db.relationship('Relatorio', backref='oficina', lazy=True)

    def __init__(self, nome, email, senha, cnpj, endereco=None, contato=None, lat=None, lon=None):
        self.nome = nome
        self.email = email
        self.senha_hash = senha
        self.cnpj = cnpj
        self.endereco = endereco
        self.contato = contato
        self.lat = lat
        self.lon = lon

    def __repr__(self):
        return f'<Oficina {self.nome}>'


class Funcionario(db.Model):
    __tablename__ = 'funcionario'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(150), nullable=False)
    id_oficina = db.Column(db.Integer, db.ForeignKey('oficina.id'), nullable=False)

    # Relacionamento com os relatórios gerados pelo funcionário
    relatorios = db.relationship('Relatorio', backref='funcionario', lazy=True)

    def set_password(self, password):
        self.senha = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.senha, password)

    def __repr__(self):
        return f'<Funcionario {self.nome}>'


class Relatorio(db.Model):
    __tablename__ = 'relatorio'

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    servico = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)

    # Relacionamentos com cliente, funcionário e oficina
    id_funcionario = db.Column(db.Integer, db.ForeignKey('funcionario.id'), nullable=False)
    id_cliente = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id_oficina = db.Column(db.Integer, db.ForeignKey('oficina.id'), nullable=False)

    def __repr__(self):
        return f'<Relatorio {self.servico} - Cliente ID: {self.id_cliente}>'

