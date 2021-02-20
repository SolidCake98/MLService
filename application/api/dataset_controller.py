from application.services.dataset_services import (
    DataSetUploadService, 
    DataSetDownloadService, 
    DataSetPathStructure, 
    DataSetReadFile
)
from application.services.dataset.file_reader import ReaderCreator
from application.facades import facades
from flask_restful import Resource
from flask import request
from application import models
from application import schemas as sc
from flask_jwt_extended import jwt_required, get_jwt_identity
import json

class DataSetDownloadController(Resource):

    def get(self, user, data):
        d_service = DataSetDownloadService()
        code, result = d_service.download( user + "/" + data)
        return reuslt, code


class DataSetAddTags(Resource):
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        json = request.get_json()

        d = facades.DataSetTagFacade()
        d.add_tags(json['id'], json['tags'])
        return {'result': 'success'}

class DataSetUploadController(Resource):

    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        data_set = request.files['dataset']
        j_data = json.load(request.files['document'])

        d_service = DataSetUploadService(j_data, current_user, data_set)
        code, result = d_service.upload()
        return result, code

class DataSetListController(Resource):

    def get(self): 
        datasets = facades.DataSetFacade().get_all()
        dataset_schema = sc.DataSetSchema(many=True)
        return dataset_schema.dump(datasets)

class DataSetListPopularController(Resource):

    def get(self): 
        datasets = facades.DataSetFacade().get_dataset_ordered_by_last_month()
        dataset_schema = sc.DataSetSchema(many=True)
        return dataset_schema.dump(datasets)

class DataSetListNewController(Resource):

    def get(self): 
        datasets = facades.DataSetFacade().get_dataset_ordered_by_data()
        dataset_schema = sc.DataSetSchema(many=True)
        return dataset_schema.dump(datasets)

class DataSetListWordTitleController(Resource):

    def post(self):
        json = request.get_json()
        datasets = facades.DataSetFacade().get_with_similarity_title(json['word'])
        dataset_schema = sc.DataSetSchema(many=True)
        return dataset_schema.dump(datasets)

class DataSetListTagController(Resource):

    def post(self):
        json = request.get_json()
        datasets = facades.DataSetFacade().get_dataset_by_tags(json['tags'])
        dataset_schema = sc.DataSetSchema(many=True)
        return dataset_schema.dump(datasets)

class TagListWordNameController(Resource):

    def post(self):
        json = request.get_json()
        tags = facades.TagFacade().get_with_similarity_tag(json['word'])
        tag_schema = sc.TagSchema(many=True)
        return tag_schema.dump(tags)

class DataSetDirReadController(Resource):

    def post(self):
        json = request.get_json()
        d_r_service = DataSetPathStructure(json)
        code, result = d_r_service.read()
        return result, code

class DataSetFileReadController(Resource):

    def post(self):
        json = request.get_json()

        reader = ReaderCreator().create(json['path'])
        d_rf_service = DataSetReadFile(json, reader)
        return d_rf_service.read()


class DataSetController(Resource):

    def get(self, user, data): 
        d_facade = facades.DataSetFacade()
        dataset = d_facade.get_dataset_by_user_and_data(user, data)
        dataset_schema = sc.DataSetSchema()
        return dataset_schema.dump(dataset)

class DataSetListUserController(Resource):

    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        facades.DataSetFacade().get_with_similarity_title("test");
        user = facades.UserFacade().get_entity(current_user['id'])
        return sc.DataSetSchema(many=True).dump(user.datasets)

class DataSetUserRatingController(Resource):

    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        json = request.get_json()
        user_rating = models.UserRating(dataset_id=json['id'], \
            rating=json['rating'], commenatary=json['commentary'],
            user_id=current_user['id'])
        facades.UserRatingFacade().create(user_rating)
        return {'result': 'success'}, 200
