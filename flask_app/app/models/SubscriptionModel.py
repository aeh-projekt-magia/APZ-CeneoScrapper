import datetime

from app.extensions import db
from dataclasses import dataclass


# TODO: Dodac uniquecostam
#  UniqueConstraint('uid', 'role', name='idx_uid_role'))
@dataclass
class Subscription(db.Model):
    __tablename__ = "subscriptions_table"

    id: int
    item_id: str
    user_id: int
    notification_frequency: int
    notify_on_price_change: bool
    last_notification: datetime

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    notification_frequency = db.Column(db.Integer, default=0)
    notify_on_price_change = db.Column(db.Boolean, default=False)
    last_notification = db.Column(db.DateTime, default=datetime.datetime.now)
    """Relationships"""
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))

    def __init__(
        self,
        item_id,
        user_id,
        notification_frequency=0,
        notify_on_price_change=False,
        last_notification=datetime.datetime.now(),

    ):
        self.item_id = item_id
        self.user_id = user_id
        self.notification_frequency = notification_frequency
        self.notify_on_price_change = notify_on_price_change

    def __repr__(self):
        return f"{self.id=}\
                {self.item_id=}\
                {self.user_id=}\
                {self.notification_frequency=}\
                {self.notify_on_price_change=}\
                {self.last_notification=}"
