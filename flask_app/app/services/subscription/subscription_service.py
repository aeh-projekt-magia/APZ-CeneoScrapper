from typing import List

from app.extensions import db

from app.models.UserModel import User
from app.models.ItemModel import Item
from app.models.SubscriptionModel import Subscription


class SubscriptionService:
    @staticmethod
    def __get_objects__(user_id, product_id):
        user = User.query.where(User.id == user_id).first()
        product_to_subscribe = Item.query.where(Item.id == product_id).first()
        return user, product_to_subscribe

    @staticmethod
    def add(user_id, product_id):
        user, product_to_subscribe = SubscriptionService.__get_objects__(
            user_id, product_id
        )

        # user.subscriptions.append(product_to_subscribe)  # LUB!
        db.session.add(Subscription(item_id=product_id, user_id=user_id))
        db.session.commit()

    @staticmethod
    def remove(user_id, product_id):
        user, product_to_subscribe = SubscriptionService.__get_objects__(
            user_id, product_id
        )

        sub = Subscription.query.filter_by(user_id=user_id, item_id=product_id).first()
        db.session.delete(sub)
        db.session.commit()

    @staticmethod
    def check_if_subscribed(user_id, product_id) -> bool:
        user, product = SubscriptionService.__get_objects__(user_id, product_id)

        return any(subscription.id == product.id for subscription in user.subscriptions)

    @staticmethod
    def get_user_subscriptions(user_id):
        user = User.query.where(User.id == user_id).first()
        return user.subscriptions

    @staticmethod
    def get_subscription_details(user_id, product_id):
        return Subscription.query.filter_by(user_id=user_id, item_id=product_id)

    def get_all_subscriptions(self) -> List[Subscription]:
        ...

    def should_be_updated(self, subscription: Subscription) -> bool:
        ...
