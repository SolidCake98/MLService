from application import schemas, models
from application.services.validate_service import (
    UserValidateProcess,
    UsernameValidate,
    EmailValidate,
    PasswordValidate,
    UserRegisterValidate
)
from datetime import datetime, timedelta
from application.facades.facades import UserFacade, GroupFacade, UserGroupFacade, CountDatasetFacade
from application.services.create_records import Creator, UserCreator
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token,
)
from passlib.hash import pbkdf2_sha256 as sha256
import re
from abc import ABC, abstractmethod
import socket


class RegistrationStrategy(ABC):
    @abstractmethod
    def registrate(self):
        pass

class AuthorizationStrategy(ABC):
    @abstractmethod
    def authorizate(self):
        pass

class ContextReg:
    
    def __init__(self, strategy):
        self.strategy = strategy

    def registrate(self):
        return self.strategy.registrate()

class ContextAuth:
    def __init__(self, strategy):
        self.strategy = strategy

    def authorizate(self):
        return self.strategy.authorizate()

class RegistrationService(RegistrationStrategy):

    def __init__(self, json):
        self.json      = json
        self.g_facade  = GroupFacade()
        self.u_facade  = UserFacade()
        self.ug_facade = UserGroupFacade()

    def registrate(self):
        data = schemas.UserSchema().load(data=self.json)
        validate_user = UserValidateProcess()
        validate_user.register(
            UsernameValidate(data['username']),
            PasswordValidate(data['password']),
            EmailValidate(data['email']),
            UserRegisterValidate(self.u_facade, data['username'], data['email'])
        )

        try:
            validate_user.validate()
        except ValueError as ex:
            return 400, {"error" : str(ex)}
        
        try:
            user = UserCreator(self.g_facade, self.ug_facade,self.u_facade, data).create()
            a_token, r_token = GenereteJWTService.create_jwt(user)
    
            return 200, {
                "message"       : f'User {user.username} was registred',
                "access_token"  : a_token,
                "refresh_token" : r_token
            }
        except:
            return 500, {"error": "Internal server error"}

       
class AuthorizationService(AuthorizationStrategy):

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

    def authorizate(self):
        data = schemas.UserSchema().load(data=self.json)
        try:
            user = self.get_user(data["username"])
            self.verify_password(data['password'], user.password)
            a_token, r_token = GenereteJWTService.create_jwt(user)
            user.last_login = datetime.now()
            self.u_facade.change(user)

            return 200, {
                'message': f'Logged in as {user.username}',
                'id': user.id,
                'username': user.username,
                'roles': [x.group.name for x in user.groups],   
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

class UserInfoService:
    local_ip = socket.gethostbyname(socket.gethostname())

    uri_to_default_avatar = f'http://localhost:5000/api/v1/user/media/default'

    def __init__(self, id):
        self.user = UserFacade().get_entity(id)

    def get_user_stats(self):
        stats = CountDatasetFacade().get_entity(self.user.id)
        dump = schemas.CountDataSetSchema().dump(stats)
        return dump

    def get_user_dataset(self):
        datasets = schemas.DataSetSchema(many=True).dump(self.user.datasets)
        return datasets

    def get_user_profile(self):
        return {
            'stats': self.get_user_stats(),
            'datasets': self.get_user_dataset(),
            'user': schemas.UserSchema(exclude=["password"]).dump(self.user),
            'avatar': self.uri_to_default_avatar,
            'groups': schemas.UserGroupsSchema(many=True).dump(self.user.groups)
        }

    @classmethod
    def get_excluded_groups(self, u_id):
        groups = GroupFacade().get_excluded_groups(u_id)
        return schemas.GroupSchema(many=True).dump(groups)

    @classmethod
    def get_all_user_profiles(self):
        users = UserFacade().get_all()
        result = [
            {'user' : schemas.UserSchema(exclude=["password"]).dump(u),
            'stats' : schemas.CountDataSetSchema().dump(CountDatasetFacade().get_entity(u.id)),
            'groups': schemas.UserGroupsSchema(many=True).dump(u.groups)
            } for u in users
        ]
        return result

    @classmethod
    def add_user_to_group(self, admin, username, groupname):
        # try:
        UserGroupFacade().add_user_to_group(admin, username, groupname)
        return {'message': 'success'}, 200
        # except Exception as ex:
        #     return {'error' : str(ex)}, 500