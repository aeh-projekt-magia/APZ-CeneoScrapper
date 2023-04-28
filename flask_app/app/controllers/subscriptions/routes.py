from flask import render_template
from flask_login import login_required, current_user
from app.controllers.subscriptions import bp
from app.services.subscription_service import SubscriptionService
from app.services.decorators import confirmed_user_required


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
