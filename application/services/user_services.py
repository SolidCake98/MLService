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
            password = data["password"]
        )


        return new_user


    def create_user_group(self, user: models.User, type_group: str):

        user_group = models.UserGroup(
            user = user,
            group = self.g_facade.get_group_by_name(type_group)
        )

        return user_group

    def create_jwt(self, user: models.User):
        json = {'id' : user.id, 'username' : user.username}
        jwt = GenereteJWTService(json)

        access_token = jwt.generate_access_token()
        refresh_token = jwt.generate_refresh_token()

        return access_token, refresh_token


    def registrate(self):
        user          = self.create_user()
        user_group    = self.create_user_group(user, "user")
        validate_user = UserValidateProcess(user)

        try:
            validate_user.validate()
        except ValueError as ex:
            return 400, {"error" : str(ex)}

        user.password = models.User.generate_hash(user.password)

        try:
            self.u_facade.create(user)
            self.ug_facade.create(user_group)
            a_token, r_token = self.create_jwt(user)
        except:
            return 500, {"error": "Internal server error"}

        return 200, {
            "message"       : f'User {user.username} was registred',
            "access_token"  : a_token,
            "refresh_token" : r_token
        }



class GenereteJWTService:

    def __init__(self, json):
        self.json = json

    def generate_access_token(self):
        return create_access_token(identity = self.json)

    def generate_refresh_token(self):
        return create_refresh_token(identity = self.json)


        