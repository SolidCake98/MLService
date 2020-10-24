from application.services.dataset_services import DataSetUploadService, DataSetDownloadService, DataSetPathStructure
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
        return d_service.download( user + "/" + data)

class DataSetUploadController(Resource):

    @jwt_required
    def post(self):
        current_user = get_jwt_identity()

        data_set = request.files['dataset']
        j_data = json.load(request.files['document'])

        d_service = DataSetUploadService(j_data, current_user, data_set)

        return d_service.upload()

class DataSetListController(Resource):

    def get(self): 
        d_facade = facades.DataSetFacade()
        datasets = d_facade.get_all()
        dataset_schema = sc.DataSetSchema(many=True)
        return dataset_schema.dump(datasets)

class DataSetDirReadController(Resource):

    def post(self):
        json = request.get_json()
        d_r_service = DataSetPathStructure(json)
        return d_r_service.read()

class DataSetController(Resource):

    def get(self, user, data): 
        d_facade = facades.DataSetFacade()
        dataset = d_facade.get_dataset_by_user_and_data(user, data)
        dataset_schema = sc.DataSetSchema()
        return dataset_schema.dump(dataset)