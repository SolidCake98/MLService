"""create view/count-dataset

Revision ID: 395cbd3628b0
Revises: 4539cbf31e1c
Create Date: 2020-11-18 17:36:28.765853

"""
import sys
sys.path = ['', '..'] + sys.path[1:]

from alembic import op
import sqlalchemy as sa
from application.database import ReplaceableObject


# revision identifiers, used by Alembic.
revision = '395cbd3628b0'
down_revision = '4539cbf31e1c'
branch_labels = None
depends_on = None

count_dataset_view = ReplaceableObject(
    "count_dataset",
    """
    SELECT public.user.id,
    public.user.username,
    COUNT(public.dataset.name),
    AVG(public.dataset.rating)
    FROM public.dataset JOIN public.user ON public.dataset.owner_id = public.user.id GROUP BY public.user.id;
    """
)

def upgrade():
    op.create_view(count_dataset_view)


def downgrade():
    op.drop_view(count_dataset_view)