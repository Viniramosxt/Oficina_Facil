from flask import render_template, request, jsonify, redirect, url_for
from models import Oficina
from app import app  # Adicionar esta linha

@app.route('/')
def index():
    oficinas = Oficina.get_all_oficinas()
    return render_template('index.html', oficinas=oficinas)

@app.route('/perfil_oficina/<int:oficina_id>')
def perfil_oficina(oficina_id):
    oficina = Oficina.query.get_or_404(oficina_id)
    return render_template('perfil_oficina.html', oficina=oficina)

@app.route('/oficinas-proximas')
def oficinas_proximas():
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))
    oficinas = Oficina.query.all()
    
    # Filtrar oficinas próximas (exemplo simples, pode ser melhorado)
    proximas = [oficina for oficina in oficinas if abs(oficina.lat - lat) < 0.1 and abs(oficina.lon - lon) < 0.1]
    
    return jsonify({'officinas': [{'id': oficina.id, 'nome': oficina.nome, 'lat': oficina.lat, 'lon': oficina.lon} for oficina in proximas]})

@app.route('/atualizar_localizacao_oficinas')
def atualizar_localizacao_oficinas():
    oficinas = Oficina.query.all()
    for oficina in oficinas:
        oficina.update_location()
    return redirect(url_for('index'))

@app.route('/oficinas')
def oficinas():
    oficinas = Oficina.query.all()
    return jsonify([{'id': oficina.id, 'nome': oficina.nome, 'lat': oficina.lat, 'lon': oficina.lon} for oficina in oficinas])
