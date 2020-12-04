"""create view/user-datasets

Revision ID: 4539cbf31e1c
Revises: 33d2a96750b8
Create Date: 2020-11-18 13:13:54.670908

"""
import sys
sys.path = ['', '..'] + sys.path[1:]

from alembic import op
import sqlalchemy as sa
from application.database import ReplaceableObject

# revision identifiers, used by Alembic.
revision = '4539cbf31e1c'
down_revision = '33d2a96750b8'
branch_labels = None
depends_on = None

user_dataset_view = ReplaceableObject(
    "user_dataset",
    """
    select public.dataset.id,
    public.user.username,
    public.dataset.name, 
    public.dataset.title,
    public.dataset_meta.size,
    public.dataset_meta.size_name
    FROM public.dataset 
    INNER JOIN public.user ON public.dataset.owner_id = public.user.id
    INNER JOIN public.dataset_meta ON public.dataset.meta_id = public.dataset_meta.id;
    """
)

def upgrade():
    op.create_view(user_dataset_view)


def downgrade():
    op.drop_view(user_dataset_view)
