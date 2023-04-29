from app.extensions import db
import datetime
from dataclasses import dataclass


@dataclass
class PriceHistory(db.Model):
    __tablename__ = "price_history"

    price_id: int
    item_id: int
    price: float
    date: datetime

    price_id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    price = db.Column(db.Numeric(10, 2), default=0.00)
    date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, itemId, price, date=None):
        self.item_id = itemId
        self.price = price
        self.date = date

    def __repr__(self):
        (
            str(self.price_id)
            + " "
            + str(self.item_id)
            + " "
            + str(self.price)
            + " "
            + str(self.date)
        )
        return f"{self.price_id=} \
                {self.item_id=}\
                {self.price=}\
                {self.date=}"
