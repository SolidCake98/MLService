"""create procedure/get by tag

Revision ID: 2e5a8de138c1
Revises: 905c7387f4dd
Create Date: 2020-11-23 15:56:52.124424

"""
import sys
sys.path = ['', '..'] + sys.path[1:]

from alembic import op
import sqlalchemy as sa
from application.database import ReplaceableObject

# revision identifiers, used by Alembic.
revision = '2e5a8de138c1'
down_revision = '395cbd3628b0'
branch_labels = None
depends_on = None

find_by_tag = ReplaceableObject(
    "find_dataset_by_tag(tag_names character varying[])",
    """
    RETURNS TABLE (id integer, dataset_name character varying) AS $$
    BEGIN
        RETURN QUERY 
        SELECT public.dataset.id, public.dataset.name
        FROM public.dataset
        WHERE NOT EXISTS 
        (SELECT * FROM UNNEST(tag_names) EXCEPT
        SELECT public.tag.tag_name FROM public.tag
        JOIN public.dataset_tag ON public.tag.id = public.dataset_tag.tag_id
        WHERE public.dataset_tag.dataset_id = public.dataset.id); 
        
    END;
    $$ LANGUAGE plpgsql;
    """
)

def upgrade():
    op.create_sp(find_by_tag)


def downgrade():
    op.drop_sp(find_by_tag)
