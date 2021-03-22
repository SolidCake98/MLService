from flask import request
from flask_restful import Resource, reqparse
from application import models
from application.facades.facades import UserFacade, UserGroupFacade, GroupFacade
from application.services import user_services as userv
from application import schemas as sc


from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity, 
    jwt_required
)

from application import schemas


class UserRegistration(Resource):
    
    def post(self):
        json = request.get_json()
        user_register_context = userv.ContextReg(userv.RegistrationService(json))
        code, message = user_register_context.registrate()
        return message, code


class UserAuthorization(Resource):

    def post(self):
        json = request.get_json()
        user_authorization_context = userv.ContextAuth(userv.AuthorizationService(json))
        code, message = user_authorization_context.authorizate()
        return message, code
        
       
class TokenRefresh(Resource):

    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        access_token = userv.GenereteJWTService(current_user).generate_access_token()
        return {'access_token': access_token}


class UserController(Resource):

    def get(self, user_id): 
        u_facade = UserFacade()
        user = u_facade.get_entity(user_id)
        if not user:
            return {"error": "User doesn't exist"}, 400
        user_schema = sc.UserSchema(only=("id", "username"))
        return user_schema.dump(user)


class UserProfileController(Resource):

    def get(self, user_id):
        profile = userv.UserInfoService(user_id).get_user_profile()
        return profile


class UserProfileListController(Resource):

    def get(self):
        profiles = userv.UserInfoService.get_all_user_profiles()
        return profiles


class UserGroupExcludedController(Resource):

    def get(self, user_id):
        groups = userv.UserInfoService.get_excluded_groups(user_id)
        return groups


class UserListController(Resource):

    def get(self):
        u_facade = UserFacade()
        users = u_facade.get_all()
        user_schema = sc.UserSchema(many=True, only=("id", "username", "date_joined"))
        return user_schema.dump(users)


class UserGroupAddController(Resource):

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        json = request.get_json()
        res, code = userv.UserInfoService.add_user_to_group(
            current_user['username'], 
            json['username'], 
            json['groupname'])
        return res, code
