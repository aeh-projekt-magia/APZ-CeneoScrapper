from dependency_injector.wiring import inject, Provide
from flask import flash, render_template, request, redirect, url_for
from flask_login import current_user, login_required

from app.controllers.products import bp
from app.services.decorators import confirmed_user_required
from app.services.forms import SubscribeProductForm

from app.services.subscription.subscription_service import SubscriptionService
from app.services.item.item_service import ItemService
from app.containers import Container


@bp.route("/", methods=["GET"])
@login_required
@confirmed_user_required
@inject
def index(item_service: ItemService = Provide[Container.item_service]):
    """Wyświetlenie pobranych do tej pory produktów"""

    page = request.args.get("page", 1, type=int)

    query_name_ceneo = request.args.get("query_name_ceneo")

    # Show products from database
    if query_name_ceneo is None or query_name_ceneo == "":
        products_to_show = item_service.get_all_products_to_show_paginate(
            page=page, pages=25
        )

    else:
        products_to_show = item_service.get_all_products_to_show_by_name(
            item_name=query_name_ceneo
        ).paginate(page=page, per_page=25)

    # Query products from ceneo by name
    if query_name_ceneo is not None and query_name_ceneo != "":
        try:
            item_service.fetch_item(item_name=query_name_ceneo)
            flash("Success", "success")

        except Exception as e:
            print(e)
            flash("There is a problem", "error")

        return redirect(url_for("products.index"))

    return render_template("products/index.html", products=products_to_show)


@bp.route("/<int:product_id>", methods=["GET", "POST"])
@login_required
@confirmed_user_required
@inject
def single_product_view(
    product_id,
    item_service: ItemService = Provide[Container.item_service],
    subscription_service: SubscriptionService = Provide[Container.subscription_service],
):
    """Wyświetlenie konkretnego pobranego do tej pory produktu"""

    """Subscribe or unsubscribe request handling"""
    form = SubscribeProductForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            if form.subscribe_button.data:
                subscription_service.add(user_id=current_user.id, item_id=product_id)
                is_already_subscribed = True
                flash("Product subscribed", "success")
            elif form.unsubscribe_button.data:
                subscription_service.remove(user_id=current_user.id, item_id=product_id)
                is_already_subscribed = False
                flash("Product unsubscribed", "success")
            return redirect(
                url_for("products.single_product_view", product_id=product_id)
            )

    tab = None
    product_to_show = item_service.get_product_to_show_by_id(product_id)
    is_already_subscribed = subscription_service.check_if_subscribed(
        user_id=current_user.id, item_id=product_id
    )

    return render_template(
        "products/single_product.html",
        product=product_to_show,
        tab=tab,
        form=form,
        is_already_subscribed=is_already_subscribed,
    )
