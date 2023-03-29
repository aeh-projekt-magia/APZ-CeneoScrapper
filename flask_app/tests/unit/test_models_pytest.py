import pytest

from app.models.models import User

def test_new_user():
    """
    Check if user model works properly
    """
    user = User('jakub@jakub.jakub', 'Testpassword2130')
    assert user.email == 'jakub@jakub.jakub'
    assert user.password != 'Testpassword2130'
    assert user.is_admin == False
    assert user.is_confirmed == False