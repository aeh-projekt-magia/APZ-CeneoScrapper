from dataclasses import dataclass
from datetime import datetime

from flask_login import UserMixin

from app.extensions import db, bcrypt

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    name = db.Column(db.Text)
    review = db.relationship('Review', backref='product')

    def __repr__(self):
        return f'{self.id} {self.product_id} {self.name} {self.review}'


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
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

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    def __repr__(self):
        return f'<Review no {self.review_id}: {self.author} - {self.content}>'

