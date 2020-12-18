from flask_restful import Resource
from flask import send_from_directory
from application.services.dataset_services import DataSetImage
from application.config import Config
import os

#TODO change next
class UserDefaultAvatar(Resource):
    
    def get(self):
        return send_from_directory(os.path.join(Config.MEDIA_ABS_PATH, "default/avatar/"), "default.jpg")

class DataSetImageController(Resource):

    def get(self, path):
        d_img = DataSetImage(path)  
        return d_img.send_image()
        