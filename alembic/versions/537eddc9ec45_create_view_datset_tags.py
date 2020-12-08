"""create view/datset tags

Revision ID: 537eddc9ec45
Revises: e163b4a958de
Create Date: 2020-12-05 22:51:01.381861

"""
import sys
sys.path = ['', '..'] + sys.path[1:]

from alembic import op
import sqlalchemy as sa
from application.database import ReplaceableObject


# revision identifiers, used by Alembic.
revision = '537eddc9ec45'
down_revision = 'e163b4a958de'
branch_labels = None
depends_on = None

tag_dataset_view = ReplaceableObject(
    "tag_dataset_popular_view",
    """
    SELECT public.tag.id,
    public.tag.tag_name,
    COUNT(public.dataset_tag.id)
    FROM public.tag
    INNER JOIN public.dataset_tag ON public.dataset_tag.tag_id = public.tag.id
    GROUP BY public.tag.id;
    """
)

type_dataset_view = ReplaceableObject(
    "type_dataset_popular_view",
    """
    SELECT public.file_type.id,
    public.file_type.type_name,
    COUNT(public.dataset_type.id)
    FROM public.file_type
    INNER JOIN public.dataset_type ON public.dataset_type.file_type_id = public.file_type.id
    GROUP BY public.file_type.id;
    """
)

def upgrade():
    op.create_view(tag_dataset_view)
    op.create_view(type_dataset_view)


def downgrade():
    op.drop_view(tag_dataset_view)
    op.drop_view(type_dataset_view)

