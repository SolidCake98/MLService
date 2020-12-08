"""create procedure/add user to group

Revision ID: 0af56aac10be
Revises: d9522989ab93
Create Date: 2020-12-06 21:56:22.579446

"""
import sys
sys.path = ['', '..'] + sys.path[1:]

from alembic import op
import sqlalchemy as sa
from application.database import ReplaceableObject


# revision identifiers, used by Alembic.
revision = '0af56aac10be'
down_revision = 'd9522989ab93'
branch_labels = None
depends_on = None

add_u_to_group = ReplaceableObject(
    "add_user_to_group(username_who_add character varying, username_to_add character varying, group_name character varying)",
    """
    RETURNS void AS $$
    DECLARE
        user_admin integer;
        user_add integer;
        group_id integer;
    BEGIN

        group_id := (SELECT id FROM public.group WHERE name = group_name);
        if group_id is null THEN
            RAISE EXCEPTION 'group doesn''t exist';
        END IF;


        user_admin := (SELECT id FROM public.user 
        WHERE id in 
        (SELECT public.user_group.user_id FROM public.user_group 
        INNER JOIN public.group ON public.group.id = public.user_group.group_id
        WHERE public.group.name = 'admin')
        AND username = username_who_add);

        if user_admin is null THEN
            RAISE EXCEPTION 'this user doesn''t have permission to add user to group';
        END IF;
        
        user_add := (SELECT id FROM public.user WHERE username_to_add = username);
        if user_add is null THEN
            RAISE EXCEPTION 'user to add doesn''t exist';
        END IF;

        IF group_id in (SELECT public.user_group.group_id FROM public.user_group WHERE public.user_group.user_id = user_add) THEN
            RAISE EXCEPTION 'user already in group';
        END IF;

        INSERT INTO public.user_group (user_id, group_id) VALUES(user_add, group_id);
    END;
    $$ LANGUAGE plpgsql;
    """
)

def upgrade():
    op.create_sp(add_u_to_group)


def downgrade():
    op.drop_sp(add_u_to_group)
