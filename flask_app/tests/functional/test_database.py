import pytest
from sqlalchemy.exc import IntegrityError

from app.models.UserModel import User
from app import db

def test_user(app,database, test_user_data):
    with app.app_context():
        new_user = User(test_user_data['email'], test_user_data['password'])
        db.session.add(new_user)
        db.session.commit()
        user = db.session.execute(db.select(User).filter_by(email=test_user_data['email'])).scalar_one()

    assert user.email == test_user_data['email']
    assert user.password != test_user_data['password']
    assert user.is_admin is False
    assert user.is_confirmed is False


@pytest.mark.xfail(raises=IntegrityError)
def test_user_duplicated_email(app,database, test_user_data):
    with app.app_context():
        user = User(email=test_user_data['email'], password=test_user_data['password'])
        db.session.add(user)
        db.session.commit()
        user2 = User(email=test_user_data['email'], password=test_user_data['password'])
        db.session.add(user2)
    
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
