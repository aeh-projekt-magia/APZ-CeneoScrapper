import datetime
import unittest

from base_test import BaseTestCase
from flask_login import current_user

from app import bcrypt
from app.models.models import User


class TestUser(BaseTestCase):
    def test_user_registration(self):
        """Add new user, and check if it exists in database"""
        with self.client:
            self.client.get("/logout", follow_redirects=True)
            response = self.client.post(
                "/register",
                data=dict(
                    email="test@user.com", password="test_user", confirm="test_user"
                ),
                follow_redirects=True,
            )
            user = User.query.filter_by(email="test@user.com").first()

            self.assertTrue(user.id)
            self.assertTrue(user.email == "test@user.com")
            self.assertFalse(user.is_admin)

    def test_get_by_id(self):
        """Try to log in as admin"""
        with self.client:
            self.client.get("/logout", follow_redirects=True)
            self.client.post(
                "/login",
                data=dict(email="ad@min.com", password="admin_user"),
                follow_redirects=True,
            )
            # Musi być dodane rzutowanie na stringa bo sie wywala xD
            self.assertTrue(current_user.get_id() == '1')

    def test_created_on_defaults_to_datetime(self):
        """Check if datetime is datetime"""
        with self.client:
            self.client.get("/logout", follow_redirects=True)
            self.client.post(
                "/login",
                data=dict(email="ad@min.com", password="admin_user"),
                follow_redirects=True,
            )
            user = User.query.filter_by(email="ad@min.com").first()
            self.assertIsInstance(user.created_on, datetime.datetime)

    def test_check_password(self):
        """Check if password is correct after unhashing"""
        user = User.query.filter_by(email="ad@min.com").first()
        self.assertTrue(bcrypt.check_password_hash(user.password, "admin_user"))
        self.assertFalse(bcrypt.check_password_hash(user.password, "dupa"))

    def test_validate_invalid_password(self):
        """Try to log in using incorrect password"""

        with self.client:
            self.client.get("/logout", follow_redirects=True)
            response = self.client.post(
                "/login",
                data=dict(email="ad@min.com", password="foo_bar"),
                follow_redirects=True,
            )
        self.assertIn(b"Invalid email and/or password.", response.data)


if __name__ == "__main__":
    unittest.main()
