from application.database import db_session, engine
from application import models
from application.facades.abstract_facade import AbstractFacade
from sqlalchemy import text, desc, nullslast


class UserFacade(AbstractFacade):

    def __init__(self):
        super().__init__(models.User)

    def get_user_by_username(self, username: str):
        return models.User.query.filter_by(username=username).first()

    def get_user_by_email(self, email: str):
        return models.User.query.filter_by(email=email).first()


class GroupFacade(AbstractFacade):

    def __init__(self):
        super().__init__(models.Group)

    def get_group_by_name(self, name: str):
        return models.Group.query.filter_by(name=name).first()

    def get_excluded_groups(self, user_id:int):
        sub_q = models.UserGroup.query.filter(models.UserGroup.user_id == user_id).subquery()
        return models.Group.query.join(sub_q, models.Group.id == sub_q.c.group_id, isouter=True).\
        filter(sub_q.c.id == None).all()


class UserGroupFacade(AbstractFacade):

    def __init__(self):
        super().__init__(models.User)

    def get_user_groups(self, user):
        return models.UserGroup.query.filter_by(id=user.id).all()

    def add_user_to_group(self, admin, user, group):
        db_session.execute(text(f"SELECT add_user_to_group('{admin}', '{user}', '{group}')"))
        db_session.commit()


class DataSetFacade(AbstractFacade):

    def __init__(self):
        super().__init__(models.DataSet)

    def get_dataset_by_name(self, name: str):
        return models.DataSet.query.filter_by(name=name).first()

    def get_dataset_ordered_by_data(self):
        return models.DataSet.query.order_by(desc(models.DataSet.date_load)).all()

    def get_with_similarity_title(self, word):
        result = db_session.execute(text(f"SELECT id, word_similarity(title, '{word}') \
            as sml FROM public.dataset WHERE '{word}' <% title ORDER BY sml DESC;"))

        pr = [rowproxy for rowproxy in result]
        res = [(column, value) for column, value in pr]
        datasets = [models.DataSet.query.filter(models.DataSet.id==el[0]).first() for el in res]
        return datasets

    def get_dataset_by_tags(self, tags):
        result = db_session.execute(text(f"SELECT id FROM find_dataset_by_tag(array{tags})"))

        pr = [rowproxy for rowproxy in result]
        res = [column for column in pr]
        datasets = [models.DataSet.query.filter(models.DataSet.id==el[0]).first() for el in res]

        return datasets

    def get_dataset_ordered_by_last_month(self):

        return models.DataSet.query.outerjoin(models.RatingDataSetLastMonth,\
         models.RatingDataSetLastMonth.id == models.DataSet.id).\
        order_by(nullslast(desc(models.RatingDataSetLastMonth.count))).all()

    def get_dataset_by_user_and_data(self, user: str, data:str):
        return models.DataSet.query.join(models.User).filter(models.User.username == user, \
        models.DataSet.name == data).first()
        

class TagFacade(AbstractFacade):

    def __init__(self):
        super().__init__(models.Tag)

    def get_tag_by_name(self, name: str):
        return models.Tag.query.filter_by(tag_name=name).first()

    def get_with_similarity_tag(self, word):
        result = db_session.execute(text(f"SELECT id, word_similarity(tag_name, '{word}') \
        as sml FROM public.tag ORDER BY sml DESC;"))

        pr = [rowproxy for rowproxy in result]
        res = [(column, value) for column, value in pr]

        tags = [models.Tag.query.filter(models.Tag.id==el[0]).first() for el in res]
        return tags 


class DataSetTagFacade(AbstractFacade):

    def __init__(self):
        super().__init__(models.DataSetTag)

    def add_tags(self, id, tags):
        db_session.execute(text(f"SELECT add_tags({id}, array{tags})"))
        db_session.commit()


class DataSetMetaFacade(AbstractFacade):
    def __init__(self):
        super().__init__(models.DataSetMeta)


class FileTypeFacade(AbstractFacade):
    def __init__(self):
        super().__init__(models.FileType)

    def get_type_by_name(self, name: str):
        return models.FileType.query.filter_by(type_name=name).first()


class DataSetTypeFacade(AbstractFacade):
    def __init__(self):
        super().__init__(models.DataSetType)


class CountDatasetFacade(AbstractFacade):
    def __init__(self):
        super().__init__(models.CountDataset)


class UserRatingFacade(AbstractFacade):
    def __init__(self):
        super().__init__(models.UserRating)


class DataSetTableFacade(AbstractFacade):
    def __init__(self):
        super().__init__(models.DataSetTable)


class DataSetColumnSourceFacade(AbstractFacade):
    def __init__(self):
        super().__init__(models.DataSetColumnSource)


class DataSetColumnVersionedFacade(AbstractFacade):
    def __init__(self):
        super().__init__(models.DataSetColumnVersioned)


class DataTypeFacade(AbstractFacade):
    def __init__(self):
        super().__init__(models.DataType)


class AggregationFacade(AbstractFacade):
    def __init__(self):
        super().__init__(models.Aggregation)


class DataTypeAggregationFacade(AbstractFacade):
    def __init__(self):
        super().__init__(models.DataTypeAggregation)

    def get_type_aggregation(self, aggr: str, type:str):
        return models.DataTypeAggregation.query.join(models.DataType).join(models.Aggregation).filter(models.DataType.name == type, \
        models.Aggregation.name == aggr).first()