"""create view/count ratings

Revision ID: e163b4a958de
Revises: 0a7099e03695
Create Date: 2020-12-05 22:33:35.107161

"""
import sys
sys.path = ['', '..'] + sys.path[1:]

from alembic import op
import sqlalchemy as sa
from application.database import ReplaceableObject


# revision identifiers, used by Alembic.
revision = 'e163b4a958de'
down_revision = '0a7099e03695'
branch_labels = None
depends_on = None

count_dataset_rating_last_month = ReplaceableObject(
    "rating_last_month",
    """
    SELECT 
    public.dataset.id, 
    public.dataset.name,
    public.dataset.title,
    COUNT(public.user_rating.id),
    AVG(public.user_rating.rating)
    FROM public.dataset
    INNER JOIN  public.user_rating ON public.dataset.id = public.user_rating.dataset_id
    WHERE public.user_rating.create_time >= (current_timestamp - interval '30 days')
    GROUP BY public.dataset.id;
    """
)

def upgrade():
    op.create_view(count_dataset_rating_last_month)


def downgrade():
    op.drop_view(count_dataset_rating_last_month)
    
