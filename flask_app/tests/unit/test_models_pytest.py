import pytest

from app.models.models import User_Legacy
from app.models.UserModel import User
from app.repository.UserRepository import addUser, updateUser, getUser, getAllUsers, deleteUser, deleteAllUsers

@pytest.mark.parametrize("test_user_legacy", [{
    'email': "test_user01@yahoo.com",
    'password': "123456"
}])
def test_new_user(test_user_legacy):
    """
    Check if user model works properly, 
    assigns proper values and hashes a password
    """
    user = User_Legacy(test_user_legacy['email'], 'Testpassword2130')
    assert user.email is test_user_legacy.get('email')
    assert user.password is not test_user_legacy.get('password')
    assert user.is_admin is False
    assert user.is_confirmed is False

@pytest.mark.parametrize("test_user", [{
    'email': "test_user01@yahoo.com",
    'password': "123456",
    'is_admin': False
}])
def test_addUser(test_user):
    """
    Check if user is added
    """
    user = User(test_user['email'],test_user['password'],test_user['is_admin'])
    assert user.email is test_user.get('email')
    assert user.password is test_user.get('password')
    assert user.is_admin is test_user.get('is_admin')