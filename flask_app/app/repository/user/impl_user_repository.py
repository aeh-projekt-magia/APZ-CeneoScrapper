from typing import List

from app.models.UserModel import User
from app.extensions import db
from repository.user.user_repository import UserRepository


class ImplUserRepository(UserRepository):

    def add_user(self, user):
        db.session.add(user)
        db.session.commit()

    def get_user_by_id(self, user_id) -> User:
        user = db.session.execute(
            db.select(User).filter_by(id=user_id)
        ).scalar_one()
        return user

    def get_user_by_email(self, email_address) -> User:
        user = db.session.execute(
            db.select(User).filter_by(email=email_address)
        ).scalar_one()
        return user

    def get_all_users(self) -> List[User]:
        users = db.session.execute(db.select(User)).scalars()
        return users

    def delete_user_by_email_address(self, email_address):
        user = db.session.execute(
            db.select(User).filter_by(email=email_address)
        ).scalar_one()
        db.session.delete(user)
        db.session.commit()

    def delete_user_by_id(self, user_id):
        user = db.session.execute(
            db.select(User).filter_by(id=user_id)
        ).scalar_one()
        db.session.delete(user)
        db.session.commit()

    def delete_all_users(self):
        db.session.query(User).delete()
        db.session.commit()

    def update_user(self, user):
        old_user = db.session.execute(
            db.select(User).filter_by(email=user.email)
        ).scalar_one()

        if user.email is not None:
            old_user.email = user.email
        if user.password is not None:
            old_user.password = user.password
        if user.is_admin is not None:
            old_user.is_admin = user.is_admin

        db.session.commit()
