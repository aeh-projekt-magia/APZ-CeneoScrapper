import datetime
from typing import List

from app.extensions import db

from app.models.UserModel import User
from app.models.ItemModel import Item
from app.models.SubscriptionModel import Subscription
from app.repository.subscription.subscription_repository import SubscriptionRepository
from services.subscription.invalid_subscription_exception import InvalidSubscriptionException


class SubscriptionService:
    def __init__(
            self,
            subscription_repository: SubscriptionRepository
    ):
        self.subscription_repository = subscription_repository

    @staticmethod
    def __get_objects__(user_id, product_id):
        user = User.query.where(User.id == user_id).first()
        product_to_subscribe = Item.query.where(Item.id == product_id).first()
        return user, product_to_subscribe

    def add(self, user_id, item_id, notification_frequency,
            notify_on_price_change):
        subscription = Subscription(
            item_id=item_id,
            user_id=user_id,
            notification_frequency=notification_frequency,
            notify_on_price_change=notify_on_price_change,
        )
        self.subscription_repository.add_subscription(subscription)

    def remove(self, user_id, item_id):
        subscription = self.subscription_repository.get_subscription_by_item_and_user(
            item_id=item_id,
            user_id=user_id
        )
        self.subscription_repository.delete_subscription_by_id(subscription.id)

    def check_if_subscribed(self, user_id, item_id) -> bool:
        subscription = self.subscription_repository.get_subscription_by_item_and_user(
            item_id=item_id,
            user_id=user_id
        )
        return bool(subscription)

    def get_user_subscriptions(self, user_id, paginate, **kwargs):
        subscriptions = self.subscription_repository.get_subscriptions_by_user(
            user_id=user_id, paginate=paginate, **kwargs
        )
        return subscriptions

    def get_user_subscribed_items(self, user_id, item_name: str):
        user = User.query.where(User.id == user_id).first()
        items = (
            Item.query.where(User.id == user.id)
            .where(Subscription.user_id == user.id)
            .where(Subscription.item_id == Item.id)
            .filter(Item.name.like(f"%{item_name}%"))
        )
        return items

    def get_subscription_details(self, user_id, item_id):
        subscription = self.subscription_repository.get_subscription_by_item_and_user(
            item_id=item_id,
            user_id=user_id
        )
        return subscription

    def get_all_subscriptions(self) -> List[Subscription]:
        subscriptions = self.subscription_repository.get_all_subscriptions()
        return subscriptions

    def get_subscriber_email(self, subscription: Subscription) -> str:
        email = self.subscription_repository.get_subscriber_email(subscription)
        return email

    def should_be_updated(self, subscription: Subscription) -> bool:
        now = datetime.datetime.now()
        try:
            difference = now - subscription.last_notification
            if difference.days >= subscription.notification_frequency:
                return True
            return False
        except TypeError:
            subscription.last_notification = now
            self.subscription_repository.update_subscription(subscription)
            raise InvalidSubscriptionException(
                "The subscription data is incorrect. Please"
                " verify the notification frequency"
            )

    @staticmethod
    def update_subscription(subscription: Subscription, update: dict):
        try:
            subscription.notification_frequency = int(update["notification_frequency"])
            subscription.notify_on_price_change = (
                True if update["notify_on_price_change"] == "Yes" else False
            )
            subscription.send_notification = (
                True if update["send_notification"] == "Yes" else False
            )
        except Exception as e:
            db.session.rollback()
        else:
            db.session.commit()
