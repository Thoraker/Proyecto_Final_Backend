"""empty message

Revision ID: e02e3d627a0b
Revises: 4004c0eada4a
Create Date: 2023-06-20 00:34:00.045137

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e02e3d627a0b'
down_revision = '4004c0eada4a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('addresses', schema=None) as batch_op:
        batch_op.drop_constraint('addresses_public_id_key', type_='unique')
        batch_op.drop_column('public_id')

    with op.batch_alter_table('portfolios', schema=None) as batch_op:
        batch_op.drop_constraint('portfolios_public_id_key', type_='unique')
        batch_op.drop_column('public_id')

    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_constraint('posts_public_id_key', type_='unique')
        batch_op.drop_column('public_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('public_id', sa.VARCHAR(length=50), autoincrement=False, nullable=False))
        batch_op.create_unique_constraint('posts_public_id_key', ['public_id'])

    with op.batch_alter_table('portfolios', schema=None) as batch_op:
        batch_op.add_column(sa.Column('public_id', sa.VARCHAR(length=50), autoincrement=False, nullable=False))
        batch_op.create_unique_constraint('portfolios_public_id_key', ['public_id'])

    with op.batch_alter_table('addresses', schema=None) as batch_op:
        batch_op.add_column(sa.Column('public_id', sa.VARCHAR(length=50), autoincrement=False, nullable=False))
        batch_op.create_unique_constraint('addresses_public_id_key', ['public_id'])

    # ### end Alembic commands ###