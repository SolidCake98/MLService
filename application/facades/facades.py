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




 
 