"""date rating

Revision ID: 0a7099e03695
Revises: dd186ad9db27
Create Date: 2020-12-05 22:28:22.971710

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a7099e03695'
down_revision = 'dd186ad9db27'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_rating', sa.Column('create_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_rating', 'create_time')
    # ### end Alembic commands ###
