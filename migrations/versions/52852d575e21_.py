"""empty message

Revision ID: 52852d575e21
Revises: 01c9afc5a7ad
Create Date: 2023-06-16 04:43:38.272052

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '52852d575e21'
down_revision = '01c9afc5a7ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'users', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###