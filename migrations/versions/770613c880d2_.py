"""empty message

Revision ID: 770613c880d2
Revises: 5b034a8d456b
Create Date: 2023-06-30 16:14:45.648061

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '770613c880d2'
down_revision = '5b034a8d456b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pets', schema=None) as batch_op:
        batch_op.drop_column('photo_url')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pets', schema=None) as batch_op:
        batch_op.add_column(sa.Column('photo_url', sa.VARCHAR(length=100), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
