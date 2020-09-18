from flask import Flask
from flask_restful import Api
from application.database import db_session
from application.api.file_controller import FileApi
from application.api.user_controller import UserAuthorization, UserRegistration
from flask_jwt_extended import JWTManager

def create_app(config_name):

    app = Flask(__name__)
    
    config_module = f"application.config.{config_name.capitalize()}Config"
    app.config.from_object(config_module)

    api = Api(app)
    jwt = JWTManager(app)

    api.add_resource(FileApi, '/')
    api.add_resource(UserRegistration, '/reg')
    api.add_resource(UserAuthorization, '/login')

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app

