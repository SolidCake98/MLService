from abc import ABC, abstractmethod
from typing import List
from application.facades.facades import UserFacade


class Validate(ABC):

    @abstractmethod
    def validate(self):
        pass

class UsernameValidate(Validate):

    def __init__(self, username: str):
        self.email = email

    def validate(self):
        facade = UserFacade()

        if facade.get_user_by_username(self.username):
            raise

class EmailValidate(Validate):

    def __init__(self, email: str):
        self.email = email

    def validate(self):
        pass

class PasswordValidate(Validate):
    
    def __init__(self, password: str):
        self.password = password

    def validate(self, object):
        pass

class UserValidateProcess:

    def __init__(self, user: models.User):

        self.validation_list: List[Validate] = [
            UsernameValidate(user.username),
            EmailValidate(user.email),
            PasswordValidate(user.password)
        ]

    def validate_params(self):

        for el in self.validation_list:
            el.validate()