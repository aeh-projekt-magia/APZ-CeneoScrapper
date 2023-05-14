from dependency_injector.wiring import Provide

from app.containers import Container
from app.services.item.item_service import ItemService
from services.subscription.subscription_service import SubscriptionService


def update_subscribers(
        item_service: ItemService = Provide[Container.item_service],
        subscription_service: SubscriptionService = Provide[
            Container.subscription_service],

):
    ...
