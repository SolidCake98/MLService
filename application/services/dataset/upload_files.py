import os
import shutil
from abc import ABC, abstractmethod

class UploadFile(ABC):

    """
    It's an abstract class for uploading datasets and expansion it
    """
    
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


class UploadOther(UploadFile):

    """
    Upload all files except archives
    """

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


class UploadZipArchive(UploadFile):
    """
    Upload archives
    """

    def __init__(self, path, file):
        self.path = path
        self.file = file

    def upload(self):
        self.clear_path(self.path)
        file_path = os.path.join(self.path, self.name)
        self.file.save(file_path)

    def add(self):
        zip_file = zipfile.ZipFile(self.file)
        zip_file.extractall(self.path)
        zip_file.close()


class Extractor(ABC):
    """
    Abstract to extract achives into folder
    """

    @abstractmethod
    def extract():
        pass

class ZipExtractot(Extractor):
    """
    Extractor for zip archives
    """

    def __init__(self, path, name):
        self.path = path 
        self.name = name

    def extract(self):
        file_path = os.path.join(self.path, self.name)
        zip_file = zipfile.ZipFile(file_path)
        zip_file.extractall(self.path)
        zip_file.close()
        os.remove(file_path)