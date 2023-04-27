def test_home_page(client):
    """Check if home page works and returns expected values, without user logged in"""
    response = client.get("/", follow_redirects=True)
    assert response.status_code == 200
    assert b"Please log in to access this page." in response.data


def test_home_page_aliases(client):
    """Check if other page works and returns expected values, without user logged in"""
    assert (
        b"Please log in to access this page."
        in client.get("/", follow_redirects=True).data
    )
    assert (
        b"Please log in to access this page."
        in client.get("/products/", follow_redirects=True).data
    )
