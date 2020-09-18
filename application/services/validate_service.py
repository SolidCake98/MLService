from abc import ABC, abstractmethod
from typing import List
from application import models
from application.facades.facades import UserFacade
import re


class Validate(ABC):

    @abstractmethod
    def validate(self):
        pass

class UsernameValidate(Validate):

    def __init__(self, username: str):
        self.username = username

    def validate(self):
        facade = UserFacade()

        if facade.get_user_by_username(self.username):
            raise ValueError(f"User {self.username} already exists")


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
        facade = UserFacade()

        if facade.get_user_by_email(email=self.email):
            raise ValueError(f"Email {self.email} already registred")

        if not re.match(self.valid_email_regex, self.email):
            raise ValueError("Incorrect email value")
        

class UserValidateProcess(Validate):

    def __init__(self, user: models.User):
        
        self.validation_list: List[Validate] = [
            UsernameValidate(user.username),
            PasswordValidate(user.password),
            EmailValidate(user.email)
        ]

    def validate(self):

        for el in self.validation_list:
            el.validate()