import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    
    user = os.environ["POSTGRES_USER"]
    password = os.environ["POSTGRES_PASSWORD"]
    hostname = os.environ["POSTGRES_HOSTNAME"]
    port = os.environ["POSTGRES_PORT"]
    database = os.environ["APPLICATION_DB"]

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{user}:{password}@{hostname}:{port}/{database}"
    )

    JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
    
    DATASETS_PATH = os.environ["DATASETS_PATH"]
    MEDIA_PATH = os.environ["MEDIA_PATH"]


    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    pass

class ProductionConfig(Config):
    pass

class TestingConfig(Config):
    TESTING = True