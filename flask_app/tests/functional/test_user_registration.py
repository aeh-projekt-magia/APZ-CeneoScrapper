from app.models.models import User


def test_home_page(client, test_user_data):
    """Check if home page works"""
    response = client.get("/", follow_redirects=True)
    assert response.status_code == 200
    assert test_user_data['password'] == '123456'


def test_register(client, test_user_data):
    """Check if user can register using correct data"""
    client.get("/logout", follow_redirects=True)
    response = client.post("/register", data=dict(
        email=test_user_data['email'],
        password=test_user_data['password'],
        confirm=test_user_data['password']), follow_redirects=True)

    user = User.query.filter_by(email=test_user_data['email']).first()

    assert user.id
    assert user.email == test_user_data['email']
    assert user.password != test_user_data['password']
    assert user.is_admin is False
    assert user.is_confirmed is False
    assert user.is_active is True

    assert b'You registered and are now logged in. Welcome!' in response.data


def test_register_incorrect_email(client, database):
    """Check if user can't be registered using incorrect email"""
    client.get("/logout", follow_redirects=True)
    response = client.post("/register", data=dict(
        email="test@user",
        password="test_user",
        confirm="test_user"), follow_redirects=True)
    user = User.query.filter_by(email="test@user.com").first()
    assert not user


def test_register_passwords_dont_match(client, database):
    """Check if user can't be registered without matching passwords"""
    client.get("/logout", follow_redirects=True)
    response = client.post("/register", data=dict(
        email="test@user.user",
        password="test_user",
        confirm="012345678"), follow_redirects=True)
    user = User.query.filter_by(email="test@user.com").first()

    assert not user
    assert b"Passwords must match" in response.data


def test_register_email_duplicate(client, database, test_user_data):
    """Check if user can't be registered with email already existing in db"""
    client.get("/logout", follow_redirects=True)
    response = client.post("/register", data=dict(
        email=test_user_data['email'],
        password=test_user_data['password'],
        confirm=test_user_data['password']), follow_redirects=True)

    client.get("/logout", follow_redirects=True)
    response = client.post("/register", data=dict(
        email=test_user_data['email'],
        password=test_user_data['password'],
        confirm=test_user_data['password']), follow_redirects=True)

    assert b'Email already registered' in response.data
