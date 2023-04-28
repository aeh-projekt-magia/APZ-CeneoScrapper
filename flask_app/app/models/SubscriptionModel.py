from app.extensions import db
from dataclasses import dataclass


# TODO: Dodac uniquecostam
#  UniqueConstraint('uid', 'role', name='idx_uid_role'))
@dataclass
class Subscription(db.Model):
    __tablename__ = "subscriptions_table"

    id: int
    item_id: int
    user_id: int
    notification_frequency: int
    notify_on_price_change: bool
    send_notification: bool

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    notification_frequency = db.Column(db.Integer, default=0)
    notify_on_price_change = db.Column(db.Boolean, default=False)
    send_notification = db.Column(db.Boolean, default=False)

    def __init__(self, itemId, userId, notificationFreq, notifyOnPriceChange):
        self.item_id = itemId
        self.user_id = userId
        self.notification_frequency = notificationFreq
        self.notify_on_price_change = notifyOnPriceChange

    def __repr__(self):
        return f"{self.id=}\
                {self.item_id=}\
                {self.user_id=}\
                {self.notification_frequency=}\
                {self.notify_on_price_change=}\
                {self.send_notification=}"
