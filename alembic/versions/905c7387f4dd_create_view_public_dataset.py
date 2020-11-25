"""create view/public dataset

Revision ID: 905c7387f4dd
Revises: f149083566ab
Create Date: 2020-11-19 21:40:24.983263

"""
from alembic import op
import sqlalchemy as sa
from application.database import ReplaceableObject

# revision identifiers, used by Alembic.
revision = '905c7387f4dd'
down_revision = 'f149083566ab'
branch_labels = None
depends_on = None


public_dataset_view = ReplaceableObject(
    "public_dataset",
    """
    select *
    FROM public.dataset WHERE public.dataset.is_public = true;
    """
)

def upgrade():
    op.create_view(public_dataset_view)


def downgrade():
    op.drop_view(public_dataset_view)
