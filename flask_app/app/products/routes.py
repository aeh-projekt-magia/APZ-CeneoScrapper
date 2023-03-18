from flask import render_template, request, url_for, redirect
from app.products import bp
from app.services.scrapper import QueryReviews


@bp.route('/<int:productid>', methods=['GET'])
def show_reviews_by_id(productid):
    a = QueryReviews(productid).get_reviews()
    return render_template('products/index.html', reviews=a)


@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        pass
    else:
        a = QueryReviews('143471602').get_reviews()
        return render_template('products/index.html', reviews=a)
