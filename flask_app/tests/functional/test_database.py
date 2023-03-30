import pytest

from app.models.models import User
from sqlalchemy.exc import IntegrityError



def test_user(database, test_user_data):
    new_user = User(test_user_data['email'], test_user_data['password'])

    database.session.add(new_user)
    database.session.commit()

    user = User.query.filter_by(email=test_user_data['email']).first()

    assert user.email == test_user_data['email']
    assert user.password != test_user_data['password']
    assert user.is_admin is False
    assert user.is_confirmed is False



@pytest.mark.xfail(raises=IntegrityError)
def test_user_duplicated_email(database, test_user_data):

    user = User(email=test_user_data['email'], password=test_user_data['password'])
    database.session.add(user)
    database.session.commit()

    user2 = User(email=test_user_data['email'], password=test_user_data['password'])
    database.session.add(user2)
    try:
        database.session.commit()
    except IntegrityError:
        database.session.rollback()




