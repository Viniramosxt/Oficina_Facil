from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import Config
from extensions import db
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config.from_object(Config)

# Defina a chave secreta para sessões
app.secret_key = 'sua_chave_secreta_muito_segura_aqui'  # Altere isso para uma chave segura

# Inicialização do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Define a página de login para redirecionamento

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

db.init_app(app)

# Rota inicial
@app.route('/')
def home():
    if current_user.is_authenticated:
        return render_template('index.html')  # Exibe conteúdo para usuários logados
    else:
        mensagem = "OFICINA FÁCIL oferece planos de saúde para veículos."
        return render_template('index.html', mensagem=mensagem)  # Exibe conteúdo para visitantes

# Rota de Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')  # Usando .get() para evitar KeyError
        password = request.form.get('password')  # Usando .get() para evitar KeyError

        if username and password:  # Verifica se os campos foram preenchidos
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):  # Verifique a senha de forma segura
                login_user(user)  # Utilize login_user do Flask-Login
                return redirect(url_for('home'))
            flash('Credenciais inválidas.', 'danger')
        else:
            flash('Por favor, preencha todos os campos.', 'danger')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()  # Utilize logout_user do Flask-Login
    return redirect(url_for('home'))  # Redireciona para a página inicial

# Rota de Cadastro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['username']
        email = request.form['email']
        senha = request.form['password']
        
        # Validação de senha forte (exemplo simples)
        if len(senha) < 8 or not any(char.isdigit() for char in senha) or not any(char.isalpha() for char in senha):
            flash('A senha deve ter pelo menos 8 caracteres, incluindo letras e números.', 'danger')
            return render_template('register.html')

        senha_hash = generate_password_hash(senha)

        # Verifica se o usuário já existe
        usuario_existente = User.query.filter_by(email=email).first()
        if usuario_existente:
            flash('E-mail já cadastrado. Faça login.', 'warning')
            return redirect(url_for('login'))

        # Cria um novo usuário
        novo_usuario = User(username=nome, email=email, password=senha_hash)
        db.session.add(novo_usuario)
        db.session.commit()
        flash('Cadastro realizado com sucesso! Faça login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# Rota de serviços
@app.route('/servicos')
@login_required  # Protege a rota
def servicos():
    return render_template('servicos.html')

# Rota de Perfil (protegida)
@app.route('/perfil')
@login_required  # Protege a rota
def perfil():
    return render_template('perfil.html', usuario=current_user)

# Finalizando a criação do banco de dados
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
