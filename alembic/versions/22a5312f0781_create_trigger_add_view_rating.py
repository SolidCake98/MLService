"""create trigger/add view rating

Revision ID: 22a5312f0781
Revises: 0af56aac10be
Create Date: 2020-12-08 15:06:26.807181

"""
import sys
sys.path = ['', '..'] + sys.path[1:]

from alembic import op
import sqlalchemy as sa
from application.database import ReplaceableObject


# revision identifiers, used by Alembic.
revision = '22a5312f0781'
down_revision = '0af56aac10be'
branch_labels = None
depends_on = None

change_dataset_rating_view = ReplaceableObject(
    "change_dataset_rating()",
    """
    RETURNS TRIGGER AS $$
    BEGIN
        IF (TG_OP = 'DELETE') THEN
            DELETE FROM public.user_rating WHERE id = NEW.id;
        END IF;

        IF (TG_OP = 'INSERT') THEN
            INSERT INTO public.user_rating(dataset_id, user_id, rating, commenatary, create_time)
            SELECT public.dataset.id, public.user.id, NEW.rating, NEW.commenatary, NEW.create_time
            FROM public.dataset 
            JOIN public.user ON public.user.username = NEW.username
            WHERE public.dataset.name = NEW.name
            RETURNING public.user_rating.id
            INTO NEW.id;

            IF NOT FOUND THEN  -- insert was canceled
                RAISE WARNING 'Skipping INSERT.';
            END IF;
        END IF;

        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """
)

change_datase_rating_trigger = ReplaceableObject(
    "dataset_rating_view",
    """
    INSTEAD OF INSERT OR DELETE ON public.user_rating_dataset
    FOR EACH ROW EXECUTE PROCEDURE change_dataset_rating();
    """
)

delete_trigger = ReplaceableObject(
    "dataset_rating_view",
    """
    ON public.user_rating_dataset
    """
)

def upgrade():
    op.create_sp(change_dataset_rating_view)
    op.create_tr(change_datase_rating_trigger)


def downgrade():
    op.drop_tr(delete_trigger)
    op.drop_sp(change_dataset_rating_view)
