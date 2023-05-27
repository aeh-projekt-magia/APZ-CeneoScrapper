from app.extensions import db
import datetime
from dataclasses import dataclass

from sqlalchemy import Integer
from app.models.SubscriptionModel import Subscription


f"""This table has to be created first 
{Subscription.__tablename__}"""


@dataclass
class Item(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
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
    subscribers = db.relationship(
        "User",
        secondary="subscriptions_table",
        back_populates="subscriptions",
        lazy="dynamic",
    )
    price_history = db.relationship(
        "PriceHistory", back_populates="item", lazy="dynamic"
    )

    def __init__(
        self,
        item_id=None,
        name=None,
        lowest_price=None,
        available_shops_count=None,
        reviews_count=None,
        description=None,
        image_url=None,
        category=None,
        is_available=None,
        offer_url=None,
    ):
        if item_id is None:
            pass
        else:
            self.id = item_id
        self.name = name
        self.lowest_price = lowest_price
        self.available_shops_count = available_shops_count
        self.reviews_count = reviews_count
        self.description = description
        self.image_url = image_url
        self.category = category
        self.offer_url = offer_url
        self.is_available = is_available

    def __repr__(self):
        return f"{self.id=}\
                {self.name=}\
                {self.is_available=}\
                {self.lowest_price=} \
                {self.offer_url=}\
                {self.last_updated=}"
