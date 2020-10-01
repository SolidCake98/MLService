import os
from abc import ABC, abstractmethod
from application.config import Config, BASE_DIR
from application.services.validate_service import FilenameValidate
from flask import Response
from application import models, schemas
from werkzeug.utils import secure_filename
import zipfile
import zipstream
import shutil


dataset_directory = os.path.join(os.path.abspath(os.path.join(BASE_DIR, os.pardir)), Config.DATASETS_PATH)


class UploadFile(ABC):
    
    name = 'archive.zip'

    @abstractmethod
    def upload():
        pass

    @abstractmethod
    def add():
        pass

    def clear_path(self, path):
        try:
            os.makedirs(path, exist_ok=False)
        except:
            for file_object in os.listdir(path):
                file_object_path = os.path.join(path, file_object)
                if os.path.isfile(file_object_path):
                    os.unlink(file_object_path)
                else:
                    shutil.rmtree(file_object_path)

class UploadZipArchive(UploadFile):

    def __init__(self, path, file):
        self.path = path
        self.file = file

    def upload(self):
        self.clear_path(self.path)
        file_path = os.path.join(self.path, self.name)
        self.file.save(file_path)

        zip_file = zipfile.ZipFile(file_path)
        zip_file.extractall(self.path)
        zip_file.close()
        os.remove(file_path)


    def add(self):
        zip_file = zipfile.ZipFile(self.file)
        zip_file.extractall(self.path)
        zip_file.close()    



class ReadFromFileInZip:

    def __init__(self, path, name):
        self.path = path
        self.name = nimportame

    def read(self):
        zip_file = zipfile.ZipFile(self.path, 'r')
        with zip_file.open(self.name) as f:
            for i, line in enumerate(f):
                pass



class UploadOther(UploadFile):

    def __init__(self, path, file):
        self.path = path
        self.file = file

    def upload(self):
        self.clear_path(self.path)
        file_dir = os.path.join(self.path, self.file.filename)
        self.file.save(file_dir)

    def add(self):
        file_dir = os.path.join(self.path, self.file.filename)
        self.file.save(file_dir)

class DataSetDownloadService:

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

class DataSetUploadService:

    def __init__(self, json, username, file):
        self.json = json
        self.username = username
        self.file = file
    

    def create_dataset_info(self):
        data = schemas.DataSetSchema(self.json)


    def upload(self):
        f_validate = FilenameValidate(self.file.filename)

        try:
            f_validate.validate()
            extension = self.file.filename.rsplit('.', 1)[1].lower()
            upload_dir = os.path.join(dataset_directory, self.username)

            if extension != 'zip':
                up_nz: UploadFile = UploadOther(upload_dir, self.file)
            else:
                up_nz: UploadFile = UploadZipArchive(upload_dir, self.file)

            up_nz.upload()

                
            return {'message': 'file saved'}

        except ValueError as err:
            return {"error": str(err)}