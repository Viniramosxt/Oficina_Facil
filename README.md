# 🚗 Oficina Fácil

**Oficina Fácil** é uma aplicação web projetada para oferecer planos de manutenção para veículos, com foco em manutenção preventiva e corretiva. O sistema facilita o gerenciamento de clientes, veículos e serviços oferecidos, proporcionando uma experiência eficiente e acessível para oficinas e proprietários de veículos.

## 🌟 Funcionalidades

- **📋 Cadastro de Clientes e Veículos**: Permite que clientes registrem informações sobre seus veículos e dados pessoais.
- **🛠️ Planos de Manutenção**: Oferece planos diferenciados (básico, intermediário e premium) para manutenção dos veículos, com coberturas que variam de serviços preventivos a reparos completos.
- **📊 Consulta de Histórico**: Registra e exibe o histórico de serviços realizados em cada veículo.
- **🔒 Autenticação de Usuário**: Sistema de login seguro com hash de senha e proteção de dados.
- **🚗 Histórico de Manutenções**: Acompanhamento do histórico de manutenção de cada veículo registrado.

## 💻 Tecnologias Utilizadas

- **Back-end**: Python com o framework Flask para gerenciar rotas, autenticação e interação com o banco de dados.
- **Banco de Dados**: MySQL, com SQLAlchemy para ORM (Object-Relational Mapping), facilitando a manipulação dos dados.
- **Front-end**: HTML, CSS (SCSS) e Bootstrap para uma interface amigável e responsiva.
- **Autenticação e Segurança**: Utiliza o werkzeug.security para hash de senha.
- **Geolocalização**: Implementação de geolocalização para melhorar a personalização de planos de manutenção com base na cidade do usuário.

## 🗂️ Estrutura do Projeto

```plaintext
Oficina_Facil/
├── app.py                  # Arquivo principal para rodar a aplicação
├── config.py               # Configurações do Flask e banco de dados
├── extensions.py           # Extensões e integrações do Flask (Ex: Flask-Login)
├── forms.py                # Definição dos formulários para cadastro e edição de dados
├── manage.py               # Script de gerenciamento do projeto (ex: migrações, gerenciamento de banco de dados)
├── models.py               # Modelos de dados (definições das tabelas)
├── requirements.txt        # Dependências do projeto (Flask, SQLAlchemy, etc.)
├── .gitignore              # Arquivo para ignorar arquivos temporários e de configuração
├── README.md               # Este arquivo
├── _pycache_/              # Cache de Python (pasta gerada automaticamente)
├── .venv                   # Ambiente virtual (não versionado no Git)
├── migrations/             # Diretório de migrações do banco de dados (se utilizado Alembic)
├── static/                 # Diretório para arquivos estáticos (CSS, JS, imagens, uploads)
│   ├── css/                
│   │   └── style.css       # Arquivo de estilos (CSS)
│   ├── js/
│   │   └── localizacao.js  # Script de geolocalização
│   ├── images/
│   │   └── logo.png       # Logo da aplicação
│   └── uploads/            # Diretório para armazenar arquivos enviados pelos usuários (ex: imagens, documentos)
├── templates/              # Diretório para armazenar os arquivos HTML/Pug
│   ├── base.html           # Layout base para as páginas
│   ├── edit_profile.html   # Página de edição de perfil do usuário
│   ├── historico_veiculo.html  # Histórico de manutenções do veículo
│   ├── index.html          # Página inicial
│   ├── index.pug           # Versão Pug da página inicial
│   ├── login.html          # Página de login
│   ├── manutencao_preventiva.html # Página de manutenção preventiva
│   ├── perfil.html         # Página de perfil do usuário
│   ├── register.html       # Página de registro de novos usuários
│   ├── reparos_emergencia.html # Página de reparos emergenciais
│   └── servicos.html       # Página com os serviços oferecidos

