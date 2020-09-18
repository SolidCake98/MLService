from application import schemas, models
from application.services.validate_service import UserValidateProcess
from application.facades.facades import UserFacade, GroupFacade, UserGroupFacade
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
)


#TODO add validation

class RegistrationService:


    def __init__(self, json):
        self.json = json
        self.g_facade = GroupFacade()
        self.u_facade = UserFacade()
        self.ug_facade = UserGroupFacade()

    def create_user(self):
        data = schemas.UserSchema().load(data=self.json)

        new_user = models.User(
            username = data["username"],
            email    = data["email"],
            password = models.User.generate_hash(data["password"])
        )

        return new_user


    def create_user_group(self, user: models.User, type_group: str):

        user_group = models.UserGroup(
            user = user,
            group = self.g_facade.get_group_by_name(type_group)
        )

        return user_group

    def registrate(self):
        user         = self.create_user()
        user_group   = self.create_user_group(user, "user")
        validate     = UserValidateProcess(user)

        try:

            self.u_facade.create(user)
            self.ug_facade.create(user_group)

        except Exception as err:

            return {"error": err}


class GenereteJWTService:

    def __init__(json):
        self.json = json

    def generate_access_token(self):
        return create_access_token(identity = json)

    def generate_refresh_token(self):
        return create_refresh_token(identity = json)


        