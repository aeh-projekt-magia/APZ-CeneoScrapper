from flask import jsonify, render_template, request, current_app, flash, redirect
from flask_login import login_required, current_user
from app import db
from app.controllers.products import bp

# from app.models.models import Reviews, Products, User
from app.models.UserModel import User
from app.models.ItemReviewModel import Review
from app.models.ProductModel import Products


from app.services.decorators import confirmed_user_required
from app.repositories import ProductRepository, ReviewRepository
from app.services.forms import SubscribeProductForm

from app.services.product_subscriber import ProductSubscription


@bp.route("/add", methods=["GET", "POST"])
@login_required
@confirmed_user_required
def add():
    tab = None
    repo_prod = ProductRepository.SqlAlchemyRepository(db.session)
    new_product = Products(
        name="aa",
        category="Smartphone",
        price="200 zł",
        available_shops_count="Available in 50 shops",
        reviews_count="12 reviews",
        description="Smartfon Apple z ekranem 6,1 cala, wyświetlacz OLED. Aparat 12 Mpix, pamięć 4 GB RAM. Obsługuje sieć: 5G",
    )

    repo_rev = ReviewRepository.SqlAlchemyRepository(db.session)

    new_review = Review(
        name="jakub",
        stars="5",
        description="Fajny no fajny polecam każdemu",
        zalety=["dobry", "fajny", "szybki"],
        wady=["drogi", "śliski"],
        recommendation="Polecam",
        date=[],
        parent=new_product,
    )
    new_review2 = Review(
        name="robert",
        stars="4",
        description="Fajny no fajny polecam każdemu",
        zalety=["dobry", "fajny", "szybki"],
        wady=["drogi", "śliski"],
        recommendation="Polecam",
        date=[],
        parent=new_product,
    )

    repo_rev.add_all([new_review, new_review2])
    repo_prod.add(new_product)
    db.session.commit()

    return jsonify({"good": "good"})


@bp.route("/", methods=["GET", "POST"])
@login_required
@confirmed_user_required
def index():
    """Wyświetlenie pobranych do tej pory produktów"""
    repo_prod = ProductRepository.SqlAlchemyRepository(db.session)
    products_to_show = repo_prod.list()

    return render_template("products/index.html", products=products_to_show)


@bp.route("/<int:product_id>", methods=["GET", "POST"])
@login_required
@confirmed_user_required
def single_product_view(product_id):
    """Wyświetlenie konkretnego pobranego do tej pory produktu"""
    tab = None

    product_to_show = db.session.query(Products).where(Products.id == product_id).first()
    
    is_already_subscribed = ProductSubscription.get(user_id=current_user.id, product_id=product_id)


    """Subscribe or unsubscribe request handling"""
    form = SubscribeProductForm(request.form)
    if form.validate_on_submit():
        if form.subscribe_button.data:            
            ProductSubscription.add(user_id=current_user.id, product_id=product_id)
            is_already_subscribed=True            
            flash('Product subscribed', 'success')                    
        elif form.unsubscribe_button.data:
            ProductSubscription.remove(user_id=current_user.id, product_id=product_id)
            is_already_subscribed=False
            flash('Product unsubscribed', 'success')            
        return render_template("products/single_product.html", product=product_to_show, tab=tab, form=form, is_already_subscribed=is_already_subscribed)

    """Tabs switching comments/shops"""
    if request.args.get("tab") == "1" and product_to_show:
        tab = 1
        return render_template(
            "products/single_product.html",
            product=product_to_show,
            tab=tab,
            reviews=product_to_show.children,
            form=form
        )
    return render_template("products/single_product.html", product=product_to_show, tab=tab, form=form, is_already_subscribed=is_already_subscribed)
