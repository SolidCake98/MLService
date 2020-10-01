from application.services.dataset_services import DataSetUploadService, DataSetDownloadService
from flask_restful import Resource
from flask import request
from application import models
from application import schemas as sc
from flask_jwt_extended import jwt_required, get_jwt_identity

class DataSetDownloadController(Resource):

    def get(self, filename):
        d_service = DataSetDownloadService()
        return d_service.download(filename)

class DataSetUploadController(Resource):

    @jwt_required
    def post(self):
        json = request.form 
        current_user = get_jwt_identity()
        data_set = request.files['dataset']
        d_service = DataSetUploadService(json, current_user['username'], data_set)

        return d_service.upload(current_user['username'], data_set)
