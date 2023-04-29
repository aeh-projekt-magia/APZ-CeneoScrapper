from flask import render_template
from flask_login import login_required, current_user
from app.controllers.subscriptions import bp
from app.services.subscription_service import SubscriptionService
from app.services.decorators import confirmed_user_required
from app.models.ItemModel import Item
from app.models.SubscriptionModel import Subscription
from app.models.PriceHistoryModel import PriceHistory


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
    """Wyświetlenie konkretnego pobranego do tej pory produktu"""

    new_product = Item(
        name="Iphone 14",
        category="Smartphone",
        price="90000 zł",
        available_shops_count="Available in 50 shops",
        reviews_count="12 reviews",
        description="Smartfon Apple z ekranem 6,1 cala, wyświetlacz OLED.\
            Aparat 12 Mpix, pamięć 4 GB RAM. Obsługuje sieć: 5G",
        image_url="https://image.ceneostatic.pl/data/products/115107321/i-apple-iphone-14-128gb-polnoc.jpg",
    )

    new_subscription = Subscription(
        itemId=1,
        userId=1,
        notificationFreq=2,
        notifyOnPriceChange=True,
        send_notification=True,
    )
    new_pricehistory = [
        PriceHistory(itemId=1, price=5000, date='20.04.2022'),
        PriceHistory(itemId=1, price=4500, date='22.04.2022'),
        PriceHistory(itemId=1, price=4000, date='27.04.2022')
    ]

    return render_template(
        "subscriptions/single_subscription.html",
        product=new_product,
        subscription=new_subscription,
        price_history=new_pricehistory,
    )

    # TODO: products/routes - Dodać obsługę repozytorium
    # tab = None
    # product_to_show = ProductService.get_product_to_show_by_id(product_id)
    # is_already_subscribed = SubscriptionService.get(
    #     user_id=current_user.id, product_id=product_id
    # )

    # """Subscribe or unsubscribe request handling"""
    # form = SubscribeProductForm(request.form)

    # if form.validate_on_submit():
    #     if form.subscribe_button.data:
    #         SubscriptionService.add(user_id=current_user.id, product_id=product_id)
    #         is_already_subscribed = True
    #         flash("Product subscribed", "success")
    #     elif form.unsubscribe_button.data:
    #         SubscriptionService.remove(user_id=current_user.id, product_id=product_id)
    #         is_already_subscribed = False
    #         flash("Product unsubscribed", "success")
    #     return render_template(
    #         "products/single_product.html",
    #         product=product_to_show,
    #         tab=tab,
    #         form=form,
    #         is_already_subscribed=is_already_subscribed,
    #     )

    # # TODO: Nie ma już opinii, wywalić raczej
    # """Tabs switching comments/shops"""
    # if request.args.get("tab") == "1" and product_to_show:
    #     tab = 1
    #     return render_template(
    #         "products/single_product.html",
    #         product=product_to_show,
    #         tab=tab,
    #         reviews=product_to_show.children,
    #         form=form,
    #     )
    # return render_template(
    #     "products/single_product.html",
    #     product=product_to_show,
    #     tab=tab,
    #     form=form,
    #     is_already_subscribed=is_already_subscribed,
    # )
