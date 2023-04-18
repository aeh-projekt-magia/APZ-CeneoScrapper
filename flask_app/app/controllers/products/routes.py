from flask import jsonify, render_template, request
from flask_login import login_required

from app.controllers.products import bp
# from app.extensions import db
from app.models.models import Review, Product
from app.services.decorators import confirmed_user_required
from app.services.scrapper import QueryReviews

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


reviews = [
    {
        "name": "jakub",
        "stars": "5",
        "description": "Fajny no fajny polecam każdemu",
        "zalety": ["dobry", "fajny", "szybki"],
        "wady": ["drogi", "śliski"],
        "recommendation": "Polecam",
        "date": {"month": "Jan", "day": "05"},
    },
    {
        "name": "robert",
        "stars": "2",
        "description": "Kurde średni średni na prawde, wiecej nie kupie",
        "zalety": ["szybki"],
        "wady": ["drogi że aż nie moge!", "śliski jak diabli!"],
        "recommendation": "Nie polecam",
        "date": {"month": "Mar", "day": "28"},
    },
]

product = {
    "name": "Iphone 14 pro ultra mini micro nano 2s",
    "category": "Smartphone",
    "price": "200 zł",
    "available_shops_count": "Available in 50 shops",
    "reviews_count": "12 reviews",
    "description": "Smartfon Apple z ekranem 6,1 cala, wyświetlacz OLED. Aparat 12 Mpix, pamięć 4 GB RAM. Obsługuje sieć: 5G",
    "reviews" : reviews
}

@bp.route("/", methods=["GET", "POST"])
@login_required
@confirmed_user_required
def index():
    """Wyświetlenie pobranych do tej pory recenzji"""
    tab = None

    if request.args.get("tab") == "1":
        tab = 1
        return render_template(
            "products/index.html", product=product, tab=tab, reviews=product['reviews']
        )
    return render_template("products/index.html", product=product, tab=tab)

