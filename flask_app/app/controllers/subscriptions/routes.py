from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app.controllers.subscriptions import bp
from app.services.subscription_service import SubscriptionService
from app.services.decorators import confirmed_user_required
from app.services.forms import SubscriptionUpdate
from app.services.product_service import ProductService


@bp.route("/", methods=["GET"])
@login_required
@confirmed_user_required
def index():
    """Wyświetlenie zasubskrybowanych produktów"""
    # TODO:subscriptions/routes - Dodać repozytorium
    page = request.args.get("page", 1, type=int)
    
    products_to_show = SubscriptionService.get_user_subscriptions_paginate(
        user_id=current_user.id, page=page, pages=15)

            
    return render_template("subscriptions/index.html", products=products_to_show)


@bp.route("/<int:product_id>", methods=["GET"])
@login_required
@confirmed_user_required
def single_subscription_view(product_id):
    """Wyświetlenie konkretnego zasubskrybowanego do tej pory produktu"""

    if not SubscriptionService.check_if_subscribed(
        user_id=current_user.id, product_id=product_id
    ):
        return render_template("errors/404.html")

    product = ProductService.get_product_to_show_by_id(id=product_id)
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

@bp.route("/<int:product_id>/update", methods=["GET", "POST"])
@login_required
@confirmed_user_required
def single_subscription_update(product_id):

    if not SubscriptionService.check_if_subscribed(
        user_id=current_user.id, product_id=product_id
    ):
        return render_template("errors/404.html")

    product = ProductService.get_product_to_show_by_id(id=product_id)
    product_price_history = product.price_history
    subscription = SubscriptionService.get_subscription_details(
        user_id=current_user.id, product_id=product_id
    )

    # Create default values for form fields
    form = SubscriptionUpdate(
        notification_frequency = subscription.notification_frequency, 
        notify_on_price_change="Yes" if subscription.notify_on_price_change else "No",
        send_notification="Yes" if subscription.send_notification else "No"
    )
    if request.method == "POST":
        if form.validate_on_submit():
            SubscriptionService.update_subscription(subscription=subscription, update={
                "notification_frequency":form.notification_frequency.data,
                "notify_on_price_change": form.notify_on_price_change.data,
                "send_notification":form.send_notification.data})
            return redirect(url_for("subscriptions.single_subscription_view", product_id=product_id))


    return render_template(
        "subscriptions/single_subscription_update.html",
        product=product,
        subscription=subscription,
        price_history=product_price_history, 
        form=form
    )