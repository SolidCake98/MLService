"""create trigger/on add rating

Revision ID: dc5ecc911c80
Revises: 2e5a8de138c1
Create Date: 2020-11-23 17:05:59.013807

"""
from alembic import op
import sqlalchemy as sa
from application.database import ReplaceableObject


# revision identifiers, used by Alembic.
revision = 'dc5ecc911c80'
down_revision = '2e5a8de138c1'
branch_labels = None
depends_on = None


update_dataset_rating = ReplaceableObject(
    "update_dataset_rating()",
    """
    RETURNS TRIGGER AS $$
    DECLARE
        d_id integer;
    BEGIN
        IF (TG_OP = 'DELETE') THEN
            d_id = OLD.dataset_id;
        ELSE
            d_id = NEW.dataset_id;
        END IF;
     
        UPDATE dataset SET

        rating = 
        (
            SELECT AVG(public.user_rating.rating) FROM public.user_rating
            WHERE public.user_rating.dataset_id = d_id
            GROUP BY public.user_rating.dataset_id
        )

        WHERE id = d_id;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """
)

before_dataset_rating = ReplaceableObject(
    "before_dataset_rating()",
    """
    RETURNS TRIGGER AS $$
    DECLARE
        rating_id int;
    BEGIN
        SELECT id INTO STRICT rating_id FROM public.user_rating WHERE dataset_id = NEW.dataset_id AND user_id = NEW.user_id;
        EXCEPTION
            WHEN NO_DATA_FOUND THEN
                RETURN NEW;
        IF FOUND THEN 
            RAISE EXCEPTION 'you can''t add review, because you''ve already added it';
        END IF;
    END;
    $$ LANGUAGE plpgsql;
    """
)

update_trigger = ReplaceableObject(
    "dataset_rating",
    """
    AFTER INSERT OR UPDATE OR DELETE ON public.user_rating
    FOR EACH ROW EXECUTE PROCEDURE update_dataset_rating();
    """
)

before_insert_trigger = ReplaceableObject(
    "before_dataset_rating",
    """
    BEFORE INSERT ON public.user_rating
    FOR EACH ROW EXECUTE PROCEDURE before_dataset_rating();
    """
)

delete_trigger = ReplaceableObject(
    "dataset_rating",
    """
    ON public.user_rating
    """
)

delete_before_trigger = ReplaceableObject(
    "before_dataset_rating",
    """
    ON public.user_rating
    """
)

def upgrade():
    op.create_sp(update_dataset_rating)
    op.create_tr(update_trigger)

    op.create_sp(before_dataset_rating)
    op.create_tr(before_insert_trigger)


def downgrade():
    op.drop_tr(delete_trigger)
    op.drop_sp(update_dataset_rating)

    op.drop_tr(delete_before_trigger)
    op.drop_sp(before_dataset_rating)

