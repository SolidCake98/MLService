"""Add name of size

Revision ID: 33d2a96750b8
Revises: 03237b05132f
Create Date: 2020-10-21 21:31:03.100225

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33d2a96750b8'
down_revision = '03237b05132f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dataset_meta', sa.Column('size_name', sa.String(length=20), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('dataset_meta', 'size_name')
    # ### end Alembic commands ###
