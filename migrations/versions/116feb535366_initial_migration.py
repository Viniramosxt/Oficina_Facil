"""initial migration

Revision ID: 116feb535366
Revises: 
Create Date: 2024-11-12 21:24:36.361808

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '116feb535366'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('plano',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=False),
    sa.Column('preco', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=150), nullable=False),
    sa.Column('email', sa.String(length=150), nullable=False),
    sa.Column('password', sa.String(length=150), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('marca', sa.String(length=50), nullable=True),
    sa.Column('modelo', sa.String(length=50), nullable=True),
    sa.Column('ano_fabricacao', sa.String(length=4), nullable=True),
    sa.Column('cor', sa.String(length=30), nullable=True),
    sa.Column('placa', sa.String(length=7), nullable=True),
    sa.Column('renavam', sa.String(length=11), nullable=True),
    sa.Column('foto_perfil', sa.String(length=200), nullable=True),
    sa.Column('foto_crlv', sa.String(length=200), nullable=True),
    sa.Column('plano_assinado_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['plano_assinado_id'], ['plano.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('oficina',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('senha', sa.Text(), nullable=False),
    sa.Column('cnpj', sa.String(length=14), nullable=False),
    sa.Column('endereco', sa.String(length=255), nullable=True),
    sa.Column('telefone', sa.String(length=50), nullable=True),
    sa.Column('logo', sa.String(length=255), nullable=True),
    sa.Column('lat', sa.Float(), nullable=True),
    sa.Column('lon', sa.Float(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('atendimentos', sa.Integer(), nullable=True),
    sa.Column('avaliacao', sa.Float(), nullable=True),
    sa.Column('especialidades', sa.Text(), nullable=True),
    sa.Column('horario', sa.String(length=255), nullable=True),
    sa.Column('horario_fds', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cnpj'),
    sa.UniqueConstraint('email')
    )
    op.create_table('funcionario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('senha', sa.String(length=150), nullable=False),
    sa.Column('id_oficina', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_oficina'], ['oficina.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('relatorio',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data', sa.Date(), nullable=False),
    sa.Column('servico', sa.String(length=100), nullable=False),
    sa.Column('descricao', sa.Text(), nullable=True),
    sa.Column('id_funcionario', sa.Integer(), nullable=False),
    sa.Column('id_cliente', sa.Integer(), nullable=False),
    sa.Column('id_oficina', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_cliente'], ['user.id'], ),
    sa.ForeignKeyConstraint(['id_funcionario'], ['funcionario.id'], ),
    sa.ForeignKeyConstraint(['id_oficina'], ['oficina.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('relatorio')
    op.drop_table('funcionario')
    op.drop_table('oficina')
    op.drop_table('user')
    op.drop_table('plano')
    # ### end Alembic commands ###