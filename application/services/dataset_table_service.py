import os
from application.config import Config
from dask import dataframe as dd
from application.services.create_records import DataSetTableCreator, DataSetColumnCreator

class DataSetTableService:

    def __init__(self, json):
        
        self.json = json
        self.path = os.path.join(Config.DATASETS_ABS_PATH, json['path'])

    def create_dataset_table(self):
        dataset_id = self.json['d_id']
        name = self.json['name']
        data_frame = dd.read_csv(self.path)

        dt_creator = DataSetTableCreator(dataset_id, self.json['path'], name)
        d_table = dt_creator.create()

        cols = data_frame.columns
        types = data_frame.dtypes

        d_columns_creator = DataSetColumnCreator(self.json['path'], d_table.id, cols, types)
        d_columns_creator.create()
        