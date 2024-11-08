# config.py
import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'sua_chave_secreta')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:12345@localhost/oficina_facil'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')
