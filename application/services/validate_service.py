from abc import ABC, abstractmethod
from typing import List
from application import models
from application.facades.facades import UserFacade
import re
from passlib.hash import pbkdf2_sha256 as sha256


class Validate(ABC):

    @abstractmethod
    def validate(self):
        pass


class PasswordValidate(Validate):

    valid_password_regex = "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"

    def __init__(self, password: str):
        self.password = password

    def validate(self):
        if not re.match(self.valid_password_regex, self.password):
            raise ValueError("Password mus be at least 8 characters, conatain 1 number and 1 letter ")


class EmailValidate(Validate):
    valid_email_regex = "[^@]+@[^@]+\.[^@]+"

    def __init__(self, email: str):

        self.email = email

    def validate(self):
        if not re.match(self.valid_email_regex, self.email):
            raise ValueError("Incorrect email value")
        

class UserValidateProcess(Validate):

    def __init__(self):
        self.validation_list: List[Validate] = []
        
    def register(self, *validation: Validate):
        for el in validation:
            self.validation_list.append(el)

    def validate(self):
        for el in self.validation_list:
            el.validate()


class FilenameValidate(Validate):

    ALLOWED_EXTENSIONS = [
        'zip',
        'csv',
        'json'
    ]

    def __init__(self, filename):
        self.filename = filename

    def allowed_file(self):
        return '.' in self.filename and \
           self.filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    def validate(self):
        if self.filename == '':
            raise ValueError('Not selected file')
        if not self.allowed_file():
            raise ValueError('Incorrect file type')