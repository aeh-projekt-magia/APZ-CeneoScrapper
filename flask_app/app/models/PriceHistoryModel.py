from app.extensions import db
import datetime

class PriceHistory(db.Model):

    __tablename__ = "price_history"

    price_id: int
    item_id: int
    price: float
    date: datetime

    price_id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('Item.item_id'))
    price = db.Column(db.Numeric(10,2), default = 0.00)
    date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, itemId, price):
        self.item_id= itemId
        self.price = price

    def __str__(self):
        return (str(self.price_id) + " " + self.item_id + " " + 
                str(self.price) + " " + str(self.date))