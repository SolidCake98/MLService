from flask import request
from flask_restful import Resource, reqparse
from application import models
from application.facades.facades import UserFacade, UserGroupFacade, GroupFacade
from application.services import user_services as userv

from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token,
    jwt_refresh_token_required, 
    get_jwt_identity, 
    get_raw_jwt)

from application import schemas



auth_parser = reqparse.RequestParser()
auth_parser.add_argument('username', help = 'This field cannot be blank', required = True)
auth_parser.add_argument('password', help = 'This field cannot be blank', required = True)
#auth_parser.add_argument('email', help = 'This field cannot be blank', required = False)


class UserRegistration(Resource):
    
    def post(self):
        json = request.get_json()
        data = schemas.UserSchema().load(data=json)
        
        new_user = models.User(
            username = data["username"],
            email = data["email"],
            password = models.User.generate_hash(data["password"])
        )

            user_group = models.UserGroup(
                user = new_user,
                group = GroupFacade().get_group_by_name("user")
            )

        user_f = UserFacade()
        user_group_f = UserGroupFacade()

        if user_f.get_user_by_username(data['username']):
            return {'message': 'User {} already exists'. format(data['username'])}

        try:
            user_f.create(new_user)
            user_group_f.create(user_group)

            json = {'id' : new_user.id, 'username' : new_user.username}
            access_token = create_access_token(identity = json )
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message': f'User {data['username']} was created',
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        except:
            return {'message': 'Something went wrong'}, 500

        return data

class UserAuthorization(Resource):

    def post(self):

        data = auth.parse_args()
        facade = UserFacade(data['username'])

        current_user = facade.get_user_by_username(data['username'])

        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}
        
        if models.User.verify_hash(data['password'], current_user.password):
            json = {'id' : current_user.id, 'username' : current_user.username}
            access_token = create_access_token(identity = json)
            refresh_token = create_refresh_token(identity = json)

            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token}


        else:
            return {'message': 'Wrong credentials'}

class TokenRefresh(Resource):

    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = userv.GenereteJWTService(current_user).generate_access_token()
        return {'access_token': access_token}