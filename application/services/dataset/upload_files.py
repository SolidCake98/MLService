import os
import shutil
from abc import ABC, abstractmethod
import zipfile



class AddFile(ABC):

    @abstractmethod
    def add(self):
        pass

class UploadFile(ABC):

    @abstractmethod
    def upload(self):
        pass


class BaseFile:

    """
    It's a basic class for uploading datasets and expansion it
    """

    def __init__(self, path, file):
        self.path = path
        self.file = file
    
    
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


class Extractor(ABC):

    """
    Abstract to extract achives into folder
    """

    @abstractmethod
    def extract(self):
        pass


class UploadOther(BaseFile, UploadFile, AddFile):

    """
    Upload all files except archives
    """
    def __init__(self, path, file):
        super().__init__(path, file)

    def upload(self):
        self.clear_path(self.path)
        file_dir = os.path.join(self.path, self.file.filename)
        self.file.save(file_dir)

    def add(self):
        file_dir = os.path.join(self.path, self.file.filename)
        self.file.save(file_dir)


class UploadZipArchive(BaseFile, UploadFile, AddFile, Extractor):
    """
    Upload archives
    """

    name = 'archive.zip'

    def __init__(self, path, file):
        super().__init__(path, file)

    def upload(self):
        self.clear_path(self.path)
        file_path = os.path.join(self.path, self.name)
        self.file.save(file_path)

    def add(self):
        zip_file = zipfile.ZipFile(self.file)
        zip_file.extractall(self.path)
        zip_file.close()

    def extract(self):
        file_path = os.path.join(self.path, self.name)
        zip_file = zipfile.ZipFile(file_path)
        zip_file.extractall(self.path)
        zip_file.close()
        
        os.remove(file_path)


class UploadCreator:

    def __init__(self, upload_dir, file):
        self.upload_dir = upload_dir
        self.file = file
        self.extension = self.file.filename.rsplit('.', 1)[1].lower()
        self.ext_func = {
            "zip": lambda: self.create_zip_upload(),
            "other": lambda: self.create_other_upload()
        }

    def create_zip_upload(self):
        up_nz = UploadZipArchive(self.upload_dir, self.file)
        return up_nz

    def create_other_upload(self):
        up_nz = UploadOther(self.upload_dir, self.file)
        return up_nz
    
    def create(self):
        try:
            uploader: UploadFile = self.ext_func[self.extension]()
            return uploader
        except:
            uploader: UploadFile = self.ext_func["other"]()
            return uploader

    def get_extractor(self):
        try:
            ext: Extractor = self.ext_func[self.extension]()
            return ext
        except:
            return None