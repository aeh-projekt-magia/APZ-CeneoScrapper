from flask import render_template, request, url_for, redirect
from app.controllers.products import bp
from app.services.scrapper import QueryReviews
from app.services.decorators import logout_required, check_is_confirmed
from app.models.models import Review
from app.extensions import db
from flask_login import login_required

@bp.route('/<int:productid>', methods=['GET'])
@login_required
@check_is_confirmed
def show_reviews_by_id(productid):
    """Pobranie recenzji o danym produkcie, zapisanie ich do bazy danych i wyświetlenie"""
    reviews = QueryReviews(productid).get_reviews()

    for review in reviews:
        new_review = Review(product_id=productid,
                            author=review['author'],
                            recommendation=review['recommendation'],
                            stars=review['stars'],
                            content=review['content'],
                            publish_date=review['publish_date'],
                            purchase_date=review['purchase_date'],
                            useful=review['useful'],
                            useless=review['useless'],
                            pros=''.join(str(x) for x in review['pros']),
                            cons=''.join(str(x) for x in review['cons']),
                            review_id=review['review_id'])
        db.session.add(new_review)
        db.session.commit()

    return render_template('products/index.html', reviews=reviews, productid=productid)


@bp.route('/', methods=['GET', 'POST'])
@login_required
@check_is_confirmed
def index():
    """Wyświetlenie pobranych do tej pory recenzji"""
    if request.method == 'POST':
        pass
    else:
        reviews = Review.query.all()
        return render_template('products/index.html', reviews=reviews)
