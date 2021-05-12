"""add index to columns

Revision ID: 66e54c03ba78
Revises: 1cb3c0789e11
Create Date: 2021-04-04 17:19:10.641702

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66e54c03ba78'
down_revision = '1cb3c0789e11'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dataset_column_source', sa.Column('index', sa.Integer(), nullable=True))
    op.add_column('dataset_column_versioned', sa.Column('index', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('dataset_column_versioned', 'index')
    op.drop_column('dataset_column_source', 'index')
    # ### end Alembic commands ###