import pytest

from app import create_app, db
from config import DevelopmentConfig


@pytest.fixture()
def app():
    app = create_app(config_class=DevelopmentConfig)
    # app.config.from_object("config.DevelopmentConfig")

    yield app


@pytest.fixture()
def database(app):
    with app.app_context():
        db.create_all()

    yield db
    db.drop_all()


@pytest.fixture()
def client(app, database):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def test_user_data():
    dictionary = {'email': "test_user01@yahoo.com", 'password': "123456"}
    return dictionary
