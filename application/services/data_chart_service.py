from dask import dataframe as dd
from application.config import Config
import os
import application.facades.facades as fc
import pandas as pd

class CalcData:

    def __init__(self, path, type_id, col1_id = None, col2_id = None):
        self.path = path
        self.abs_path = os.path.join(Config.DATASETS_ABS_PATH, self.path)
        self.df = dd.read_csv(self.abs_path)
        self.chart_type = type_id

        self.col1 = col1_id
        self.col2 = col2_id

        self.types = {
            'integer': 'int64',
            'string': 'string',
            'float': 'float64'
        }

        self.default_agg = {
            'string': 'count',
            'integer': 'sum',
            'float': 'sum'
        }

        self.aggregations = {
            'count': lambda x: x.count(),
            'countunique': lambda x: x.nunique(),
            'sum': lambda x: x.sum(),
            'avg': lambda x: x.mean(),
            'min': lambda x: x.min(),
            'max': lambda x: x.max(),
        }

    def get_chart_type(self):
        return fc.ChartTypeFacade().get_entity(self.chart_type)

    def get_col(self, col_id):
        return fc.DataSetColumnVersionedFacade().get_entity(col_id)

    def calc(self):
        chart_type = self.get_chart_type()

        col_x = self.get_col(self.col1)
        col_y = self.get_col(self.col2)


        x_name = col_x.dataset_column_sources.tittle
        y_name = col_y.dataset_column_sources.tittle

        df = self.df.persist()
        df = df.loc[:1000]


        df[x_name] = df[x_name].astype(self.types[col_x.data_type_aggregation.data_type.name])
        df[y_name] = df[y_name].astype(self.types[col_y.data_type_aggregation.data_type.name])

        if chart_type.name != "scatter plot":
            aggregation = col_y.data_type_aggregation.aggregation.name
            
            if aggregation == "none":
                aggregation = self.default_agg[col_y.data_type_aggregation.data_type.name]

            result = self.aggregations[aggregation](df.groupby(x_name)[y_name]).compute()

            return {
                "type" : chart_type.name,
                "agg" : aggregation,
                "x" : { 
                    "data" :list(result.keys()),
                    "field" : x_name
                },
                "y" : { 
                    "data" :list(result),
                    "field" : y_name
                }
            }

        # x = df[x_name].compute()
        # y = df[y_name].compute()

        # pf = x.to_frame()
        # pf[y_name] = y    
        # pf = pf.sort_values(x_name)

        return {
            "type" : chart_type.name,
            "agg" : "none",
            "x" : { 
                    "data" :list(df[x_name].compute()),
                    "field" : x_name
                },
            "y" : { 
                "data" :list(df[y_name].compute()),
                "field" : y_name
            }
        }
