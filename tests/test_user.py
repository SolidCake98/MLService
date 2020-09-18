from application.models import User, Group, UserGroup
from application.facades.user_facade import UserFacade
from sqlalchemy.orm import  sessionmaker
from passlib.hash import pbkdf2_sha256 as sha256

def test__create_user(session):
    email       = "some.email@server.com"
    password    = "123456"
    username    = "dddddd"
    first_name  = "dddd"
    last_name   = "ddddddd"

    user        = User(email=email, password=sha256.hash(password), username=username, first_name=first_name, last_name=last_name) 
    group       = Group(name="admin")
    ug          = UserGroup(user=user, group=group)


    fc = UserFacade()
    fc.create(user)

    # session.add(group)
    # session.add(ug)

    #session.commit()

    em = User.query.first()
    print(fc.get_all()[0].password)

    assert em.email == email