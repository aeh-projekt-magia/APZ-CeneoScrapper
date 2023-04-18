from app.extensions import db
from dataclasses import dataclass
from app.models.ItemModel import Item
from app.models.UserModel import User

@dataclass
class Subscription(db.Model):

    __tablename__ = "subscriptions"

    subscription_id: int
    item_id: int
    user_id: int
    notification_frequency: int
    notify_on_price_change: bool
    send_notification: bool

    subscription_id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.item_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    notification_frequency = db.Column(db.Integer, default = 0)
    notify_on_price_change = db.Column(db.Boolean, default = False)
    send_notification = db.Column(db.Boolean, default = False)

    def __init__(self, itemId, userId, notificationFreq,notifyOnPriceChange):
        self.item_id = itemId
        self.user_id = userId
        self.notification_frequency = notificationFreq
        self.notify_on_price_change = notifyOnPriceChange
    
    def __str__(self):
        return (str(self.subscription_id) + " " + str(self.item_id) + " " + 
                str(self.user_id) + " " + str(self.notification_frequency) + " " +
                str(self.notify_on_price_change) + " " + str(self.send_notification))