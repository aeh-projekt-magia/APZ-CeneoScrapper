from app.extensions import db
import datetime
from dataclasses import dataclass
from sqlalchemy.orm import relationship


@dataclass
class PriceHistory(db.Model):
    __tablename__ = "price_history"

    price_id: int
    item_id: int
    price: float
    date: datetime

    price_id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Numeric(10, 2), default=0.00)
    date = db.Column(db.DateTime, default=datetime.datetime.now)

    """Relationships"""
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    item = relationship("Item", back_populates="price_history")

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
