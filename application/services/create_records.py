import os

from passlib.hash import pbkdf2_sha256 as sha256
from abc import ABC, abstractmethod
from application import models
from application.facades import facades


class Creator(ABC):
    """
    Abstract create records of datasets based on ther json
    """

    @abstractmethod
    def create(self):
        pass


class UserCreator(Creator):

    def __init__(self, g_facade, ug_facade, u_facade, data):
        self.data = data
        self.g_facade = g_facade
        self.ug_facade = ug_facade
        self.u_facade = u_facade
    
    def generate_hash(self, password):
        return sha256.hash(password)
    
    def create_user(self):
        new_user = models.User(
            username = self.data["username"],
            email    = self.data["email"],
            password = self.generate_hash(self.data["password"])
        )
        return new_user

    def create_user_group(self, user: models.User, type_group: str):
        user_group = models.UserGroup(
            user  = user,
            group = self.g_facade.get_group_by_name(type_group)
        )
        return user_group

    def create(self):
        user = self.create_user()
        self.u_facade.create(user)
        self.ug_facade.create(self.create_user_group(user, "user"))
        return user


class DataSetCreator(Creator):
    """
    Create record of dataset
    """

    def __init__(self, data, user):
        self.data = data
        self.user = user

    def __create_meta(self, dir):
        meta = models.DataSetMeta(
            path = dir,
        )
        return meta

    def __create_info(self):

        new_dataset = models.DataSet(
            name  =  self.data['name'],
            title = self.data['title'],
            owner_id = self.user['id']
        )

        return new_dataset

    def create(self):
        dataset = self.__create_info()
        meta = self.__create_meta(os.path.join(self.user['username'], dataset.name))

        dataset.dataset_meta = meta
        facades.DataSetFacade().create(dataset)

        return dataset

    def set_size(self, dataset, total_size):
        sizes = ['B', 'KB', 'MB', 'GB']

        size_name = ""
        size = 0

        for el in sizes:
            if total_size[el] > 0:
                size_name = el
                size = total_size[el]

        dataset.dataset_meta.size = size
        dataset.dataset_meta.size_name = size_name

        facades.DataSetFacade().change(dataset)


class DataSetTypeCreator(Creator):
    """
    Create record of dataset file type
    """

    def __init__(self, types, dataset):
        self.types = types
        self.dataset = dataset

    def __get_types(self):
        type_ar = []

        for t in self.types:
            type_d = facades.FileTypeFacade().get_type_by_name(t)
            type_ar.append(type_d)

        return type_ar

    def create(self):
        dt_facade = facades.DataSetTypeFacade()
        types = self.__get_types()
        for t in types:
            dtype = models.DataSetType(
                dataset = self.dataset,
                file_type = t
            )
            dt_facade.create(dtype)


class DataSetTagCreator(Creator):
    """
    Create record of dataset file type
    """

    def __init__(self, dataset, data):
        self.dataset = dataset
        self.data = data

    def __get_tags(self):
        t_facade = facades.TagFacade()
        tag_ar = []
        for tag in self.data['tags']:
            t = t_facade.get_tag_by_name(tag['tag_name'])
            if not t:
                t = models.Tag(tag_name=tag['tag_name'])
                t_facade.create(t)
            tag_ar.append(t)

        return tag_ar

    def create(self):
        dt_facade = facades.DataSetTagFacade()
        tags = self.__get_tags()
        for t in tags:
            dtag = models.DataSetTag(
                dataset=self.dataset, 
                tag=t
            )
            dt_facade.create(dtag)
