from app.models.SubscriptionModel import Subscription
from app.extensions import db
from app.models.UserModel import User
from app.repository.subscription.subscription_repository import SubscriptionRepository
from app.models.ItemModel import Item


class ImplSubscriptionRepository(SubscriptionRepository):

    def add_subscription(self, subscription: Subscription):
        db.session.add(subscription)
        db.session.commit()

    def get_subscription_by_id(self, subscription_id):
        subscription = db.session.execute(
            db.select(Subscription).filter_by(id=subscription_id)
        ).scalar_one()
        return subscription

    def get_subscription_by_item_and_user(self, item_id, user_id):
        subscription = db.session.execute(
            db.select(Subscription).filter_by(
                user_id=user_id, item_id=item_id
            )
        ).scalar_one_or_none()
        return subscription

    def get_subscriptions_by_user(self, user_id, paginate: bool = False, **kwargs):
        per_page = kwargs.get("per_page", 25)
        page = kwargs.get("page", None)
        select = db.select(Subscription).filter_by(
                user_id=user_id
        )
        if paginate:
            subscriptions = db.paginate(
                select=select,
                page=page,
                per_page=per_page
            )
            return subscriptions

        subscriptions = db.session.execute(
            select
        ).scalars().all()
        return subscriptions

    def user_subscribed_items_query(self, user_id, item_name: str):
        user = User.query.where(User.id == user_id).first()
        query = (
            Item.query.where(User.id == user.id)
            .where(Subscription.user_id == user.id)
            .where(Subscription.item_id == Item.id)
        )
        if item_name:
            query = query.filter(Item.name.ilike(f"%{item_name}%"))
        return query

    def get_subscriber_email(self, subscription: Subscription) -> str:
        user = db.session.execute(
            db.select(User).filter_by(
                user_id=subscription.user_id
            )
        ).scalar_one_or_none()
        if user:
            return user.email
        return None

    def get_all_subscriptions(self):
        subscriptions = db.session.execute(db.select(Subscription)).scalars().all()
        return subscriptions

    def delete_subscription_by_id(self, subscription_id):
        subscription = db.session.execute(
            db.select(Subscription).filter_by(id=subscription_id)
        ).scalar_one()
        db.session.delete(subscription)
        db.session.commit()

    def delete_all_subscriptions(self):
        db.session.query(Subscription).delete()
        db.session.commit()

    def update_subscription(self, subscription: Subscription):
        old_subscription: Subscription = db.session.execute(
            db.select(Subscription).filter_by(id=subscription.id)
        ).scalar_one()

        if subscription.last_notification is not None:
            old_subscription.last_notification = subscription.last_notification
        if subscription.notify_on_price_change is not None:
            old_subscription.notify_on_price_change = subscription.notify_on_price_change
        if subscription.notification_frequency is not None:
            old_subscription.notification_frequency = subscription.notification_frequency
        if subscription.item_id is not None:
            old_subscription.item_id = subscription.item_id

        db.session.commit()
