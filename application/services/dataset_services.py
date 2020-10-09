import os
from abc import ABC, abstractmethod
from application.config import Config, BASE_DIR
from application.facades import facades
from application.services.validate_service import FilenameValidate
from application.services.dataset import upload_files as up
from application.services.dataset import create_records as cr

from flask import Response
from application import models, schemas
from werkzeug.utils import secure_filename
import zipfile
import zipstream
import shutil
import json
from threading import Thread

dataset_directory = os.path.join(os.path.abspath(os.path.join(BASE_DIR, os.pardir)), Config.DATASETS_PATH)


# class ReadFromFileInZip:

#     def __init__(self, path, name):
#         self.path = path
#         self.name = nimportame

#     def read(self):
#         zip_file = zipfile.ZipFile(self.path, 'r')
#         with zip_file.open(self.name) as f:
#             for i, line in enumerate(f):
#                 pass


class DataSetDownloadService:

    """
    Service for downloading of datasets
    """

    def download(self, path):
        
        z = zipstream.ZipFile(mode='w', compression=zipstream.ZIP_DEFLATED)
        path = os.path.join(dataset_directory, path)

        for root, dirs, files in os.walk(path):
            for file in files:
                absname = os.path.abspath(os.path.join(root, file))
                arcname = absname[len(path) + 1:]
                z.write(absname, arcname=arcname)

        response = Response(z, mimetype='application/zip')
        response.headers['Content-Disposition'] = 'attachment; filename={}'.format('archive.zip')
        return response


#TODO add tags and do refactor
class DataSetUploadService:

    """
    Service for uploading of datasets
    """

    types = [
        'csv',
        'json'
    ]

    def __init__(self, j_data, user, file):

        self.data = schemas.DataSetSchema().load(data=j_data)
        self.user = user
        self.file = file


    #TODO нормальный поиск типов файла
    def find_types_and_size(self, dir):
        types = set()
        total_size = 0

        for dirpath, dirnames, filenames in os.walk(dir):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)

                extesion = f.rsplit('.', 1)[1].lower()
                if extesion not in self.types:
                    types.add('other')
                else:
                    types.add(extesion)

        return types, total_size//1024

    
    def __check_error_dataset(self, name):
        if facades.DataSetFacade().get_dataset_by_name(name):
            raise ValueError('Data set with this name was already upload')

        
    def get_file_by_ext(self, ext, upload_dir):
        if ext == 'zip':
            up_nz: up.UploadFile = up.UploadZipArchive(upload_dir, self.file)
        else:
            up_nz: up.UploadFile = up.UploadOther(upload_dir, self.file)

        return up_nz

    def upload(self):

        def extract(zi:up.Extractor):
            zi.extract()

        def write_dataset(upload_dir:str, name:str):
            types, size = self.find_types_and_size(upload_dir)
            d_creator = cr.DataSetCreator(self.data, self.user, size)
            dataset = d_creator.create()

            d_type = cr.DataSetTypeCreator(types, dataset)
            d_type.create()

            d_tag = cr.DataSetTagCreator(dataset, self.data)
            d_tag.create()


        try:
            f_validate = FilenameValidate(self.file.filename)
            f_validate.validate()
            self.__check_error_dataset(self.data['name'])

            upload_dir = os.path.join(dataset_directory, self.user['username'], self.data['name'])

            extension = self.file.filename.rsplit('.', 1)[1].lower()
            up_nz = self.get_file_by_ext(extension, upload_dir)
            up_nz.upload()

            if extension == 'zip':
                thread1 = Thread(target=extract, kwargs={'zi': up_nz})
                thread1.start()

            thread2 = Thread(target=write_dataset, kwargs={'upload_dir': upload_dir, 'name': self.data['name']})
            thread2.start()

            return {'message': 'file saved'}, 200

        except ValueError as err:
            return {"error": str(err)}, 400

        # except Exception as err:
        #     return {"error": "Can't upload dataset"}, 400