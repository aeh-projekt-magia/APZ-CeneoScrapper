from flask import flash, render_template, request, redirect,url_for
from flask_login import current_user, login_required
from app.controllers.products import bp
from app.services.decorators import confirmed_user_required
from app.services.forms import SubscribeProductForm

from app.services.subscription_service import SubscriptionService
from app.services.product_service import ProductService


@bp.route("/", methods=["GET"])
@login_required
@confirmed_user_required
def index():
    """Wyświetlenie pobranych do tej pory produktów"""
    # TODO: products/routes - Dodać obsługę repozytorium

    products_to_show = ProductService.get_all_products_to_show()

    return render_template("products/index.html", products=products_to_show)


@bp.route("/<int:product_id>", methods=["GET", "POST"])
@login_required
@confirmed_user_required
def single_product_view(product_id):
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
                SubscriptionService.remove(user_id=current_user.id, product_id=product_id)
                is_already_subscribed = False
                flash("Product unsubscribed", "success")
            return redirect(url_for("products.single_product_view", product_id=product_id))

    # TODO: products/routes - Dodać obsługę repozytorium
    tab = None
    product_to_show = ProductService.get_product_to_show_by_id(product_id)
    is_already_subscribed = SubscriptionService.check_if_subscribed(
        user_id=current_user.id, product_id=product_id
    )


    # TODO: Nie ma już opinii, wywalić raczej
    """Tabs switching comments/shops"""
    if request.args.get("tab") == "1" and product_to_show:
        tab = 1
        return render_template(
            "products/single_product.html",
            product=product_to_show,
            tab=tab,
            reviews=product_to_show.children,
            form=form,
        )
    return render_template(
        "products/single_product.html",
        product=product_to_show,
        tab=tab,
        form=form,
        is_already_subscribed=is_already_subscribed,
    )
