from app.services.item.item_service import ItemService
from app.services.emails.email_sender import EmailSender
from app.services.subscription.subscription_service import SubscriptionService


def update_subscribers(
        item_service: ItemService,
        subscription_service: SubscriptionService,
        email_service: EmailSender
):
    # init variables
    item_id_set = set()
    subs_to_update = []
    price_change_summary = {}
    print("task is working")
    #
    # all_subscriptions = subscription_service.get_all_subscriptions()
    #
    # if len(all_subscriptions) == 0:
    #     return
    #
    # # filter for subscriptions that should be updated
    # for sub in all_subscriptions:
    #     if subscription_service.should_be_updated(sub):
    #         item_id_set.add(sub.item_id)
    #         subs_to_update.append(sub)
    #
    # # update price for all items requested
    # while len(item_id_set) != 0:
    #     item_id = item_id_set.pop()
    #     item_service.update_price(item_id)
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
    #     email_service.send_email(
    #         message=message,
    #         subject="price update",  #  TODO: the email sending service maybe should be expanded
    #         recipient=sub.user_id  # TODO: user email needed here
    #     )

