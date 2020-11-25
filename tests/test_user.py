from application.services import user_services
from application.facades import facades
from passlib.hash import pbkdf2_sha256 as sha256
from werkzeug.datastructures import FileStorage

json_r = {
        "username": "danil",
        "email": "some.email@server.com",
        "password": "1234567f"
    }

json_a = {
        "username": "some.email@server.com",
        "password": "1234567f"
    }


def register_user(json):
    reg = user_services.RegistrationService(json)
    return reg.registrate()

def auth_user(json):
    auth = user_services.AuthorizationService(json)
    code, response = auth.athorizate()
    return code, response


def test_register_user(session):
    code, result = register_user(json_r)

    fc = facades.UserFacade()
    user = fc.get_user_by_username(json_r["username"])

    assert user.email == json_r["email"]

def test_register_not_valid_password_user(session):
    json_r_not_valid_password = {
        "username": "danil",
        "email": "some.email@server.com",
        "password": "1234567"
    }

    code, result = register_user(json_r_not_valid_password)
    print(code, result)
    assert code == 400 

def test_register_not_valid_username_user(session):
    json_r_not_valid_username = {
        "username": "12345",
        "email": "some.email@server.com",
        "password": "1234567f"
    }
    code, result = register_user(json_r_not_valid_username)
    print(code, result)
    assert code == 400

def test_register_user_is_already_exist(session):

    register_user(json_r)
    code, result = register_user(json_r)
    print(code, result)
    assert code == 400 

def test_register_user_email_is_already_exist(session):
    json_r_new = {
        "username": "daniil",
        "email": "some.email@server.com",
        "password": "1234567f"
    }
    register_user(json_r)
    code, result = register_user(json_r_new)
    print(code, result)
    assert code == 400 




def test_auth_user(session):
    register_user(json_r)
    code, response = auth_user(json_a)
    assert code == 200

def test_auth_user_not_vaild_email(session):
    json_not_valid_email = {
        "username": "some.emal@server.com",
        "password": "1234567f"
    }
    register_user(json_r)
    code, response = auth_user(json_not_valid_email)

    print(code, response)
    assert code == 400

def test_auth_not_valid_name(session):
    json_not_valid_name = {
        "username": "daniil",
        "password": "1234567f"
    }
    register_user(json_r)
    code, response = auth_user(json_not_valid_name)

    print(code, response)
    assert code == 400

def test_auth_not_valid_password(session):
    json_not_valid_password = {
        "username": "danil",
        "password": "1234"
    }
    register_user(json_r)
    code, response = auth_user(json_not_valid_password)

    print(code, response)
    assert code == 400
