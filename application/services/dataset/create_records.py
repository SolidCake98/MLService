import os

from abc import ABC, abstractmethod
from application import models
from application.facades import facades


class Creator(ABC):
    """
    Abstract create records of datasets based on ther json
    """

    @abstractmethod
    def create():
        pass

#TODO подумать над фабрикой

class DataSetCreator(Creator):
    """
    Create record of dataset
    """

    def __init__(self, data, user, size):
        self.data = data
        self.user = user
        self.size = size

    def __create_meta(self, dir):
        meta = models.DataSetMeta(
            path = dir,
            size = self.size
        )
        return meta

    def __create_info(self):

        new_dataset = models.DataSet(
            name = self.data['name'],
            title = self.data['title'],
            description = self.data['description'],
            owner_id = self.user['id']
        )

        return new_dataset

    def create(self):
        dataset = self.__create_info()
        meta = self.__create_meta(os.path.join(self.user['username'], dataset.name))

        dataset.dataset_meta = meta
        facades.DataSetFacade().create(dataset)

        return dataset
        


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
            try:
                type_d = facades.FileTypeFacade().get_type_by_name(t)
                type_ar.append(type_d)
            except:
                raise Exception("Type doesn't allowes")

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
