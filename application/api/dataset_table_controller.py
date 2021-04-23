import json

from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from application.facades import facades
from application.services.dataset_table_service import DataSetTableService


class DataSetTableController(Resource):

    @jwt_required()
    def post(self):
        json = request.get_json()

        data_table = DataSetTableService(json)
        data_table.create_dataset_table()

        return {'result': 'success'}