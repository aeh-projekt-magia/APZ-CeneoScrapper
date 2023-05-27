from collections import defaultdict
from typing import List, Callable

from app.services.item.item_service import ItemService
from app.services.emails.email_sender import EmailSender
from app.models.SubscriptionModel import Subscription
from app.services.subscription.subscription_service import SubscriptionService
from app.services.price_history.price_history_service import PriceHistoryService
from app.repository.user.user_repository import UserRepository


class Tasks:
    """
    Defines the repetitive, possible to schedule
    tasks executed by the application.
    """

    def __init__(
            self,
            item_service: ItemService,
            subscription_service: SubscriptionService,
            email_service: EmailSender,
            price_history_service: PriceHistoryService,
            user_repository: UserRepository
    ):
        self.item_service = item_service
        self.subscription_service = subscription_service
        self.email_service = email_service
        self.price_history_service = price_history_service
        self.user_repository = user_repository

    def get_tasks(self) -> list[Callable]:
        """
        Retrieve all tasks defined in the class that should be
        regularly executed by the application.
        Returns:
            List of methods to be considered as tasks
        """
        return [
            self.update_subscribers,
        ]

    def update_subscribers(self):
        """
        Check for subscriptions that should be updated, group them by users
        and send a proper summary to each user.
        """

        # init variables
        item_id_set = set()
        subs_to_update = []
        price_change_summary = {}

        all_subscriptions = self.subscription_service.get_all_subscriptions()

        if len(all_subscriptions) == 0:
            return

        # filter for subscriptions that should be updated
        for sub in all_subscriptions:
            if self.subscription_service.should_be_updated(sub):
                item_id_set.add(sub.item_id)
                subs_to_update.append(sub)

        # update price for all items requested
        while len(item_id_set) != 0:
            item_id = item_id_set.pop()
            self.item_service.update_price(item_id)
            summary = self.price_history_service.compare_two_latest(item_id)
            price_change_summary[item_id] = summary

        # group subscriptions by user
        subs_to_update_by_user = defaultdict(list)
        for sub in subs_to_update:
            subs_to_update_by_user[sub.user_id].append(sub)

        # send an email with a proper update to each user
        for user_id in subs_to_update_by_user:
            user_subs: List[Subscription] = subs_to_update_by_user[user_id]
            email_address = self.user_repository.get_user_by_id(user_id).email
            message = ""
            for sub in user_subs:
                summary, has_changed = price_change_summary[sub.item_id]
                if sub.notify_on_price_change and not has_changed:
                    continue
                message += summary + "\n"
            self.email_service.send_email(
                message=message,
                subject="price update",
                recipient=email_address
            )
