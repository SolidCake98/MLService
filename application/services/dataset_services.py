import os
from application.config import Config
from application.facades import facades
from application.services.validate_service import FilenameValidate
from application.services.dataset import upload_files as up
from application.services import create_records as cr

from flask import Response, send_from_directory
from application import schemas
import zipstream
from threading import Thread, Lock
import re
import imghdr


# TODO сделать раздление по файлам
# TODO когда гружу директории сразу грузить и uri для картинок
class DataSetPathStructure:

    def __init__(self, json):
        self.path = os.path.join(Config.DATASETS_ABS_PATH, json['path'])
        self.pos = json['pos']

    def sorted_alphanumeric(self, data):
        convert = lambda text: int(text) if text.isdigit() else text.lower()
        alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
        return sorted(data, key=alphanum_key)

    def check_path_exists(self, path):
        return os.path.exists(path)

    def create_dir_struct(self, dir_list, from_pos, to_pos):
        lst = []

        for i, x in enumerate(dir_list[from_pos: to_pos]):

            dir_info = {}

            if os.path.isdir(os.path.join(self.path, x)):
                dir_info['type'] = 'directory'

            else:
                dir_info['type'] = 'file'

            dir_info['id'] = self.pos + i
            dir_info['name'] = os.path.basename(x)

            lst.append(dir_info)

        return lst

    def sort_dir_list(self, list_dir):
        alpabec_dir_list = self.sorted_alphanumeric(list_dir)
        s_dir_list = sorted(alpabec_dir_list, key=lambda x: not os.path.isdir(os.path.join(self.path, x)))
        return s_dir_list

    def read(self, offset=20):

        res = {}

        if not self.check_path_exists(self.path):
            return 404, {'error': 'dataset not found'}

        s_dir_list = self.sort_dir_list(os.listdir(self.path))

        count = len(s_dir_list)

        res['next_pos'] = (self.pos + offset) if max(0, count - (self.pos + offset)) else 0
        res['count'] = max(0, count - (self.pos + offset))
        res['dir'] = self.create_dir_struct(s_dir_list, self.pos, self.pos + offset)

        return 200, res


class DataSetDownloadService:
    """
    Service for downloading of datasets
    """

    def download(self, path):

        z = zipstream.ZipFile(mode='w', compression=zipstream.ZIP_DEFLATED)
        pat = os.path.join(Config.DATASETS_ABS_PATH, path)

        if not os.path.exists(pat):
            return 404, {'error': "Path didn't exist"}

        for root, dirs, files in os.walk(pat):
            for file in files:
                absname = os.path.abspath(os.path.join(root, file))
                arcname = absname[len(pat) + 1:]
                z.write(absname, arcname=arcname)

        response = Response(z, mimetype='application/zip')
        response.headers['Content-Disposition'] = 'attachment; filename={}'.format('archive.zip')
        return 200, response


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

    def get_type(self, f):
        try:
            extension = f.rsplit('.', 1)[1].lower()
        except ValueError:
            extension = ''

        if extension not in self.types:
            return 'other'
        else:
            return extension

    # TODO нормальный поиск типов файла
    def find_types_and_size(self, dir):
        types = set()

        sizes = ['B', 'KB', 'MB', 'GB']
        total_size = {'B': 0, 'KB': 0, 'MB': 0, 'GB': 0}

        for dirpath, _, filenames in os.walk(dir):
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
                        total_size[sizes[s + 1]] += total_size[sizes[s]] // 1024
                        total_size[sizes[s]] = total_size[sizes[s]] % 1024

                types.add(self.get_type(f))

        return types, total_size

    def __check_error_dataset(self, name):
        if facades.DataSetFacade().get_dataset_by_name(name):
            raise ValueError('Data set with this name was already upload')

    def upload(self):

        def extract(arch: up.Extractor):
            mutex.acquire()
            arch.extract()
            mutex.release()

        def write_dataset(upload_dir: str, dataset_id: int):

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

            upload_dir = os.path.join(Config.DATASETS_ABS_PATH, self.user['username'], self.data['name'])
            upload_creator = up.UploadCreator(upload_dir, self.file)

            uploader = upload_creator.create()
            uploader.upload()
            mutex = Lock()

            extr = upload_creator.get_extractor()

            if extr:
                thread_2 = Thread(target=extract, kwargs={'arch': extr})
                # extract(extr)
                thread_2.start()

            d_creator = cr.DataSetCreator(self.data, self.user)
            dataset = d_creator.create()

            thread_1 = Thread(target=write_dataset, kwargs={'upload_dir': upload_dir, 'dataset_id': dataset.id})
            thread_1.start()
            write_dataset(upload_dir, dataset.id)

            return 200, {'message': 'file saved'}

        except ValueError as err:
            return 400, {"error": str(err)}

        except Exception as err:
            return 500, {"error": "Can't upload dataset"}


class DataSetReadFile:

    def __init__(self, json, reader):
        self.json = json
        self.path = self.json['path']
        self.abs_path = os.path.join(Config.DATASETS_ABS_PATH, self.path)
        self.pos = self.json['pos']
        self.reader = reader

    def read(self):
        return self.reader.read(self.path, self.pos)


class DataSetImage:

    def __init__(self, path):
        self.path = path

    @staticmethod
    def check_img(path):
        allowed_img_types = ['gif', 'jpeg', 'png']
        return imghdr.what(path) in allowed_img_types

    def send_image(self):

        if self.check_img(os.path.join(Config.DATASETS_ABS_PATH, self.path)):
            return send_from_directory(Config.DATASETS_ABS_PATH, self.path)

        else:
            return 404
