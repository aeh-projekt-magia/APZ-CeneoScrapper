import pytest

from app import create_app, db
from app.models.models import User



def test_home_page(client, test_user_data):
    """Check if home page works"""
    response = client.get("/", follow_redirects=True)
    assert response.status_code == 200

