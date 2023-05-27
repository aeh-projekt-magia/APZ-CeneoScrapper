from dependency_injector.wiring import Provide, inject
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app.controllers.subscriptions import bp
from app.services.subscription.subscription_service import SubscriptionService
from app.services.decorators import confirmed_user_required
from app.services.forms import SubscriptionUpdate
from app.services.item.item_service import ItemService
from app.containers import Container


@bp.route("/", methods=["GET"])
@login_required
@confirmed_user_required
@inject
def index(
        subscription_service: SubscriptionService = Provide[Container.subscription_service]
):
    """Wyświetlenie zasubskrybowanych produktów"""
    # TODO:subscriptions/routes - Dodać repozytorium

    page = request.args.get("page", 1, type=int)

    query_name = request.args.get("query_name")
    if query_name is None or query_name == "":
        products_to_show = subscription_service.get_user_subscriptions(
            user_id=current_user.id, paginate=True, per_page=25, page=page
        )
    else:
        products_to_show = subscription_service.get_user_subscribed_items(
            user_id=current_user.id, item_name=query_name
        ).paginate(page=page, per_page=25)

    return render_template("subscriptions/index.html", products=products_to_show)


@bp.route("/<int:product_id>", methods=["GET"])
@login_required
@confirmed_user_required
@inject
def single_subscription_view(
        product_id,
        item_service: ItemService = Provide[Container.item_service],
        subscription_service: SubscriptionService = Provide[Container.subscription_service]
):
    """Wyświetlenie konkretnego zasubskrybowanego do tej pory produktu"""

    if not subscription_service.check_if_subscribed(
        user_id=current_user.id, item_id=product_id
    ):
        return render_template("errors/404.html")

    product = item_service.get_product_to_show_by_id(item_id=product_id)
    product_price_history = product.price_history
    subscription = subscription_service.get_subscription_details(
        user_id=current_user.id, item_id=product_id
    )

    return render_template(
        "subscriptions/single_subscription.html",
        product=product,
        subscription=subscription,
        price_history=product_price_history,
    )


@bp.route("/<int:product_id>/update", methods=["GET", "POST"])
@login_required
@confirmed_user_required
@inject
def single_subscription_update(
    product_id, item_service: ItemService = Provide[Container.item_service],
    subscription_service: SubscriptionService = Provide[Container.subscription_service]
):

    # If item is not subscribed, return 404

    if not subscription_service.check_if_subscribed(
        user_id=current_user.id, item_id=product_id

    ):
        return render_template("errors/404.html")

    product = item_service.get_product_to_show_by_id(item_id=product_id)
    product_price_history = product.price_history
    subscription = subscription_service.get_subscription_details(
        user_id=current_user.id, item_id=product_id
    )

    # Create default values for form fields
    form = SubscriptionUpdate(
        notification_frequency=subscription.notification_frequency,
        notify_on_price_change="Yes" if subscription.notify_on_price_change else "No",
    )
    if request.method == "POST":
        if form.validate_on_submit():
            subscription_service.update_subscription(
                subscription=subscription,
                update={
                    "notification_frequency": form.notification_frequency.data,
                    "notify_on_price_change": form.notify_on_price_change.data,
                },
            )
            return redirect(
                url_for("subscriptions.single_subscription_view", product_id=product_id)
            )

    return render_template(
        "subscriptions/single_subscription_update.html",
        product=product,
        subscription=subscription,
        price_history=product_price_history,
        form=form,
    )
