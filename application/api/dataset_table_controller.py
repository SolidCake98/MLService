import json

from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from application.facades import facades
from application.services.dataset_table_service import DataSetTableService
import application.schemas as sch


class DataSetTableCreateController(Resource):

    @jwt_required()
    def post(self):
        json = request.get_json()

        data_table = DataSetTableService(json)
        data_table.create_dataset_table()

        return {'result': 'success'}


class DataSetTableListController(Resource):

    def get(self, data_id):
        table_facade = facades.DataSetTableFacade()
        tables = table_facade.get_all_tables_by_data_id(data_id)
        result = sch.DataTableSchema(many=True).dump(tables)
        return result



class DataSetTableController(Resource):

    def get(self, table_id):
        v_col_facade = facades.DataSetColumnVersionedFacade()
        table_facade = facades.DataSetTableFacade()

        table = table_facade.get_entity(table_id)
        cols = v_col_facade.get_all_columns_of_data_table(table_id)
        

        result = {
            "cols"  : sch.DataTableColumnVersionedSchema(many=True).dump(cols),
            "table" : sch.DataTableSchema().dump(table)
        }
        
        return result


class DataTypeAggregationController(Resource):

    def get(self):
        data_type_facade = facades.DataTypeFacade()
        data_types = data_type_facade.get_all()
        aggregations = { x.name: [y.aggregation.name for y in x.data_type_ags] for x in data_types}
        return aggregations
