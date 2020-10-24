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
from threading import Thread, Lock
import re

dataset_directory = os.path.join(os.path.abspath(os.path.join(BASE_DIR, os.pardir)), Config.DATASETS_PATH)


class DataSetPathStructure:

    def __init__(self, json):
        self.path = os.path.join(dataset_directory, json['path'])
        self.pos = json['pos']

    def sorted_alphanumeric(self, data):
        convert = lambda text: int(text) if text.isdigit() else text.lower()
        alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
        return sorted(data, key=alphanum_key)

    def read(self, offset = 20):

        res = {}
        lst = []

        dir_list = self.sorted_alphanumeric(os.listdir(self.path))
        count = len(dir_list)

        s_dir_list = sorted(dir_list, key= lambda x : not os.path.isdir(os.path.join(self.path, x)))

        res['dir'] = lst
        res['next_pos'] = (self.pos + offset) if max(0, count - (self.pos + offset)) else 0

        res['count'] = max(0, count - (self.pos + offset))

        for i, x in enumerate(s_dir_list[self.pos: self.pos + offset]):

            dir_info = {}

            if os.path.isdir(os.path.join(self.path, x)):
                dir_info['type'] = 'directory'
                
            else:
                dir_info['type'] = 'file'

            dir_info['id'] = self.pos + i
            dir_info['name'] = os.path.basename(x)

            lst.append(dir_info)

        return res
        

        


class DataSetDownloadService:

    """
    Service for downloading of datasets
    """

    def download(self, path):
        
        z = zipstream.ZipFile(mode='w', compression=zipstream.ZIP_DEFLATED)
        pat = os.path.join(dataset_directory, path)

        
        for root, dirs, files in os.walk(pat):
            for file in files:
                absname = os.path.abspath(os.path.join(root, file))
                arcname = absname[len(pat) + 1:]
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

        sizes = ['B', 'KB', 'MB', 'GB']
        total_size = {'B': 0, 'KB': 0, 'MB': 0, 'GB': 0}

        for dirpath, dirnames, filenames in os.walk(dir):
            for f in filenames:
                fp = os.path.join(dirpath, f)

                size = os.path.getsize(fp)
                i = 0

                while size > 0 and i < len(sizes):
                    total_size[sizes[i]] += size % 1024
                    size = size // 1024
                    i += 1
                
                for s in range(len(sizes) - 1):
                    if total_size[sizes[s]] // 1024 > 0:
                        total_size[sizes[s+1]] +=  total_size[sizes[s]] // 1024
                        total_size[sizes[s]] = total_size[sizes[s]] % 1024

                try:
                    extesion = f.rsplit('.', 1)[1].lower()
                except:
                    extesion = ''
                if extesion not in self.types:
                    types.add('other')
                else:
                    types.add(extesion)

        return types, total_size

    
    def __check_error_dataset(self, name):
        if facades.DataSetFacade().get_dataset_by_name(name):
            raise ValueError('Data set with this name was already upload')


    def upload(self):

        def extract(arch:up.Extractor):
            mutex.acquire()
            arch.extract()
            mutex.release()

        def write_dataset(upload_dir:str, dataset_id:int):
            
            dataset = facades.DataSetFacade().get_entity(dataset_id)

            mutex.acquire()
            types, size = self.find_types_and_size(upload_dir)
            mutex.release()

            d_creator.set_size(dataset, size)
            d_type = cr.DataSetTypeCreator(types, dataset)
            d_type.create()

            dataset.is_loaded = True
            facades.DataSetFacade().change(dataset)


        try:
            f_validate = FilenameValidate(self.file.filename)
            f_validate.validate()
            self.__check_error_dataset(self.data['name'])

            upload_dir = os.path.join(dataset_directory, self.user['username'], self.data['name'])
            upload_creator = up.UploadCreator(upload_dir, self.file)

            uploader = upload_creator.create()
            uploader.upload()


            mutex = Lock()

            extr = upload_creator.get_extractor()
            if extr:
                thread_2 = Thread(target=extract, kwargs={'arch': extr})
                thread_2.start()

            d_creator = cr.DataSetCreator(self.data, self.user)
            dataset = d_creator.create()

            thread_1 = Thread(target=write_dataset, kwargs={'upload_dir': upload_dir, 'dataset_id': dataset.id})
            thread_1.start() 

            return {'message': 'file saved'}, 200

        except ValueError as err:
            return {"error": str(err)}, 400

        except Exception as err:
            return {"error": "Can't upload dataset"}, 500

#TODO добавить сервисы для добавления описания и тэгов