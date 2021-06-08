from flask import Flask
from flask_restful import Api

from application.database import db_session

import application.api.user_controller as user_c
import application.api.dataset_controller as data_c
import application.api.dataset_table_controller as data_table_c
import application.api.media_controller as media_c
import application.api.dataset_chart_controller as data_chart_c


from flask_jwt_extended import JWTManager


def create_app(config_name):
    
    app = Flask(__name__)

    config_module = f"application.config.{config_name.capitalize()}Config"
    app.config.from_object(config_module)


    api = Api(app)
    JWTManager(app)

    api.add_resource(user_c.UserRegistration, '/api/v1/jwt/register', endpoint="reg")
    api.add_resource(user_c.UserAuthorization, '/api/v1/jwt/auth', endpoint="auth")
    api.add_resource(user_c.TokenRefresh, '/api/v1/jwt/refresh', endpoint="refresh")

    api.add_resource(user_c.UserListController, '/api/v1/user')
    api.add_resource(user_c.UserController, '/api/v1/user/<user_id>')
    api.add_resource(user_c.UserProfileController,'/api/v1/user/profile/<user_id>')
    api.add_resource(user_c.UserProfileListController,'/api/v1/user/profile')
    api.add_resource(user_c.UserGroupExcludedController, '/api/v1/user/groups/excluded/<user_id>')
    api.add_resource(user_c.UserGroupAddController, "/api/v1/user/group")

    api.add_resource(media_c.UserDefaultAvatar, '/api/v1/user/media/default')

    api.add_resource(data_c.DataSetDownloadController, '/api/v1/dataset/download/<user>/<data>')
    api.add_resource(data_c.DataSetUploadController, '/api/v1/dataset/upload')

    api.add_resource(data_c.DataSetListController, '/api/v1/dataset')
    api.add_resource(data_c.DataSetListNewController, '/api/v1/dataset/new')
    api.add_resource(data_c.DataSetListPopularController, '/api/v1/dataset/popular')
    api.add_resource(data_c.DataSetListUserController, '/api/v1/dataset/owner')
    api.add_resource(data_c.DataSetListWordTitleController, '/api/v1/dataset/search')
    api.add_resource(data_c.DataSetListTagController, '/api/v1/dataset/search/tag')
    api.add_resource(data_c.DataSetUserRatingController, '/api/v1/dataset/rating')

    api.add_resource(data_c.TagListWordNameController, '/api/v1/dataset/tag')

    api.add_resource(data_c.DataSetController, '/api/v1/dataset/<user>/<data>')
    api.add_resource(data_c.DataSetDirReadController, '/api/v1/dataset/dir')
    api.add_resource(data_c.DataSetFileReadController, '/api/v1/dataset/file')
    api.add_resource(media_c.DataSetImageController, '/api/v1/dataset/img/<path:path>')
    api.add_resource(data_c.DataSetAddTags, '/api/v1/dataset/add_tags')

    api.add_resource(data_table_c.DataSetTableCreateController, '/api/v1/dataset_table')
    api.add_resource(data_table_c.DataSetTableListController, '/api/v1/dataset_table/list/<int:data_id>')
    api.add_resource(data_table_c.DataSetTableController, '/api/v1/dataset_table/<int:table_id>')
    api.add_resource(data_table_c.DataTypeAggregationController, '/api/v1/dataset_table/types')

    api.add_resource(data_chart_c.DataChartController, '/api/v1/dataset_chart/calculate')
    api.add_resource(data_chart_c.ChartTypeController, '/api/v1/dataset_chart/type')

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app
