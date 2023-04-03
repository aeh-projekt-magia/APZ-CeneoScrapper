import pytest

from app import create_app, db
from app.models.models import User


@pytest.fixture()
def app():
    app = create_app()
    
    yield app


@pytest.fixture()
def database(app):
    with app.app_context():
        db.drop_all()
        db.create_all()

    yield db
    db.drop_all()
    db.create_all()


@pytest.fixture()
def client(app, database):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def test_user_data():
    return {'email': 'test_user01@yahoo.com', 'password': '123456'}


@pytest.fixture()
def test_admin_data():
    return {'email': 'admin@admin.admin', 'password': '123456', 'is_admin': True, 'is_confirmed':True}