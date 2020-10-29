from flask_restful import Resource
from application.services.dataset_services import DataSetImage

class UserAvatar(Resource):
    pass

class DataSetImageController(Resource):

    def get(self, path):
        d_img = DataSetImage(path)
        return d_img.send_image()
        