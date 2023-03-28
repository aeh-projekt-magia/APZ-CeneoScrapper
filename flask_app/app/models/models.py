from dataclasses import dataclass
from datetime import datetime

from flask_login import UserMixin

from app.extensions import db, bcrypt


@dataclass
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id: int
    email: str
    password: str
    created_on: datetime
    is_admin: bool

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, is_admin=False, is_confirmed=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.created_on = datetime.now()
        self.is_admin = is_admin
        self.is_confirmed = is_confirmed

    def __repr__(self):
        return f"<email {self.email}>"


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Text)
    name = db.Column(db.Text)
    review = db.relationship('Review', backref='product')

    def __repr__(self):
        return f'{self.id} {self.product_id} {self.name} {self.review}'


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Text)
    recommendation = db.Column(db.Text)
    stars = db.Column(db.Text)
    content = db.Column(db.Text)
    publish_date = db.Column(db.Text)
    purchase_date = db.Column(db.Text)
    useful = db.Column(db.Text)
    useless = db.Column(db.Text)
    pros = db.Column(db.Text)
    cons = db.Column(db.Text)
    review_id = db.Column(db.Text)

    product_id = db.Column(db.Text, db.ForeignKey('product.id'))

    def __repr__(self):
        return f'<Review no {self.review_id}: {self.author} - {self.content}>'


class Country(db.Model):
    __tablename__ = 'countries'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    cities = db.relationship('City', back_populates = 'country',
lazy = True)
class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'))
    country = db.relationship('Country', back_populates = 'cities')