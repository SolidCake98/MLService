from application import schemas, models
from application.services.validate_service import (
    UserValidateProcess,
    UsernameValidate,
    EmailValidate,
    PasswordValidate
)
from datetime import datetime, timedelta
from application.facades.facades import UserFacade, GroupFacade, UserGroupFacade
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token,
)
from passlib.hash import pbkdf2_sha256 as sha256
import re


class RegistrationService:


    def __init__(self, json):
        self.json      = json
        self.g_facade  = GroupFacade()
        self.u_facade  = UserFacade()
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
            user  = user,
            group = self.g_facade.get_group_by_name(type_group)
        )

        return user_group

    def check_user(self, username, email):

        if self.u_facade.get_user_by_username(username):
            raise ValueError(f"User {username} already exist")

        if self.u_facade.get_user_by_email(email):
            raise ValueError(f"Email {email} already registred")

    def generate_hash(self, password):
        return sha256.hash(password)

    def registrate(self):
        user          = self.create_user()
        user_group    = self.create_user_group(user, "user")
        validate_user = UserValidateProcess()

        validate_user.register(
            UsernameValidate(user.username),
            PasswordValidate(user.password),
            EmailValidate(user.email))

        try:
            validate_user.validate()
            self.check_user(user.username, user.email)
        except ValueError as ex:
            return 400, {"error" : str(ex)}

        user.password = self.generate_hash(user.password)

        try:
            self.u_facade.create(user)
            self.ug_facade.create(user_group)
            a_token, r_token = GenereteJWTService.create_jwt(user)

            return 200, {
                "message"       : f'User {user.username} was registred',
                "access_token"  : a_token,
                "refresh_token" : r_token
            }

        except:
            return 500, {"error": "Internal server error"}

        
class AuthorizationService:


    valid_email_regex = "[^@]+@[^@]+\.[^@]+"

    def __init__(self, json):
        self.json = json
        self.u_facade = UserFacade()

    def get_user(self, param):
        if not re.match(self.valid_email_regex, param):
            return self.get_user_by_username(param)
        else:
            return self.get_user_by_email(param)


    def get_user_by_username(self, username):
        user = self.u_facade.get_user_by_username(username)
        if not user:
            raise ValueError(f"Username {username}  doesn't exist")
        return user

    def get_user_by_email(self, email):
        user = self.u_facade.get_user_by_email(email)
        if not user:
            raise ValueError(f"Email {email} doesn't exist")
        return user

    def verify_password(self, veryfied_pass, hash):
        if not sha256.verify(veryfied_pass, hash):
            raise ValueError("Incorrect password")

    def athorizate(self):
        data = schemas.UserSchema().load(data=self.json)
        try:
            user = self.get_user(data["username"])
            self.verify_password(data['password'], user.password)
            a_token, r_token = GenereteJWTService.create_jwt(user)
            user.last_login = datetime.now()
            self.u_facade.change(user)

            return 200, {
                'message': f'Logged in as {user.username}',
                'username': user.username,
                'access_token': a_token,
                'refresh_token': r_token
            }

        except ValueError as ex:
            return 400, {"error" : "The username or password provided is incorrect."} 
     

class GenereteJWTService:

    def __init__(self, json):
        self.json = json

    def generate_access_token(self):
        expires = timedelta(days=2)
        return create_access_token(identity = self.json, expires_delta=expires)

    def generate_refresh_token(self):
        return create_refresh_token(identity = self.json)

    @staticmethod
    def create_jwt(user: models.User):
        json = {'id' : user.id, 'username' : user.username}
        jwt = GenereteJWTService(json)

        access_token = jwt.generate_access_token()
        refresh_token = jwt.generate_refresh_token()

        return access_token, refresh_token        