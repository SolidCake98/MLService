"""create procedure/add tags

Revision ID: dd186ad9db27
Revises: dc5ecc911c80
Create Date: 2020-11-28 17:53:12.913945

"""
import sys
sys.path = ['', '..'] + sys.path[1:]

from alembic import op
import sqlalchemy as sa
from application.database import ReplaceableObject


# revision identifiers, used by Alembic.
revision = 'dd186ad9db27'
down_revision = 'dc5ecc911c80'
branch_labels = None
depends_on = None


add_tags = ReplaceableObject(
    "add_tags(data_id integer,tag_names character varying[])",
    """
    RETURNS void AS $$
    DECLARE
        d_id integer;
        t_id integer;
        t character varying;
    BEGIN
        SELECT id INTO STRICT d_id FROM public.dataset WHERE id = data_id;
        
        FOREACH t IN ARRAY tag_names LOOP
            
            d_id := (SELECT dataset_id FROM public.dataset_tag 
            WHERE public.dataset_tag.dataset_id = data_id 
            AND public.dataset_tag.tag_id = (SELECT id from public.tag WHERE tag_name = t));
            t_id := (SELECT id FROM public.tag WHERE tag_name = t);
            IF (d_id is not null) OR (t_id is null) THEN
                RAISE EXCEPTION 'can''t add tags';
            END IF;
            INSERT INTO public.dataset_tag (dataset_id, tag_id) 
            VALUES(data_id, t_id);
        END LOOP;
        
    END;
    $$ LANGUAGE plpgsql;
    """
)

def upgrade():
    op.create_sp(add_tags)


def downgrade():
    op.drop_sp(add_tags)
