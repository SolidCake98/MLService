from flask import Flask
from flask_restful import Api
from application.database import db_session
from application.api.user_controller import (
    UserAuthorization, 
    UserRegistration, 
    TokenRefresh, 
    UserController, 
    UserListController
)
from application.api.dataset_controller import (
    DataSetDownloadController, 
    DataSetUploadController, 
    DataSetListController, 
    DataSetController,
    DataSetDirReadController
)
from flask_jwt_extended import JWTManager

def create_app(config_name):

    app = Flask(__name__)
    
    config_module = f"application.config.{config_name.capitalize()}Config"
    app.config.from_object(config_module)

    api = Api(app)
    jwt = JWTManager(app)

    api.add_resource(UserRegistration, '/api/v1/jwt/register')
    api.add_resource(UserAuthorization, '/api/v1/jwt/auth')
    api.add_resource(TokenRefresh, '/api/v1/jwt/refresh')

    api.add_resource(UserListController, '/api/v1/user')
    api.add_resource(UserController, '/api/v1/user/<user_id>')

    api.add_resource(DataSetDownloadController, '/api/v1/dataset/download/<user>/<data>')
    api.add_resource(DataSetUploadController, '/api/v1/dataset/upload')
    api.add_resource(DataSetListController, '/api/v1/dataset')
    api.add_resource(DataSetController, '/api/v1/dataset/<user>/<data>')
    api.add_resource(DataSetDirReadController, '/api/v1/dataset/dir')


    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app

