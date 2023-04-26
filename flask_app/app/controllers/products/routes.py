from flask import jsonify, render_template, request, current_app, flash, redirect
from flask_login import login_required, current_user
from app import db
from app.controllers.products import bp

# from app.extensions import db
from app.models.models import Reviews, Products, User
from app.services.decorators import confirmed_user_required
from app.services.scrapper import QueryReviews
from app.repositories import ProductsRepository, ReviewsRepository
from app.services.forms import SubscribeProductForm
from markupsafe import escape


# @bp.route("/<int:productid>", methods=["GET"])
# @login_required
# @confirmed_user_required
# def show_reviews_by_id(productid):
#     """Pobranie recenzji o danym produkcie, zapisanie ich do bazy danych i wyświetlenie"""
#     reviews = QueryReviews(productid).get_reviews()

#     new_product = Product.query.filter_by(product_id=productid).first()
#     if not new_product:
#         new_product = Product(product_id=productid, name="Nieznana")
#         db.session.add(new_product)
#         db.session.commit()

#     for review in reviews:
#         new_review = Review(
#             product_id=productid,
#             author=review["author"],
#             recommendation=review["recommendation"],
#             stars=review["stars"],
#             content=review["content"],
#             publish_date=review["publish_date"],
#             purchase_date=review["purchase_date"],
#             useful=review["useful"],
#             useless=review["useless"],
#             pros="".join(str(x) for x in review["pros"]),
#             cons="".join(str(x) for x in review["cons"]),
#             review_id=1,
#         )
#         db.session.add(new_review)
#         db.session.commit()

#     return render_template("products/index.html", reviews=reviews, productid=productid)


@bp.route("/add", methods=["GET", "POST"])
@login_required
@confirmed_user_required
def add():
    tab = None
    repo_prod = ProductsRepository.SqlAlchemyRepository(db.session)
    new_product = Products(
        name="aa",
        category="Smartphone",
        price="200 zł",
        available_shops_count="Available in 50 shops",
        reviews_count="12 reviews",
        description="Smartfon Apple z ekranem 6,1 cala, wyświetlacz OLED. Aparat 12 Mpix, pamięć 4 GB RAM. Obsługuje sieć: 5G",
    )

    repo_rev = ReviewsRepository.SqlAlchemyRepository(db.session)

    new_review = Reviews(
        name="jakub",
        stars="5",
        description="Fajny no fajny polecam każdemu",
        zalety=["dobry", "fajny", "szybki"],
        wady=["drogi", "śliski"],
        recommendation="Polecam",
        date=[],
        parent=new_product,
    )
    new_review2 = Reviews(
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
    repo_prod = ProductsRepository.SqlAlchemyRepository(db.session)
    products_to_show = repo_prod.list()

    return render_template("products/index.html", products=products_to_show)


@bp.route("/<int:product_id>", methods=["GET", "POST"])
@login_required
@confirmed_user_required
def single_product_view(product_id):
    """Wyświetlenie konkretnego pobranego do tej pory produktu"""
    form = SubscribeProductForm(request.form)
    tab = None
    repo_prod = ProductsRepository.SqlAlchemyRepository(db.session)
    product_to_show = repo_prod.get_by_id(product_id)

    if form.validate_on_submit():
        if form.subscribe_button.data:
            flash('Product subscribed', 'success')
            flash(f'{current_user.id}')

            user = db.session.query(User).where(User.id == current_user.id).first()
            product = db.session.query(Products).where(Products.id == product_id).first()
            
            user.subscriptions.append(product)
            db.session.commit()
            return render_template("products/single_product.html", product=product_to_show, tab=tab, form=form)
            

    if request.args.get("tab") == "1" and product_to_show:
        tab = 1
        return render_template(
            "products/single_product.html",
            product=product_to_show,
            tab=tab,
            reviews=product_to_show.children,
            form=form
        )
    return render_template("products/single_product.html", product=product_to_show, tab=tab, form=form)
