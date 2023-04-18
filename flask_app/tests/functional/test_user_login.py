from app.models.models import User_Legacy
from app import db
def test_login(app,client, database, test_user_data):
    """Check if regular user exists and can be logged to"""
    with app.app_context():
        db.session.add(User_Legacy(**test_user_data))
        db.session.commit()

    client.get("/logout", follow_redirects=True)

    response = client.post("/login", data=dict(**test_user_data), follow_redirects=True)

    assert b'You have logged in successfully' in response.data


def test_login_admin(app, client, database, test_admin_data):
    """Check if admin account exists and can be logged to"""
    with app.app_context():
        db.session.add(User_Legacy(**test_admin_data))
        db.session.commit()

    client.get("/logout", follow_redirects=True)

    response = client.post("/login", data=dict(**test_admin_data), follow_redirects=True)

    assert b'You have logged in successfully' in response.data
