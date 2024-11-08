from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import Config
from extensions import db  # Aqui você já tem o db, então remova 'migrate' da importação
from flask_migrate import Migrate  # Importe o Migrate
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import os  # Adicionando a importação do módulo os para manipulação de arquivos
from forms import EditProfileForm  # Certifique-se de que o caminho esteja correto
from werkzeug.utils import secure_filename
# Certifique-se de importar o formulário corretamente
# Exemplo:
# from forms import EditProfileForm  # Importe o form de edição de perfil, se estiver em um arquivo separado.

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

# Inicialize o banco de dados e o Flask-Migrate
db.init_app(app)
migrate = Migrate(app, db)  # Inicializa o Migrate com a aplicação e o banco de dados

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
        username = request.form.get('username')
        password = request.form.get('password')

        if username and password:
            user = User.query.filter_by(username=username).first()
            if user:
                print(f"Usuário encontrado: {user.username}")
            else:
                print("Usuário não encontrado.")
            
            if user and check_password_hash(user.password, password):
                login_user(user)
                print(f"Usuário logado: {current_user.username}")
                return redirect(url_for('perfil'))  # Verifique se essa rota está correta
            else:
                print("Falha na autenticação - credenciais inválidas.")
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

    try:
        # Cria um novo usuário
        novo_usuario = User(username=nome, email=email, password=senha_hash)
        db.session.add(novo_usuario)
        db.session.commit()
        flash('Cadastro realizado com sucesso! Faça login.', 'success')
        return redirect(url_for('login'))
    except Exception as e:
        db.session.rollback()  # Desfaz qualquer mudança no banco
        flash(f'Ocorreu um erro ao tentar cadastrar: {str(e)}', 'danger')
        return render_template('register.html')

# Rota de serviços
@app.route('/servicos')
@login_required  # Protege a rota
def servicos():
    return render_template('servicos.html')


@app.route('/perfil')
@login_required  # Garante que o usuário esteja autenticado
def perfil():
    # Agora você pode acessar o current_user diretamente
    return render_template('perfil.html', user=current_user)


@app.route('/manutencao_preventiva')
def manutencao_preventiva():
    return render_template('manutencao_preventiva.html')

@app.route('/reparos_emergencia')
def reparos_emergencia():
    return render_template('reparos_emergencia.html')

@app.route('/historico_veiculo')
def historico_veiculo():
    return render_template('historico_veiculo.html')

# Rota para editar o perfil
@app.route('/editar_perfil', methods=['GET', 'POST'])
@login_required  # Garante que o usuário esteja autenticado
def edit_profile():
    user = current_user  # Acessa o usuário logado via Flask-Login

    if request.method == 'POST':
        # Aqui você coleta os dados do formulário e salva as alterações
        user.username = request.form['username']
        user.email = request.form['email']
        
        # Coleta os dados do veículo
        user.marca = request.form['marca']
        user.modelo = request.form['modelo']
        user.ano_fabricacao = request.form['ano_fabricacao']
        user.cor = request.form['cor']
        user.placa = request.form['placa']
        user.renavam = request.form['renavam']
        
        # Se o upload das fotos for feito, processa e armazena
        if 'foto_perfil' in request.files:
            foto_perfil = request.files['foto_perfil']
            if foto_perfil:
                # Salve a foto no diretório correto
                foto_perfil.save(os.path.join(app.config['UPLOAD_FOLDER'], foto_perfil.filename))
                user.foto_perfil = foto_perfil.filename
        
        if 'foto_crlv' in request.files:
            foto_crlv = request.files['foto_crlv']
            if foto_crlv:
                foto_crlv.save(os.path.join(app.config['UPLOAD_FOLDER'], foto_crlv.filename))
                user.foto_crlv = foto_crlv.filename
        
        # Atualiza no banco de dados
        db.session.commit()

        # Mensagem de sucesso
        flash('Perfil atualizado com sucesso!', 'success')

        # Redireciona para a página de perfil
        return redirect(url_for('perfil'))
    
    return render_template('edit_profile.html', user=user)

# Finalizando a criação do banco de dados
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Isso cria o banco de dados se ainda não existir
    app.run(debug=True)
