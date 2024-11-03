# config.py
import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'sua_chave_secreta')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:12345@localhost/oficina_facil'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
