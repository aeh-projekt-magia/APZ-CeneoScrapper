from app.models.models import User
def test_login(client, database, test_user_data):
    """Check if regular user exists and can be logged to"""
    database.session.add(User(**test_user_data))
    database.session.commit()

    client.get("/logout", follow_redirects=True)

    response = client.post("/login", data=dict(**test_user_data), follow_redirects=True)

    assert b'You have logged in successfully' in response.data


def test_login_admin(client, database, test_admin_data):
    """Check if admin account exists and can be logged to"""
    database.session.add(User(**test_admin_data))
    database.session.commit()

    client.get("/logout", follow_redirects=True)

    response = client.post("/login", data=dict(**test_admin_data), follow_redirects=True)

    assert b'You have logged in successfully' in response.data
