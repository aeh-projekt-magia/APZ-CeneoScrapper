from typing import List, Callable

from dependency_injector.wiring import inject

from app.services.item.item_service import ItemService
from app.services.emails.email_sender import EmailSender
from app.models.SubscriptionModel import Subscription
from app.services.subscription.subscription_service import SubscriptionService


class Tasks:
    """
    Defines the repetitive, possible to schedule
    tasks executed by the application.
    """
    def __init__(self, item_service: ItemService,
                 subscription_service: SubscriptionService,
                 email_service: EmailSender):
        self.item_service = item_service
        self.subscription_service = subscription_service
        self.email_service = email_service

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

        Returns:

        """

        # init variables
        item_id_set = set()
        subs_to_update = []
        price_change_summary = {}
        print("task is working")

        # all_subscriptions = self.subscription_service.get_all_subscriptions()
        #
        # if len(all_subscriptions) == 0:
        #     return
        #
        # # filter for subscriptions that should be updated
        # for sub in all_subscriptions:
        #     if self.subscription_service.should_be_updated(sub):
        #         item_id_set.add(sub.item_id)
        #         subs_to_update.append(sub)
        #
        # # update price for all items requested
        # while len(item_id_set) != 0:
        #     item_id = item_id_set.pop()
        #     self.item_service.update_price(item_id)
        #     summary = ...  # TODO: generate a summary text for the price change
        #     price_change_summary[item_id] = summary
        #
        # # group subscriptions by user
        # subs_to_update_by_user = ...
        #
        # # send an email with a proper update to each user
        # for user_subs in subs_to_update_by_user:
        #     user_subs: List[Subscription]
        #     message = ""
        #     for sub in user_subs:
        #         if sub.notify_on_price_change:
        #             # probably a responsibility of price_hist_service
        #             # get the two latest price hist records and check if the offer
        #             # and price are the same
        #             should_update = ...
        #             if not should_update:
        #                 continue
        #         message += price_change_summary[sub.item_id]
        #     self.email_service.send_email(
        #         message=message,
        #         subject="price update",  #  TODO: the email sending service maybe should be expanded
        #         recipient=sub.user_id  # TODO: user email needed here
        #     )
