import json

from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from application.facades import facades
from application.services.data_chart_service import CalcData
import application.schemas as sch

class DataChart(Resource):

    def post(self):
        json = request.get_json()
        calculated_data = CalcData(json['path'], json['type_id'], json['col1_id'], json['col2_id'])
        return calculated_data.calc()