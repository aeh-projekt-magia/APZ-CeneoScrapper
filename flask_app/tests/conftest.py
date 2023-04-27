import pytest

from config import TestingConfig
from app import create_app, db


@pytest.fixture()
def app():
    app = create_app(TestingConfig)
    app_context = app.app_context()
    app_context.push()
    db.create_all()

    yield app

    db.session.remove()
    db.drop_all()
    app_context.pop()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def test_user_data():
    return {"email": "test_user01@yahoo.com", "password": "123456"}


@pytest.fixture()
def test_admin_data():
    return {
        "email": "admin@admin.admin",
        "password": "123456",
        "is_admin": True,
        "is_confirmed": True,
    }
