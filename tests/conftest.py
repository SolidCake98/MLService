import pytest
from application.app import create_app

@pytest.fixture
def app():
    app = create_app("testing")
    return app

@pytest.fixture(scope="function")
def session(app):
    with app.app_context():
        from application.database import Base, engine, db_session
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine) 

    yield db_session