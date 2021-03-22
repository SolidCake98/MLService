from abc import ABC, abstractmethod
import application.services.dataset.read_csv as rcsv
import json
import os
import magic
import socket

from application.config import Config


class ReadFile(ABC):

    @abstractmethod
    def read(self, path, pos):
        pass


class ReadCSVFile(ReadFile):

    def read(self, path, pos):
        response = {}
        reader = rcsv.ReadCSVFile(os.path.join(Config.DATASETS_ABS_PATH, path))

        if pos == 0:
            response['type'] = 'csv'
            header = reader.get_header()

            response['header'] = header
        
        response['data'] = reader.read_small_chunck(pos)
        return response


class ReadIMGFile(ReadFile):

    uri_to_img = 'http://localhost:5000/api/v1/dataset/img/'

    def read(self, path, pos):
        response = {'type': 'img', 'data': self.uri_to_img + path}
        return response


class ReadTXTFile(ReadFile):

    def read(self, path, pos):
        response = {'type': 'text'}
        with open(os.path.join(Config.DATASETS_ABS_PATH, path)) as f:
            response['data'] = f.read()
        return response


class ReadJSONFile(ReadFile):

    def read(self, path, pos):
        response = {'type': 'json'}
        with open(os.path.join(Config.DATASETS_ABS_PATH, path)) as f:
            response['data'] = json.load(f)
        return response


class ReadUndefinedFile(ReadFile):

    def read(self, path, pos):
        return {'error': 'Incorrect type'}


class ReaderCreator:

    def create(self, path):
        type_file = magic.from_file(os.path.join(Config.DATASETS_ABS_PATH, path), mime=True)

        if type_file.split('/')[0] == 'text':
            try:
                extension = path.rsplit('.', 1)[1].lower()
                if extension == 'csv':
                    return ReadCSVFile()
                return ReadTXTFile()
            except ValueError:
                return ReadTXTFile()

        if type_file.split('/')[0] == 'image':
            return ReadIMGFile()

        if type_file == 'application/json':
            return ReadJSONFile()

        return ReadUndefinedFile()
