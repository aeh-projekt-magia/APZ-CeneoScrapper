from app.extensions import db
import datetime
from dataclasses import dataclass

@dataclass
class Item(db.Model):

    __tablename__ = "item"
    
    item_id: int
    item_name: str
    is_available: bool
    lowest_price: float
    offer_url: str
    last_updated: datetime

    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.Text, default="")
    is_available = db.Column(db.Boolean, default=False)
    lowest_price = db.Column(db.Numeric(10,2), default = 0.00)
    offer_url = db.Column(db.Text, default = "")
    last_updated = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, itemId, itemName, isAvailable, lowestPrice, offerUrl):
        self.item_id = itemId
        self.item_name = itemName
        self.is_available = isAvailable
        self.lowest_price = lowestPrice
        self.offer_url = offerUrl
        
    def __str__(self):
        return (str(self.item_id) + " " + self.item_name + " " + 
                str(self.is_available) + " " + str(self.lowest_price) + " " + 
                    self.offer_url + " " + str(self.last_updated))


#created_date = DateTime(default=datetime.datetime.utcnow)