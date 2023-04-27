from app.extensions import db
import datetime
from dataclasses import dataclass

from sqlalchemy import Integer
from sqlalchemy.orm import relationship
from app.models.relations import user_product_subscription


@dataclass
class Item(db.Model):
    __tablename__ = "items"

    name = str
    is_available = str

    id = db.Column(Integer, primary_key=True)
    name = db.Column(db.String, default="")
    category = db.Column(db.String)
    price = db.Column(db.String)
    available_shops_count = db.Column(db.String)
    reviews_count = db.Column(db.String)
    description = db.Column(db.String)
    image_url = db.Column(db.String)

    is_available = db.Column(db.Boolean, default=False)
    lowest_price = db.Column(db.Numeric(10, 2), default=0.00)
    offer_url = db.Column(db.String, default="")
    last_updated = db.Column(db.DateTime, default=datetime.datetime.now)

    """Relations"""
    subscribers = relationship(
        "User", secondary=user_product_subscription, back_populates="subscriptions"
    )

    def __repr__(self):
        return f"{self.id=}\
                {self.name=}\
                {self.is_available=}\
                {self.lowest_price=} \
                {self.offer_url=}\
                {self.last_updated=}"
