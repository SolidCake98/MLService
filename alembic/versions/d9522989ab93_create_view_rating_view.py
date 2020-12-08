"""create view/rating view

Revision ID: d9522989ab93
Revises: 537eddc9ec45
Create Date: 2020-12-05 23:08:51.843400

"""
import sys
sys.path = ['', '..'] + sys.path[1:]

from alembic import op
import sqlalchemy as sa
from application.database import ReplaceableObject


# revision identifiers, used by Alembic.
revision = 'd9522989ab93'
down_revision = '537eddc9ec45'
branch_labels = None
depends_on = None

rating_dataset_view = ReplaceableObject(
    "user_rating_dataset",
    """
    select public.user_rating.id,
    public.dataset.name,
    public.user.username,
    public.user_rating.commenatary,
    public.user_rating.rating,
    public.user_rating.create_time
    FROM public.user_rating
    INNER JOIN public.dataset ON public.dataset.id = public.user_rating.dataset_id
    INNER JOIN public.user ON public.user.id = public.user_rating.user_id
    ORDER BY public.user_rating.create_time;
    """
)

def upgrade():
    op.create_view(rating_dataset_view)


def downgrade():
    op.drop_view(rating_dataset_view)
