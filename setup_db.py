from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Oficina
from config import Config

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

def setup_database():
    # Crie a tabela Oficina no banco de dados
    Oficina.metadata.create_all(engine)

    # Crie algumas instâncias de exemplo da classe Oficina
    oficina1 = Oficina(
        nome='Oficina 1',
        email='oficina1@example.com',
        senha='senha123',
        cnpj='12345678901234',
        endereco='Endereço da Oficina 1',
        telefone='123456789'
    )

    oficina2 = Oficina(
        nome='Oficina 2',
        email='oficina2@example.com',
        senha='senha456',
        cnpj='98765432109876',
        endereco='Endereço da Oficina 2',
        telefone='987654321'
    )

    # Adicione as instâncias à sessão do banco de dados
    session.add_all([oficina1, oficina2])

    # Confirme as alterações no banco de dados
    session.commit()

if __name__ == '__main__':
    setup_database()
    print("Banco de dados configurado com sucesso!")