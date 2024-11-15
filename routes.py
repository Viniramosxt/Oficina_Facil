from flask import Flask, render_template, redirect, url_for
from models import Oficina, User
from app import app  # Importe a instância do aplicativo Flask
from flask_login import current_user

@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.tipo == 'cliente':
            return redirect(url_for('home_cliente'))
        elif current_user.tipo == 'oficina':
            return redirect(url_for('home_oficina'))
    return render_template('index.html')

@app.route('/home_cliente')
def home_cliente():
    oficinas = Oficina.get_all_oficinas()
    return render_template('home_cliente.html', oficinas=oficinas)

@app.route('/home_oficina')
def home_oficina():
    return render_template('home_oficina.html')
