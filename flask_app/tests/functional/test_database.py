import pytest
from sqlalchemy.exc import IntegrityError
from app.models.UserModel import User
from app import db


def test_user(app, test_user_data):
    new_user = User(test_user_data["email"], test_user_data["password"])
    db.session.add(new_user)
    db.session.commit()
    user = User.query.filter_by(email=test_user_data["email"]).first()

    assert user.email == test_user_data["email"]
    assert user.password != test_user_data["password"]
    assert user.is_admin is False
    assert user.is_confirmed is False


@pytest.mark.xfail(raises=IntegrityError)
def test_user_duplicated_email(app, test_user_data):
    user = User(email=test_user_data["email"], password=test_user_data["password"])
    db.session.add(user)
    db.session.commit()
    user2 = User(email=test_user_data["email"], password=test_user_data["password"])
    db.session.add(user2)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
