import os
from abc import ABC, abstractmethod
from application.config import Config, BASE_DIR
from application.facades import facades
from application.services.validate_service import FilenameValidate
from flask import Response
from application import models, schemas
from werkzeug.utils import secure_filename
import zipfile
import zipstream
import shutil
from threading import Thread

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

    def extract(self):
        file_path = os.path.join(self.path, self.name)
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


#TODO add tags
class DataSetUploadService:

    types = [
        'csv',
        'json'
    ]

    def __init__(self, json, user, file):
        self.json = json
        self.user = user
        self.file = file

        self.d_facade = facades.DataSetFacade()
        self.tag_facade = facades.TagFacade()
        self.type_facade = facades.FileTypeFacade()
        self.dtype_facade = facades.DataSetTypeFacade()
        self.dtag_facade = facades.DataSetTagFacade()

    

    def create_dataset_info(self):
        data = schemas.DataSetSchema().load(data=self.json)

        new_dataset = models.DataSet(
            name = data['name'],
            title = data['title'],
            description = data['description'],
            owner_id = self.user['id']
        )
        
        return new_dataset


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



    def create_meta(self, dir, size):
        meta = models.DataSetMeta(
            path = dir,
            size = size
        )
        return meta

    def check_dataset(self, name):
        if self.d_facade.get_dataset_by_name(name):
            raise ValueError('DataSet with this name was already upload')

    def save(self, dataset, meta, types):
        dataset.dataset_meta = meta 
        self.d_facade.create(dataset)
        print(types)
        for t in types:
            type = self.type_facade.get_type_by_name(t)
            dtypy = models.DataSetType(
                dataset = dataset,
                file_type = type
            )
            self.dtype_facade.create(dtypy)
        

    def upload(self):
        f_validate = FilenameValidate(self.file.filename)

        def write_dataset(zi, upload_dir, name):
            zi.extract()
            types, size = self.find_types_and_size(upload_dir)
            meta = self.create_meta(os.path.join(self.user['username'], name), size)
            self.save(dataset, meta, types)

        try:
            f_validate.validate()
            extension = self.file.filename.rsplit('.', 1)[1].lower()

            dataset = self.create_dataset_info()
            self.check_dataset(dataset.name)
            upload_dir = os.path.join(dataset_directory, self.user['username'], dataset.name)

            if extension != 'zip':
                up_nz: UploadFile = UploadOther(upload_dir, self.file)
            else:
                up_nz: UploadFile = UploadZipArchive(upload_dir, self.file)

            up_nz.upload()

            thread = Thread(target=write_dataset, kwargs={'zi': up_nz, 'upload_dir': upload_dir, 'name':dataset.name})
            thread.start()

            return {'message': 'file saved'}, 200


        except ValueError as err:
            return {"error": str(err)}, 400

        except Exception as err:
            return {"error": "Can't upload dataset"}, 400