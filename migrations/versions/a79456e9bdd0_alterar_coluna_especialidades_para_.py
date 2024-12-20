"""Alterar coluna especialidades para String(255)

Revision ID: a79456e9bdd0
Revises: 046b029c8ae1
Create Date: 2024-11-15 14:51:34.885750

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a79456e9bdd0'
down_revision = '046b029c8ae1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('oficina', schema=None) as batch_op:
        batch_op.alter_column('senha',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.String(length=512),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('oficina', schema=None) as batch_op:
        batch_op.alter_column('senha',
               existing_type=sa.String(length=512),
               type_=mysql.VARCHAR(length=255),
               existing_nullable=False)

    # ### end Alembic commands ###
