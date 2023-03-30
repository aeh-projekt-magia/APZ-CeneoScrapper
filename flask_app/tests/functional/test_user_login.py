def test_login(client, database, test_user_data):
    client.get("/logout", follow_redirects=True)
    response = client.post("/register", data=dict(
        email=test_user_data['email'],
        password=test_user_data['password'],
        confirm=test_user_data['password']), follow_redirects=True)
    client.get("/logout", follow_redirects=True)

    response = client.post("/login", data=dict(
        email=test_user_data['email'],
        password=test_user_data['password']), follow_redirects=True)

    assert b'You have logged in successfully' in response.data
