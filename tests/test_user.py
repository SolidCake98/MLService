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
    reg.registrate()

def auth_user(json):
    auth = user_services.AuthorizationService(json)
    code, response = auth.athorizate()
    return code, response



def test_register_user(session):
    register_user(json_r)

    fc = facades.UserFacade()
    user = fc.get_user_by_username(json_r["username"])

    assert user.email == json_r["email"]

def test_auth_user(session):
    register_user(json_r)
    code, response = auth_user(json_a)

    assert code == 200
