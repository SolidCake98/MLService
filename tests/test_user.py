from application.services import user_services
from application.facades import facades
from sqlalchemy.orm import  sessionmaker
from passlib.hash import pbkdf2_sha256 as sha256

json = {
        "username": "danil",
        "email": "some.email@server.com",
        "password": "1234567f"
    }


def register_user():
    reg = user_services.RegistrationService(json)
    reg.registrate()


def test_register_user(session):
    register_user()

    fc = facades.UserFacade()
    user = fc.get_user_by_username(json["username"])

    assert user.email == json["email"]

def test_auth_user(session):
    register_user()

    json = {
        "username": "danil",
        "password": "1234567f"
    }

    auth = user_services.AuthorizationService(json)
    code, response = auth.athorizate()

    assert response['access_token'] != None