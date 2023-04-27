from app import db

from app.models.UserModel import User
from app.models.ItemModel import Item


class ProductSubscription:
    @staticmethod
    def __get_objects__(user_id, product_id):
        user = db.session.query(User).where(User.id == user_id).first()
        product_to_subscribe = (
            db.session.query(Item).where(Item.id == product_id).first()
        )
        return user, product_to_subscribe

    @staticmethod
    def add(user_id, product_id):
        user, product_to_subscribe = ProductSubscription.__get_objects__(
            user_id, product_id
        )

        user.subscriptions.append(product_to_subscribe)
        db.session.commit()

    @staticmethod
    def remove(user_id, product_id):
        user, product_to_subscribe = ProductSubscription.__get_objects__(
            user_id, product_id
        )

        user.subscriptions.remove(product_to_subscribe)
        db.session.commit()

    @staticmethod
    def get(user_id, product_id) -> bool:
        user, product = ProductSubscription.__get_objects__(user_id, product_id)

        return any(subscription.id == product.id for subscription in user.subscriptions)
