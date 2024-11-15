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
from datetime import datetime
from utils import allowed_file
from flask import abort
from flask_wtf.csrf import CSRFProtect


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
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if len(password) < 8 or not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password):
            flash('A senha deve ter pelo menos 8 caracteres, incluindo letras e números.', 'danger')
            return render_template('register.html')

        if User.query.filter_by(email=email).first():
            flash('E-mail já cadastrado. Faça login.', 'warning')
            return redirect(url_for('login'))

        try:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, email=email, password=hashed_password, tipo='cliente')
            db.session.add(new_user)
            db.session.commit()
            flash('Cadastro realizado com sucesso! Faça login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cadastrar: {str(e)}', 'danger')
    
    return render_template('register.html')

@app.route('/servicos')
@login_required
def servicos():
    # Se o usuário já tem um plano assinado, redireciona para agendar_manutencao
    if current_user.plano_assinado_id:
        return redirect(url_for('agendar_manutencao'))
    # Se não tem plano, mostra a página de planos
    planos = Plano.query.all()
    return render_template('servicos.html', planos=planos)


@app.route('/perfil')
@login_required
def perfil():
    if session.get('oficina_id'):
        # Se for uma oficina logada
        oficina = Oficina.query.get(session['oficina_id'])
        return render_template('perfil_oficina.html', oficina=oficina)
    else:
        # Se for um cliente logado
        return render_template('perfil.html', user=current_user)

@app.route('/reparos_emergencia')
def reparos_emergencia():
    return render_template('reparos_emergencia.html')

@app.route('/historico_veiculo')
@login_required
def historico_veiculo():
    print(f'Usuário logado: {current_user.id}')
    if not current_user.plano_assinado:
        print(f'Plano não assinado, redirecionando para /servicos')
        return redirect(url_for('servicos'))
    relatorios = Relatorio.query.filter_by(id_cliente=current_user.id).all()
    print(f'Relatórios encontrados: {relatorios}')
    return render_template('historico_veiculo.html', relatorios=relatorios)



@app.route('/assinar_plano/<int:plano_id>', methods=['GET', 'POST'])
@login_required
def assinar_plano(plano_id):
    plano = Plano.query.get(plano_id)
    if plano:
        return redirect(url_for('confirmar_assinatura', plano_id=plano_id))
    flash('Plano não encontrado', 'danger')
    return redirect(url_for('servicos'))

@app.route('/confirmar_assinatura/<int:plano_id>', methods=['GET', 'POST'])
@login_required
def confirmar_assinatura(plano_id):
    plano = Plano.query.get(plano_id)
    if plano:
        if request.method == 'POST':
            # Associar o plano ao usuário
            current_user.plano_assinado_id = plano.id
            db.session.commit()
            flash('Plano assinado com sucesso!', 'success')
            return redirect(url_for('perfil'))
        return render_template('confirmar_assinatura.html', plano=plano)
    flash('Plano não encontrado', 'danger')
    return redirect(url_for('servicos'))

@app.route('/visualizar_agendamentos')
@login_required
def visualizar_agendamentos():
    oficina_id = session.get('oficina_id')
    if not oficina_id:
        flash('Acesso permitido apenas para oficinas.', 'warning')
        return redirect(url_for('home'))
        
    # Busca todos os relatórios/agendamentos para esta oficina
    agendamentos = Relatorio.query.filter_by(
        id_oficina=oficina_id
    ).order_by(
        Relatorio.data.desc()
    ).all()
    
    return render_template('visualizar_agendamentos.html', agendamentos=agendamentos)

@app.route('/detalhes_relatorio/<int:relatorio_id>')
def detalhes_relatorio(relatorio_id):
    # Lógica para obter os detalhes do relatório
    relatorio = Relatorio.query.get(relatorio_id)
    if relatorio:
        return render_template('detalhes_relatorio.html', relatorio=relatorio)
    else:
        flash('Relatório não encontrado!', 'error')
        return redirect(url_for('historico'))


@app.route('/agendar_manutencao', methods=['GET', 'POST'])
@login_required
def agendar_manutencao():
    # Verifica se o usuário tem plano assinado
    if not current_user.plano_assinado_id:
        flash('É necessário assinar um plano para agendar manutenções.', 'warning')
        return redirect(url_for('servicos'))
        
    if request.method == 'POST':
        oficina_id = request.form.get('oficina_id')
        data = request.form.get('data')
        horario = request.form.get('horario')
        servico = request.form.get('servico')
        descricao = request.form.get('descricao')
        
        novo_relatorio = Relatorio(
            servico=servico,
            descricao=descricao,
            data=datetime.strptime(data, '%Y-%m-%d'),
            id_cliente=current_user.id,
            id_oficina=oficina_id,
            id_funcionario=1
        )
        
        try:
            db.session.add(novo_relatorio)
            db.session.commit()
            flash('Manutenção agendada com sucesso!', 'success')
            return redirect(url_for('historico_veiculo'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao agendar manutenção: {str(e)}', 'danger')
    
    oficinas = Oficina.query.all()
    return render_template('agendar_manutencao.html', oficinas=oficinas)


@app.route('/criar_relatorio', methods=['GET', 'POST'])
@login_required
def criar_relatorio():
    # Verifica se é uma oficina logada
    oficina_id = session.get('oficina_id')
    if not oficina_id:
        flash('Você precisa estar logado como oficina para criar relatórios', 'danger')
        return redirect(url_for('login_oficina'))

    oficina = Oficina.query.get(oficina_id)
    if not oficina:
        flash('Oficina não encontrada', 'danger')
        return redirect(url_for('home'))

    if request.method == 'POST':
        servico = request.form.get('servico')
        descricao = request.form.get('descricao')
        id_cliente = request.form.get('id_cliente')

        novo_relatorio = Relatorio(
            servico=servico,
            descricao=descricao,
            id_cliente=id_cliente,
            id_oficina=oficina_id,
            data=datetime.now()
        )

        try:
            db.session.add(novo_relatorio)
            db.session.commit()
            flash('Relatório criado com sucesso!', 'success')
            return redirect(url_for('listar_relatorios'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao criar relatório: {str(e)}', 'danger')

    # Busca todos os clientes para o select
    clientes = User.query.filter_by(tipo='cliente').all()
    return render_template('criar_relatorio.html', clientes=clientes)

@app.route('/listar_relatorios')
@login_required
def listar_relatorios():
    oficina_id = session.get('oficina_id')
    if not oficina_id:
        flash('Você precisa estar logado como oficina para ver relatórios', 'danger')
        return redirect(url_for('login_oficina'))

    oficina = Oficina.query.get(oficina_id)
    if not oficina:
        flash('Oficina não encontrada', 'danger')
        return redirect(url_for('home'))

    relatorios = Relatorio.query.filter_by(id_oficina=oficina_id).order_by(Relatorio.data.desc()).all()
    return render_template('listar_relatorios.html', relatorios=relatorios)


@app.route('/visualizar_relatorio/<int:id>')
@login_required
def visualizar_relatorio(id):
    relatorio = Relatorio.query.get_or_404(id)

    # Verificar se o usuário tem permissão para ver o relatório
    if not (current_user.id == relatorio.id_cliente or
            (current_user.oficina and current_user.oficina.id == relatorio.id_oficina)):
        abort(403)

    return render_template('visualizar_relatorio.html', relatorio=relatorio)


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


@app.route('/login_oficina', methods=['GET', 'POST'])
def login_oficina():
    if request.method == 'POST':
        cnpj = request.form.get('cnpj')
        senha = request.form.get('password')
        
        oficina = Oficina.query.filter_by(cnpj=cnpj).first()
        
        if oficina and oficina.check_password(senha):
            # Armazena o ID da oficina na sessão
            session['oficina_id'] = oficina.id
            session['tipo_usuario'] = 'oficina'  # Marca como usuário tipo oficina
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('perfil_oficina'))
        else:
            flash('CNPJ ou senha inválidos.', 'danger')

    return render_template('login_oficina.html')


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

        # Criar e salvar a nova oficina com senha em texto claro
        try:
            nova_oficina = Oficina(nome=nome, email=email, senha=senha, cnpj=cnpj)
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
    oficina_id = session.get('oficina_id')
    if not oficina_id:
        flash('Faça login para ver o perfil.', 'warning')
        return redirect(url_for('login_oficina'))
        
    oficina = Oficina.query.get_or_404(oficina_id)

    if request.method == 'POST':
        # Lógica de atualização do perfil
        oficina.nome = request.form['nome']
        oficina.email = request.form['email']
        oficina.atendimentos = request.form.get('atendimentos', oficina.atendimentos)
        oficina.avaliacao = request.form.get('avaliacao', oficina.avaliacao)

        # Certifique-se de que 'especialidades' é uma lista válida
        especialidades = request.form.getlist('especialidades')
        oficina.especialidades = especialidades if especialidades else ['Mecânica Geral', 'Elétrica', 'Funilaria']

        oficina.horario = request.form['horario']
        
        try:
            db.session.commit()
            flash('Perfil atualizado com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar perfil: {str(e)}', 'danger')
            
        return redirect(url_for('perfil_oficina'))

    return render_template('perfil_oficina.html', oficina=oficina)

@app.route('/cadastrar_funcionario', methods=['GET', 'POST'])
def cadastrar_funcionario():
    oficina_id = session.get('oficina_id')
    if not oficina_id:
        flash('Faça login para cadastrar funcionários.', 'warning')
        return redirect(url_for('login_oficina'))
    
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        
        # Criação de um novo funcionário
        funcionario = Funcionario(nome=nome, email=email, id_oficina=oficina_id)
        funcionario.set_password(senha)

        try:
            db.session.add(funcionario)
            db.session.commit()
            flash('Funcionário cadastrado com sucesso!', 'success')
            return redirect(url_for('perfil_oficina'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cadastrar funcionário: {str(e)}', 'danger')
    
    return render_template('cadastrar_funcionario.html')

# Adicione estas rotas ao seu app.py

@app.route('/funcionarios')
@login_required
def listar_funcionarios():
    oficina_id = session.get('oficina_id')
    if not oficina_id:
        flash('Acesso permitido apenas para oficinas.', 'warning')
        return redirect(url_for('home'))
        
    funcionarios = Funcionario.query.filter_by(id_oficina=oficina_id).all()
    return render_template('funcionarios/listar.html', funcionarios=funcionarios)

@app.route('/funcionarios/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_funcionario(id):
    oficina_id = session.get('oficina_id')
    if not oficina_id:
        flash('Acesso permitido apenas para oficinas.', 'warning')
        return redirect(url_for('home'))
        
    funcionario = Funcionario.query.get_or_404(id)
    
    if funcionario.id_oficina != oficina_id:
        flash('Você não tem permissão para editar este funcionário.', 'danger')
        return redirect(url_for('listar_funcionarios'))
    
    if request.method == 'POST':
        funcionario.nome = request.form['nome']
        funcionario.email = request.form['email']
        
        if request.form.get('senha'):
            funcionario.set_password(request.form['senha'])
            
        try:
            db.session.commit()
            flash('Funcionário atualizado com sucesso!', 'success')
            return redirect(url_for('listar_funcionarios'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar funcionário: {str(e)}', 'danger')
    
    return render_template('funcionarios/editar.html', funcionario=funcionario)

@app.route('/funcionarios/deletar/<int:id>', methods=['POST'])
@login_required
def deletar_funcionario(id):
    if not session.get('oficina_id'):
        flash('Acesso não autorizado.', 'danger')
        return redirect(url_for('login_oficina'))
        
    funcionario = Funcionario.query.get_or_404(id)
    
    if funcionario.id_oficina != session['oficina_id']:
        flash('Você não tem permissão para deletar este funcionário.', 'danger')
        return redirect(url_for('listar_funcionarios'))
    
    try:
        db.session.delete(funcionario)
        db.session.commit()
        flash('Funcionário removido com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao remover funcionário: {str(e)}', 'danger')
    
    return redirect(url_for('listar_funcionarios'))

@app.route('/editar_perfil_oficina', methods=['GET', 'POST'])
def editar_perfil_oficina():
    oficina_id = session.get('oficina_id')
    if not oficina_id:
        flash('Faça login para editar o perfil.', 'warning')
        return redirect(url_for('login_oficina'))
    
    oficina = Oficina.query.get_or_404(oficina_id)
    
    if request.method == 'POST':
        try:
            oficina.nome_oficina = request.form.get('nome_oficina')
            oficina.email_oficina = request.form.get('email_oficina')
            oficina.telefone = request.form.get('telefone')
            oficina.endereco = request.form.get('endereco')
            oficina.horario = request.form.get('horario')
            oficina.horario_fds = request.form.get('horario_fds')
            oficina.especialidades = request.form.get('especialidades')
            
            if 'logo' in request.files:
                file = request.files['logo']
                if file and file.filename != '' and allowed_file(file.filename):
                    if oficina.logo:
                        old_logo_path = os.path.join(app.config['UPLOAD_FOLDER'], oficina.logo)
                        if os.path.exists(old_logo_path):
                            os.remove(old_logo_path)
                    
                    filename = secure_filename(file.filename)
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"{timestamp}_{filename}"
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    oficina.logo = filename

            db.session.commit()
            flash('Perfil atualizado com sucesso!', 'success')
            return redirect(url_for('perfil_oficina'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar perfil: {str(e)}', 'danger')
            
    return render_template('editar_perfil_oficina.html', oficina=oficina)

def check_password(self, password):
    try:
        return check_password_hash(self.senha_hash, password)
    except Exception as e:
        app.logger.error(f"Error checking password: {e}")
        return False
    
@app.context_processor
def utility_processor():
    def get_oficina():
        if session.get('oficina_id'):
            return Oficina.query.get(session['oficina_id'])
        return None

    def is_oficina():  # Agora é uma função que retorna um booleano
        return bool(session.get('oficina_id') and session.get('tipo_usuario') == 'oficina')

    return {
        'oficina': get_oficina(),
        'is_oficina': is_oficina  # Retorna a função, não o resultado
    }
# No app.py, antes do app.run()
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Finalizando a criação do banco de dados
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Isso cria o banco de dados se ainda não existir
    app.run(debug=True)

    
def create_sample_plans():
    if not Plano.query.first():
        planos = [
            Plano(
                nome='Plano Básico',
                preco=100.00,
                features=['Manutenções essenciais', 'Checagem mensal', 'Suporte básico']
            ),
            Plano(
                nome='Plano Intermediário',
                preco=200.00,
                features=['Todos os benefícios do plano básico', 'Serviços de médio porte', 'Revisões programadas', 'Suporte prioritário']
            ),
            Plano(
                nome='Plano Premium',
                preco=300.00,
                features=['Todos os benefícios do plano intermediário', 'Cobertura completa', 'Assistência 24h', 'Benefícios exclusivos']
            )
        ]
        db.session.add_all(planos)
        db.session.commit()
