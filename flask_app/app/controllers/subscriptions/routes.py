from flask import render_template
from flask_login import login_required, current_user
from app.controllers.subscriptions import bp
from app.services.subscription.subscription_service import SubscriptionService
from app.services.decorators import confirmed_user_required

from app.services.item.product_service import ItemService


@bp.route("/", methods=["GET", "POST"])
@login_required
@confirmed_user_required
def index():
    """Wyświetlenie zasubskrybowanych produktów"""
    # TODO:subscriptions/routes - Dodać repozytorium
    products_to_show = SubscriptionService.get_user_subscriptions(
        user_id=current_user.id
    )
    return render_template("subscriptions/index.html", products=products_to_show)


@bp.route("/<int:product_id>", methods=["GET", "POST"])
@login_required
@confirmed_user_required
def single_subscription_view(product_id):
    """Wyświetlenie konkretnego zasubskrybowanego do tej pory produktu"""

    if not SubscriptionService.check_if_subscribed(
        user_id=current_user.id, product_id=product_id
    ):
        return render_template("errors/404.html")

    product = ItemService.get_product_to_show_by_id(id=product_id)
    product_price_history = product.price_history
    subscription = SubscriptionService.get_subscription_details(
        user_id=current_user.id, product_id=product_id
    )

    return render_template(
        "subscriptions/single_subscription.html",
        product=product,
        subscription=subscription,
        price_history=product_price_history,
    )
