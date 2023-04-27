import pytest

from app.models.UserModel import User


@pytest.mark.parametrize(
    "test_user", [{"email": "test_user01@yahoo.com", "password": "123456"}]
)
def test_new_user(test_user):
    """
    Check if user model works properly,
    assigns proper values and hashes a password
    """
    user = User(test_user["email"], "Testpassword2130")
    assert user.email is test_user.get("email")
    assert user.password is not test_user.get("password")
    assert user.is_admin is False
    assert user.is_confirmed is False
