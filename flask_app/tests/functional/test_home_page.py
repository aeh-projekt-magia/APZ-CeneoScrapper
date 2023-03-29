import pytest

from app import create_app, db
from app.models.models import User


@pytest.fixture()
def app():
    app = create_app()
    app.config.from_object("config.TestingConfig")

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def database(app):
    with app.app_context():
        db.create_all()

    yield db
    db.drop_all()


def test_home_page_better(client):
    response = client.get("/", follow_redirects=True)
    assert response.status_code == 200


def test_db_post_model(database):
    testuser = User('d@dd.d', 'Testpassword2130')
    database.session.add(testuser)
    database.session.commit()

    user = User.query.filter_by(email=testuser.email).first()

    assert user.email == testuser.email
    assert user.password != 'Testpassword2130'
    assert user.is_admin == False
    assert user.is_confirmed == False
