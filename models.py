from extensions import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import requests

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(20), default='cliente')
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

    # Relacionamentos
    relatorios = db.relationship('Relatorio', backref='cliente', lazy=True)
    plano_assinado_id = db.Column(db.Integer, db.ForeignKey('plano.id'), nullable=True)
    
    oficina = db.relationship('Oficina', backref='user', lazy=True)
    def __repr__(self):
        return f'<User {self.username}>'

class Plano(db.Model):
    __tablename__ = 'plano'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    features = db.Column(db.String(255), nullable=False)

    # Relationship with the User model
    usuarios = db.relationship('User', backref='plano_assinado', lazy=True)

    def __repr__(self):
        return f'<Plano {self.nome}>'


class Oficina(db.Model, UserMixin):  # Adicione UserMixin aqui
    __tablename__ = 'oficina'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(512), nullable=False)  # Aumentado para 512
    cnpj = db.Column(db.String(18), unique=True, nullable=False)
    endereco = db.Column(db.String(255))
    telefone = db.Column(db.String(50))
    logo = db.Column(db.String(255), nullable=True)
    lat = db.Column(db.Float, nullable=True)
    lon = db.Column(db.Float, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    atendimentos = db.Column(db.Integer, default=0)
    avaliacao = db.Column(db.Float, default=5.0)
    especialidades = db.Column(db.String(255))  # Alterado para String(255)
    horario = db.Column(db.String(255))
    horario_fds = db.Column(db.String(255))

    funcionarios = db.relationship('Funcionario', backref='oficina', lazy=True)
    relatorios = db.relationship('Relatorio', backref='oficina', lazy=True)

    def __init__(self, nome, email, senha, cnpj, endereco=None, telefone=None, 
                 lat=None, lon=None, especialidades=None, horario=None, 
                 horario_fds=None, logo=None):
        self.nome = nome
        self.email = email
        # Hash da senha antes de armazenar
        self.senha = generate_password_hash(senha)
        self.cnpj = cnpj
        self.endereco = endereco
        self.telefone = telefone
        self.lat = lat
        self.lon = lon
        self.especialidades = especialidades
        self.horario = horario
        self.horario_fds = horario_fds
        self.logo = logo
        self.atendimentos = 0
        self.avaliacao = 5.0

    def check_password(self, senha):
        # Alterado para usar o atributo 'senha' ao invés de 'senha_hash'
        return check_password_hash(self.senha, senha)
    
    # Certifique-se de que estes métodos existam
    def get_id(self):
        return str(self.id)
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True
        
    @property
    def is_anonymous(self):
        return False

    @staticmethod
    def get_all_oficinas():
        return Oficina.query.all()

    def update_location(self):
        if self.endereco:
            response = requests.get(f'https://nominatim.openstreetmap.org/search?q={self.endereco}&format=json')
            if response.status_code == 200:
                data = response.json()
                if data:
                    self.lat = float(data[0]['lat'])
                    self.lon = float(data[0]['lon'])
                    db.session.commit()

    def __repr__(self):
        return f'<Oficina {self.nome}>'


class Funcionario(db.Model):
    __tablename__ = 'funcionario'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150))
    email = db.Column(db.String(150))
    senha = db.Column(db.String(255))
    id_oficina = db.Column(db.Integer, db.ForeignKey('oficina.id'))


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

