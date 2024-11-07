from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import Config
from extensions import db  # Aqui você já tem o db, então remova 'migrate' da importação
from flask_migrate import Migrate  # Importe o Migrate
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import os  # Adicionando a importação do módulo os para manipulação de arquivos
from forms import EditProfileForm  # Certifique-se de que o caminho esteja correto
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
@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()  # Criando uma instância do formulário
    if form.validate_on_submit():  # Se o formulário for enviado e validado
        # Atualizando dados do veículo
        current_user.marca = form.marca.data
        current_user.modelo = form.modelo.data
        current_user.ano_fabricacao = form.ano_fabricacao.data
        current_user.cor = form.cor.data
        current_user.placa = form.placa.data
        current_user.renavam = form.renavam.data

        # Atualizando fotos
        if form.foto_perfil.data:
            foto_perfil_path = os.path.join('static/uploads', secure_filename(form.foto_perfil.data.filename))
            form.foto_perfil.data.save(foto_perfil_path)
            current_user.foto_perfil = foto_perfil_path

        if form.crlv_foto.data:
            crlv_foto_path = os.path.join('static/uploads', secure_filename(form.crlv_foto.data.filename))
            form.crlv_foto.data.save(crlv_foto_path)
            current_user.foto_crlv = crlv_foto_path

        db.session.commit()  # Salvando no banco de dados
        flash('Perfil atualizado com sucesso!')  # Mensagem de sucesso
        return redirect(url_for('perfil'))  # Redirecionando para o perfil

    elif request.method == 'GET':
        # Preenchendo o formulário com os dados atuais
        form.marca.data = current_user.marca
        form.modelo.data = current_user.modelo
        form.ano_fabricacao.data = current_user.ano_fabricacao
        form.cor.data = current_user.cor
        form.placa.data = current_user.placa
        form.renavam.data = current_user.renavam

    return render_template('edit_profile.html', form=form)

# Finalizando a criação do banco de dados
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Isso cria o banco de dados se ainda não existir
    app.run(debug=True)
