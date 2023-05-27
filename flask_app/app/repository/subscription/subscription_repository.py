from abc import ABC, abstractmethod

from app.models.SubscriptionModel import Subscription
from app.extensions import db
from app.repository.base_repository import BaseRepository


class SubscriptionRepository(BaseRepository, ABC):
    @abstractmethod
    def add_subscription(self, subscription: Subscription):
        ...
        # db.session.add(subscription)
        # db.session.commit()

    @abstractmethod
    def get_subscription_by_id(self, subscription_id):
        ...

    @abstractmethod
    def get_subscription_by_item_and_user(self, item_id, user_id):
        ...

    @abstractmethod
    def get_subscriptions_by_user(self, user_id, paginate: bool, **kwargs):
        ...

    @abstractmethod
    def user_subscribed_items_query(self, user_id, item_name: str):
        ...

    @abstractmethod
    def get_subscriber_email(self, subscription: Subscription) -> str:
        ...

    @abstractmethod
    def get_all_subscriptions(self):
        ...

    @abstractmethod
    def delete_subscription_by_id(self, subscription_id):
        ...

    @abstractmethod
    def delete_all_subscriptions(self):
        ...

    @abstractmethod
    def update_subscription(self, subscription: Subscription):
        ...
