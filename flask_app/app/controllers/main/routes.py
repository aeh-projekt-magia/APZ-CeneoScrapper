from flask import Blueprint, render_template, flash
from flask_login import login_required

from app.models.models import User, Product, Review

bp = Blueprint("core", __name__)


@bp.route("/")
@login_required
def home():
    return render_template("index.html")


@bp.route("/1")
def testowy():
    users = User.query.all()
    lista = []
    for a in users:
        lista.append([a.id, a.email, str(a.password), a.created_on, a.is_admin, a.is_confirmed])
    return lista


@bp.route("/2")
def test2():
    flash('testowy flasz', "info")
    return render_template("index.html")


# @bp.route("/3")
# def test3():
#     products = Product.query.all()
#     lista = []
#     for product in products:
#         lista.append([product.product_id, product.name, product.review])
#     return lista


from app import db


@bp.route("/3")
def test3():

    product1 = Product(product_id=2137, name='Jakub!')
    product2 = Product(product_id=6969, name='Agatka!')

    review1 = Review(author='Jakis', review_id='01', product=product1)
    review2 = Review(author='Debil', review_id='02', product_id=1)

    db.session.add(product1)
    db.session.add(product2)
    db.session.add(review1)
    db.session.add(review2)
    db.session.commit()

    return "  Done!"


@bp.route("/4")
def test4():
    result = []
    products = Product.query.all()
    aaa = db.session.query(Product).first()

    dwa = []
    for x in aaa.review:
        dwa.append(x.author)

    for product in products:
        rev = []
        for review in product.review:
            rev.append([review.author, review.review_id])

        result.append([product.product_id, product.name, rev])

    return aaa.name, dwa

