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
from application.api.dataset_controller import DataSetDownloadController, DataSetUploadController, DataSetListController
from flask_jwt_extended import JWTManager

def create_app(config_name):

    app = Flask(__name__)
    
    config_module = f"application.config.{config_name.capitalize()}Config"
    app.config.from_object(config_module)

    app = Api(app)
    jwt = JWTManager(app)

    app.add_resource(UserRegistration, '/api/v1/jwt/register')
    app.add_resource(UserAuthorization, '/api/v1/jwt/auth')
    app.add_resource(TokenRefresh, '/api/v1/jwt/refresh')
    app.add_resource(UserListController, '/api/v1/user')
    app.add_resource(UserController, '/api/v1/user/<user_id>')
    app.add_resource(DataSetDownloadController, '/api/v1/dataset/download/<filename>')
    app.add_resource(DataSetUploadController, '/api/v1/dataset/upload')
    app.add_resource(DataSetListController, '/api/v1/dataset')


    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app

