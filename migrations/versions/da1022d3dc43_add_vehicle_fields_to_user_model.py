"""Add vehicle fields to User model

Revision ID: da1022d3dc43
Revises: 
Create Date: 2024-11-06 22:15:10.642205

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'da1022d3dc43'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('marca', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('modelo', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('ano_fabricacao', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('cor', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('placa', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('renavam', sa.String(length=20), nullable=True))
        batch_op.alter_column('password',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.String(length=150),
               nullable=False)
        batch_op.drop_column('carro_modelo')
        batch_op.drop_column('carro_marca')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('carro_marca', mysql.VARCHAR(length=100), nullable=True))
        batch_op.add_column(sa.Column('carro_modelo', mysql.VARCHAR(length=120), nullable=True))
        batch_op.alter_column('password',
               existing_type=sa.String(length=150),
               type_=mysql.VARCHAR(length=255),
               nullable=True)
        batch_op.drop_column('renavam')
        batch_op.drop_column('placa')
        batch_op.drop_column('cor')
        batch_op.drop_column('ano_fabricacao')
        batch_op.drop_column('modelo')
        batch_op.drop_column('marca')

    # ### end Alembic commands ###
