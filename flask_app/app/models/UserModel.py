from app.extensions import db, bcrypt
import datetime
from dataclasses import dataclass
from flask_login import UserMixin
from sqlalchemy import Integer
from sqlalchemy.orm import relationship

from app.models.SubscriptionModel import Subscription

"""This table has to be created first"""
Subscription.__tablename__


@dataclass
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id: int
    email: str
    password: str
    is_admin: bool
    created_on: datetime

    id = db.Column(Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    created_on = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)

    """Relations"""
    subscriptions = relationship(
        "Item", secondary="subscriptions_table", back_populates="subscribers"
    )

    def __init__(self, email, password, is_admin=False, is_confirmed=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")
        self.is_admin = is_admin
        self.is_confirmed = is_confirmed

    def __repr__(self):
        return f"{self.id=} {self.email=}"

    # TODO: model repr? zostawic?
    def __str__(self):
        return (
            str(self.id)
            + " "
            + self.email
            + " "
            + str(self.password)
            + " "
            + str(self.is_admin)
            + " "
            + str(self.created_on)
        )
