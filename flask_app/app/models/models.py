from dataclasses import dataclass
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship, mapped_column
from flask_login import UserMixin

from app.extensions import db, bcrypt

user_product_subscription = db.Table('user_product_subscription',
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('product_id', Integer, ForeignKey('products_table.id'))
)

class User(db.Model, UserMixin) :
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)

    subscriptions = relationship('Products', secondary=user_product_subscription, back_populates='subscribers')

    def __init__(self, email, password, is_admin=False, is_confirmed=False):
        self.email = email
        # Important thing, to decode bytes to string before pushing to psql
        # Or, we can also change column type to bytes/binary
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.created_on = datetime.now()
        self.is_admin = is_admin
        self.is_confirmed = is_confirmed

    def __repr__(self):
        return f"<id {self.id}> <email {self.email}> <subscriptions {self.subscriptions}>"


class Products(db.Model):
    __tablename__ = "products_table"    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    category = Column(String)
    price = Column(String)
    available_shops_count = Column(String)
    reviews_count = Column(String)
    description = Column(String)
    image_url = Column(String)

    children = relationship('Reviews', back_populates='parent')

    subscribers = relationship('User', secondary=user_product_subscription, back_populates='subscriptions')

    def __repr__(self):
        return f'<id {self.id}> <name {self.name}> <subscribers {self.name}>'




# class UserSubscription(db.Model):
#     __tablename__ = "users_subscriptions"
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     product_id = Column(Integer, ForeignKey('products_table.id'))


class Reviews(db.Model):
    __tablename__ = "reviews_table"    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    stars = Column(String)
    description = Column(String)
    zalety = Column(String)
    wady = Column(String)
    recommendation = Column(String)
    date = Column(String)

    parent_id = mapped_column(ForeignKey('products_table.id'))
    parent = relationship('Products', back_populates='children')

    def __init__(self,name,stars, description, zalety : list, wady :list, recommendation, date, parent_id = None, parent = None) -> None:
        self.name = name
        self.stars = stars
        self.description = description
        self.zalety = ';'.join(zalety)
        self.wady = ';'.join(wady)
        self.reccomendation = recommendation
        self.date = date
        self.parent_id = parent_id
        self.parent = parent

    def __repr__(self):
        return f'{self.id} {self.name} {self.stars}'






class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Text)
    # recommendation = db.Column(db.Text)
    # stars = db.Column(db.Text)
    # content = db.Column(db.Text)
    # publish_date = db.Column(db.Text)
    # purchase_date = db.Column(db.Text)
    # useful = db.Column(db.Text)
    # useless = db.Column(db.Text)
    # pros = db.Column(db.Text)
    # cons = db.Column(db.Text)
    # review_id = db.Column(db.Text)

    # product_id = db.Column(db.Text, db.ForeignKey('product.id'))

    # def __repr__(self):
    #     return f'<Review no {self.review_id}: {self.author} - {self.content}>'

