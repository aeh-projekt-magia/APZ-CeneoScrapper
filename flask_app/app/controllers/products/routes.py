from dependency_injector.wiring import inject, Provide
from flask import flash, render_template, request, redirect, url_for
from flask_login import current_user, login_required

from app.controllers.products import bp
from app.services.decorators import confirmed_user_required
from app.services.forms import SubscribeProductForm

from app.services.subscription.subscription_service import SubscriptionService
from app.services.item.item_service import ItemService
from app.containers import Container
from app.services.ceneo.ceneo_item import CeneoItem


@bp.route("/", methods=["GET"])
@login_required
@confirmed_user_required
@inject
def index(item_service: ItemService = Provide[Container.item_service]):
    """Wyświetlenie pobranych do tej pory produktów"""
    # TODO: products/routes - Dodać obsługę repozytorium

    page = request.args.get("page", 1, type=int)

    query_name = request.args.get("query_name")
    query_name_ceneo = request.args.get("query_name_ceneo")
    query_id_ceneo = request.args.get("query_id_ceneo")

    # Query products from ceneo by name
    if query_name_ceneo is not None and query_name_ceneo != "":
        ceneo_item = CeneoItem()
        try:
            item_by_name = ceneo_item.find_id_by_item_name(
                item_name=str(query_name_ceneo)
            )
        except Exception as e:
            print(e)
            return {"query_result": "Error"}

        return {"query_result": item_by_name}
    # Query products from ceneo by id
    if query_id_ceneo is not None and query_id_ceneo != "":
        # ceneo_item = CeneoItem()

        # try:
        #     item_by_id = ceneo_item.fetch_lowest_price(item_id=str(query_id_ceneo))
        # except Exception as e:
        #     print(e)
        #     return {"query_result": "Error"}
        item_service.fetch_item(item_name=query_id_ceneo)

        return {"query_result": 'ok'}

    # Quering products from database by name or
    # all products if name is not provided or empty
    if query_name is None or query_name == "":
        products_to_show = item_service.get_all_products_to_show_paginate(
            page=page, pages=25
        )
    else:
        products_to_show = item_service.get_all_products_to_show_by_name(
            item_name=query_name
        ).paginate(page=page, per_page=25)

    return render_template("products/index.html", products=products_to_show)


@bp.route("/<int:product_id>", methods=["GET", "POST"])
@login_required
@confirmed_user_required
@inject
def single_product_view(
    product_id, item_service: ItemService = Provide[Container.item_service]
):
    """Wyświetlenie konkretnego pobranego do tej pory produktu"""

    """Subscribe or unsubscribe request handling"""
    form = SubscribeProductForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            if form.subscribe_button.data:
                SubscriptionService.add(user_id=current_user.id, product_id=product_id)
                is_already_subscribed = True
                flash("Product subscribed", "success")
            elif form.unsubscribe_button.data:
                SubscriptionService.remove(
                    user_id=current_user.id, product_id=product_id
                )
                is_already_subscribed = False
                flash("Product unsubscribed", "success")
            return redirect(
                url_for("products.single_product_view", product_id=product_id)
            )

    tab = None
    product_to_show = item_service.get_product_to_show_by_id(product_id)
    is_already_subscribed = SubscriptionService.check_if_subscribed(
        user_id=current_user.id, product_id=product_id
    )

    return render_template(
        "products/single_product.html",
        product=product_to_show,
        tab=tab,
        form=form,
        is_already_subscribed=is_already_subscribed,
    )


@bp.route("/search/<product_name>", methods=["GET", "POST"])
@login_required
@confirmed_user_required
@inject
def search_product(product_name):
    """Wyszukiwanie produktu z ceneo"""
    return "Test"
