from app import db
from app.controllers.products import bp
from app.models.ItemModel import Item

# from app.models.models import Reviews, Products, User
from app.services.decorators import confirmed_user_required
from app.services.forms import SubscribeProductForm
from app.services.product_subscriber import ProductSubscription
from flask import flash, render_template, request
from flask_login import current_user, login_required


@bp.route("/", methods=["GET", "POST"])
@login_required
@confirmed_user_required
def index():
    """Wyświetlenie pobranych do tej pory produktów"""
    # TODO: products/routes - Dodać obsługę repozytorium
    products_to_show = Item.query.all()

    return render_template("products/index.html", products=products_to_show)


@bp.route("/<int:product_id>", methods=["GET", "POST"])
@login_required
@confirmed_user_required
def single_product_view(product_id):
    """Wyświetlenie konkretnego pobranego do tej pory produktu"""
    # TODO: products/routes - Dodać obsługę repozytorium
    tab = None

    product_to_show = db.session.query(Item).where(Item.id == product_id).first()
    is_already_subscribed = ProductSubscription.get(
        user_id=current_user.id, product_id=product_id
    )

    """Subscribe or unsubscribe request handling"""
    form = SubscribeProductForm(request.form)
    if form.validate_on_submit():
        if form.subscribe_button.data:
            ProductSubscription.add(user_id=current_user.id, product_id=product_id)
            is_already_subscribed = True
            flash("Product subscribed", "success")
        elif form.unsubscribe_button.data:
            ProductSubscription.remove(user_id=current_user.id, product_id=product_id)
            is_already_subscribed = False
            flash("Product unsubscribed", "success")
        return render_template(
            "products/single_product.html",
            product=product_to_show,
            tab=tab,
            form=form,
            is_already_subscribed=is_already_subscribed,
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
