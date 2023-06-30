"""empty message

Revision ID: b9439eb65f62
Revises: dc9b33f1db53
Create Date: 2023-06-30 15:21:24.016296

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9439eb65f62'
down_revision = 'dc9b33f1db53'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('portfolios', schema=None) as batch_op:
        batch_op.alter_column('url',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=150),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('portfolios', schema=None) as batch_op:
        batch_op.alter_column('url',
               existing_type=sa.String(length=150),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)

    # ### end Alembic commands ###
