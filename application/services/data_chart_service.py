from dask import dataframe as dd
from application.config import Config
import os
import application.facades.facades as fc
from sklearn.decomposition import KernelPCA
from sklearn.manifold import TSNE
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd

class CalcData:

    def __init__(self, path, type_id, col1_id = None, col2_id = None):
        self.path = path
        self.abs_path = os.path.join(Config.DATASETS_ABS_PATH, self.path)
        self.df: dd.DataFrame = dd.read_csv(self.abs_path)
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

    def calc_pca(self, df):

        df = df.compute()
        df = df.dropna(axis=0)

        for col in df.columns:
            try:
                if df[col].dtype == "string":
                    df[col] = pd.factorize(df[col])[0]
            except TypeError:
                if df[col].dtype == "object":
                    df[col] = pd.factorize(df[col])[0]
        
        scaler = StandardScaler()

        # y = df['output'] 

        scaler.fit(df)
        df = scaler.transform(df)
        pca = KernelPCA(n_components=2, kernel='rbf', max_iter=100)

        df = pca.fit_transform(df)
        df = df.T

        pdf = pd.DataFrame()
        pdf["x"] = df[0]
        pdf["y"] = df[1]

        return pdf

    def calc_lda(self, df, col_y):

        df = df.compute()
        df = df.dropna(axis=0)

        for col in df.columns:
            try:
                if df[col].dtype == "string":
                    df[col] = pd.factorize(df[col])[0]
            except TypeError:
                if df[col].dtype == "object":
                    df[col] = pd.factorize(df[col])[0]
        
        scaler = StandardScaler()

        y = df[col_y] 
        df = df.drop(columns= [col_y])

        scaler.fit(df)
        df = scaler.transform(df)

        lda = LinearDiscriminantAnalysis()

        df = lda.fit_transform(df, y)
        df = df.T

        pdf = pd.DataFrame()
        pdf["x"] = df[0]
        
        try:
            pdf["y"] = df[1]
        except Exception:
            pdf["y"] = df[0]

        return pdf


    def calc(self):

        df: dd.DataFrame = self.df.persist()
        fraction = 1000 / len(df)
        
        if fraction > 1:
            df = df.sample(frac = 1, random_state=10)
        else:
            df = df.sample(frac = fraction, random_state=10)


        chart_type = self.get_chart_type()

        if chart_type.id != 5 and chart_type.id != 6:

            col_x = self.get_col(self.col1)
            col_y = self.get_col(self.col2)

            x_name = col_x.dataset_column_sources.tittle
            y_name = col_y.dataset_column_sources.tittle
            
            df[x_name] = df[x_name].astype(self.types[col_x.data_type_aggregation.data_type.name])
            df[y_name] = df[y_name].astype(self.types[col_y.data_type_aggregation.data_type.name])

            
            if chart_type.id != 2 or col_y.data_type_aggregation.aggregation.name != "none":
                aggregation = col_y.data_type_aggregation.aggregation.name
                
                if aggregation == "none":
                    aggregation = self.default_agg[col_y.data_type_aggregation.data_type.name]

                
                result = self.aggregations[aggregation](df.groupby(x_name)[y_name]).compute()

                pdf = pd.DataFrame()
                
                pdf["x"] = result.keys()
                pdf["y"] = list(result)

            
            if chart_type.id == 2:
                df = df[(df[x_name].notnull()) & (df[y_name].notnull())]
                d = {
                    "x": df[x_name].compute(),
                    "y": df[y_name].compute()
                }
                pdf = pd.DataFrame(d)

                aggregation = col_y.data_type_aggregation.aggregation.name

        elif chart_type.id == 5:
            x_name = "PCA 1"
            y_name = "PCA 2"
            pdf = self.calc_pca(df)
            aggregation = "none"

        elif chart_type.id == 6:

            col_x = self.get_col(self.col1)
            classes = col_x.dataset_column_sources.tittle

            x_name = "LDA 1"
            y_name = "LDA 2"
            pdf = self.calc_lda(df, classes)
            aggregation = "none"
        

        pdf["xlabel"] = pd.factorize(pdf["x"])[0]
        pdf["ylabel"] = pd.factorize(pdf["y"])[0]

        try:
            categorical_x = pdf.dtypes["x"] == "object" or pdf.dtypes["x"] == "string"
        except TypeError:
            categorical_x = False
        
        try:
            categorical_y = pdf.dtypes["y"] == "object" or pdf.dtypes["y"] == "string"
        except TypeError:
            categorical_y = False

        
        return {
            "type" : chart_type.name,
            "agg" : aggregation,
            "x" : { 
                    "data"  : list(pdf["xlabel"]),
                    "label" : list(pdf["x"]),
                    "max"   : int(pdf["xlabel"].max()) if categorical_x else int(pdf["x"].max()),
                    "min"   : int(pdf["xlabel"].min()) if categorical_x else int(pdf["x"].min()),
                    "field" : x_name,
                    "categorical" : categorical_x
                },
            "y" : { 
                "data"  :list(pdf["ylabel"]),
                "label" : list(pdf["y"]),
                "field" : y_name,
                "categorical" : categorical_y
            }
        }
