from flask import Flask
from flask_restful import Api
from application.database import db_session
from application.api.user_controller import (
    UserAuthorization, 
    UserRegistration, 
    TokenRefresh, 
    UserController, 
    UserListController,
    UserProfileController,
    UserProfileListController, 
    UserGroupExcludedController,
    UserGroupAddController,
)
from application.api.dataset_controller import (
    DataSetDownloadController, 
    DataSetUploadController, 
    DataSetListController, 
    DataSetController,
    DataSetDirReadController,
    DataSetFileReadController,
    DataSetAddTags,
    DataSetListNewController,
    DataSetListPopularController,
    DataSetListUserController,
    DataSetListWordTitleController,
    TagListWordNameController,
    DataSetListTagController
)

from application.api.media_controller import DataSetImageController, UserDefaultAvatar
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
    api.add_resource(UserProfileController,'/api/v1/user/profile/<user_id>')
    api.add_resource(UserProfileListController,'/api/v1/user/profile')
    api.add_resource(UserGroupExcludedController, '/api/v1/user/groups/excluded/<user_id>')
    api.add_resource(UserGroupAddController, "/api/v1/user/group")

    api.add_resource(UserDefaultAvatar, '/api/v1/user/media/default')

    api.add_resource(DataSetDownloadController, '/api/v1/dataset/download/<user>/<data>')
    api.add_resource(DataSetUploadController, '/api/v1/dataset/upload')

    api.add_resource(DataSetListController, '/api/v1/dataset')
    api.add_resource(DataSetListNewController, '/api/v1/dataset/new')
    api.add_resource(DataSetListPopularController, '/api/v1/dataset/popular')
    api.add_resource(DataSetListUserController, '/api/v1/dataset/owner')
    api.add_resource(DataSetListWordTitleController, '/api/v1/dataset/search')
    api.add_resource(DataSetListTagController, '/api/v1/dataset/search/tag')

    api.add_resource(TagListWordNameController, '/api/v1/dataset/tag')

    api.add_resource(DataSetController, '/api/v1/dataset/<user>/<data>')
    api.add_resource(DataSetDirReadController, '/api/v1/dataset/dir')
    api.add_resource(DataSetFileReadController, '/api/v1/dataset/file')
    api.add_resource(DataSetImageController, '/api/v1/dataset/img/<path:path>')
    api.add_resource(DataSetAddTags, '/api/v1/dataset/add_tags/<name>')


    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app