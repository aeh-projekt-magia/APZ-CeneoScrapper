from app.models.models import User
from app import db


def test_login(client, test_user_data):
    """Check if regular user exists and can be logged to"""
    # client = app.test_client()

    db.session.add(User(**test_user_data))
    db.session.commit()

    client.get("/logout", follow_redirects=True)

    response = client.post("/login", data=dict({"email": "test_user01@yahoo.com", "password": "123456"}), follow_redirects=True)

    assert b"You have logged in successfully" in response.data


def test_login_admin(app, test_admin_data):
    """Check if admin account exists and can be logged to"""
    client = app.test_client()
    db.session.add(User(**test_admin_data))
    db.session.commit()

    client.get("/logout", follow_redirects=True)

    response = client.post(
        "/login", data=dict(**test_admin_data), follow_redirects=True
    )

    assert b"You have logged in successfully" in response.data
