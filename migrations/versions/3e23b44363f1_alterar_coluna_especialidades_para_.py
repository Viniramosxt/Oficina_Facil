"""Alterar coluna especialidades para String(255)

Revision ID: 3e23b44363f1
Revises: a79456e9bdd0
Create Date: 2024-11-15 14:53:31.356835

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3e23b44363f1'
down_revision = 'a79456e9bdd0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('oficina', schema=None) as batch_op:
        batch_op.alter_column('especialidades',
               existing_type=mysql.TEXT(),
               type_=sa.String(length=255),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('oficina', schema=None) as batch_op:
        batch_op.alter_column('especialidades',
               existing_type=sa.String(length=255),
               type_=mysql.TEXT(),
               existing_nullable=True)

    # ### end Alembic commands ###
