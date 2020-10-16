from application.database import db_session, engine
from application import models
from application.facades.abstract_facade import AbstractFacade

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


class UserGroupFacade(AbstractFacade):

    def __init__(self):
        super().__init__(models.User)

    def get_user_groups(self, user):
        return models.UserGroup.query.filter_by(id=user.id).all()

class DataSetFacade(AbstractFacade):

    def __init__(self):
        super().__init__(models.DataSet)

    def get_dataset_by_name(self, name: str):
        return models.DataSet.query.filter_by(name=name).first()

    def get_dataset_by_user_and_data(self, user: str, data:str):
        return models.DataSet.query.join(models.User).filter(models.User.username == user, \
        models.DataSet.name == data).first()
        

class TagFacade(AbstractFacade):

    def __init__(self):
        super().__init__(models.Tag)

    def get_tag_by_name(self, name: str):
        return models.Tag.query.filter_by(tag_name=name).first()


class DataSetTagFacade(AbstractFacade):

    def __init__(self):
        super().__init__(models.DataSetTag)


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