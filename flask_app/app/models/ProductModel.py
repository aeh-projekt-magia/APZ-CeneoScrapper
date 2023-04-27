from dataclasses import dataclass
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship, mapped_column
from flask_login import UserMixin

from app.extensions import db, bcrypt



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

    # children = relationship('Reviews', back_populates='parent')

    # subscribers = relationship('User', secondary=user_product_subscription2, back_populates='subscriptions')

    def __repr__(self):
        return f'<id {self.id}> <name {self.name}> <subscribers {self.name}>'