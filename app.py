from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import Config
from extensions import db  # Aqui você já tem o db, então remova 'migrate' da importação
from flask_migrate import Migrate  # Importe o Migrate
from models import User,Funcionario,Oficina,Relatorio, Plano
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import os  # Adicionando a importação do módulo os para manipulação de arquivos
from forms import EditProfileForm  # Certifique-se de que o caminho esteja correto
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError


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
def servicos():
    planos = [
        {
            'id': 1,
            'nome': 'Plano Básico',
            'preco': '100,00',
            'features': ['Manutenções essenciais', 'Checagem mensal', 'Suporte básico']
        },
        {
            'id': 2,
            'nome': 'Plano Intermediário',
            'preco': '200,00',
            'features': ['Todos os benefícios do plano básico', 'Serviços de médio porte', 'Revisões programadas', 'Suporte prioritário']
        },
        {
            'id': 3,
            'nome': 'Plano Premium',
            'preco': '300,00',
            'features': ['Todos os benefícios do plano intermediário', 'Cobertura completa', 'Assistência 24h', 'Benefícios exclusivos']
        }
    ]
    return render_template('servicos.html', planos=planos)


@app.route('/perfil')
@login_required  # Garante que o usuário esteja autenticado
def perfil():
    # Agora você pode acessar o current_user diretamente
    return render_template('perfil.html', user=current_user)

@app.route('/reparos_emergencia')
def reparos_emergencia():
    return render_template('reparos_emergencia.html')

@app.route('/historico_veiculo')
@login_required
def historico_veiculo():
    # Obter todos os relatórios associados ao cliente logado
    relatorios = Relatorio.query.filter_by(id_cliente=current_user.id).all()
    return render_template('historico_veiculo.html', relatorios=relatorios)

@app.route('/editar_perfil_oficina', methods=['GET', 'POST'])
@login_required  # Se necessário para autenticação
def editar_perfil_oficina():
    # Aqui você pega a oficina que será editada (exemplo usando ID)
    oficina = Oficina.query.first()  # ou use .filter_by(id=some_id) para pegar uma oficina específica

    if request.method == 'POST':
        # Processa os dados enviados via POST
        oficina.nome_oficina = request.form['nome_oficina']
        oficina.localizacao = request.form['localizacao']
        # Adicione outros campos conforme necessário

        try:
            db.session.commit()  # Substitua 'db' pelo seu objeto de banco de dados
            flash('Perfil da oficina atualizado com sucesso!', 'success')
            return redirect(url_for('perfil_oficina'))  # Redireciona para a página de perfil da oficina
        except Exception as e:
            flash(f'Ocorreu um erro: {e}', 'danger')
            db.session.rollback()

    # Para o método GET, exibe o formulário com os dados atuais
    return render_template('editar_perfil_oficina.html', oficina=oficina)

@app.route('/assinar_plano/<int:plano_id>', methods=['GET', 'POST'])
@login_required
def assinar_plano(plano_id):
    plano = Plano.query.get(plano_id)
    if plano:
        # Associar o plano ao usuário
        current_user.plano_assinado_id = plano.id
        db.session.commit()
        flash('Plano assinado com sucesso!', 'success')
        return redirect(url_for('perfil'))  # Redireciona para o perfil do usuário
    flash('Plano não encontrado', 'danger')
    return redirect(url_for('servicos'))  # Se o plano não for encontrado, redireciona para a página de serviços


@app.route('/confirmar_assinatura/<int:plano_id>', methods=['GET', 'POST'])
def confirmar_assinatura(plano_id):
    # Lógica para confirmar a assinatura
    pass

@app.route('/editar_perfil', methods=['GET', 'POST'])
@login_required  # Garante que o usuário esteja autenticado
def edit_profile():
    user = current_user  # Acessa o usuário logado via Flask-Login

    # Supondo que você tenha uma função para obter a oficina do usuário
    oficina = obter_oficina(user.id)  # Adicione esta função para recuperar os dados da oficina associada ao usuário
    
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
    
    return render_template('edit_profile.html', user=user, oficina=oficina)

# Função para obter os dados da oficina do usuário (exemplo)
def obter_oficina(user_id):
    # Aqui você faria uma consulta ao banco de dados para pegar os dados da oficina relacionada ao usuário
    oficina = Oficina.query.filter_by(user_id=user_id).first()  # Exemplo de consulta, ajuste conforme o seu modelo
    return oficina


# Rota de Login para Oficinas
@app.route('/login_oficina', methods=['GET', 'POST'])
def login_oficina():
    if request.method == 'POST':
        cnpj = request.form.get('cnpj')
        senha = request.form.get('password')
        oficina = Oficina.query.filter_by(cnpj=cnpj).first()

        # Verifica se o CNPJ está cadastrado
        if oficina:
            # Verifica se a senha está correta
            if check_password_hash(oficina.senha_hash, senha):
                session['oficina_id'] = oficina.id
                flash('Login realizado com sucesso!', 'success')
                return redirect(url_for('perfil_oficina'))
            else:
                flash('Senha incorreta. Tente novamente.', 'danger')
        else:
            flash('CNPJ não encontrado. Por favor, cadastre sua oficina.', 'danger')

    return render_template('login_oficina.html')


# Rota de Cadastro para Oficinas
@app.route('/register_oficina', methods=['GET', 'POST'])
def register_oficina():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('password')
        cnpj = request.form.get('cnpj')

        # Verificar se o CNPJ já está cadastrado
        if Oficina.query.filter_by(cnpj=cnpj).first():
            flash('CNPJ já cadastrado. Tente outro.', 'danger')
            return redirect(url_for('register_oficina'))

        # Verificar se o email já está cadastrado
        if Oficina.query.filter_by(email=email).first():
            flash('E-mail já cadastrado. Tente outro.', 'danger')
            return redirect(url_for('register_oficina'))

        # Criptografar a senha
        senha_criptografada = generate_password_hash(senha)

        # Criar e salvar a nova oficina
        try:
            nova_oficina = Oficina(nome=nome, email=email, senha=senha_criptografada, cnpj=cnpj)
            db.session.add(nova_oficina)
            db.session.commit()
            flash('Cadastro realizado com sucesso! Faça login para acessar sua conta.', 'success')
            return redirect(url_for('login_oficina'))
        except IntegrityError:
            db.session.rollback()
            flash('Erro ao cadastrar oficina. Tente novamente mais tarde.', 'danger')

    return render_template('register_oficina.html')

@app.route('/perfil_oficina', methods=['GET', 'POST'])
def perfil_oficina():
    # Supondo que a oficina tenha o ID 1 (ajuste conforme necessário)
    oficina = Oficina.query.get(1)

    if request.method == 'POST':
        # Lógica de atualização do perfil
        oficina.nome = request.form['nome']
        oficina.email = request.form['email']
        oficina.atendimentos = request.form.get('atendimentos', oficina.atendimentos)
        oficina.avaliacao = request.form.get('avaliacao', oficina.avaliacao)
        oficina.especialidades = request.form['especialidades']
        oficina.horario = request.form['horario']
        
        db.session.commit()
        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('perfil_oficina'))

    return render_template('perfil_oficina.html', oficina=oficina)

@app.route('/editar_perfil', methods=['GET', 'POST'])
def editar_perfil():
    oficina = Oficina.query.get(1)  # Supondo que a oficina tenha o ID 1
    
    if request.method == 'POST':
        # Atualizar os dados do perfil da oficina
        oficina.nome = request.form['nome']
        oficina.email = request.form['email']
        oficina.atendimentos = request.form.get('atendimentos', oficina.atendimentos)
        oficina.avaliacao = request.form.get('avaliacao', oficina.avaliacao)
        oficina.especialidades = request.form['especialidades']
        oficina.horario = request.form['horario']
        
        db.session.commit()
        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('perfil_oficina'))

    return render_template('editar_perfil.html', oficina=oficina)
# Finalizando a criação do banco de dados
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Isso cria o banco de dados se ainda não existir
    app.run(debug=True)
