from flask import render_template
from flask_login import login_required, current_user
from app import db
from app.controllers.subscriptions import bp

# from app.extensions import db
from app.models.UserModel import User


from app.services.decorators import confirmed_user_required



@bp.route("/", methods=["GET", "POST"])
@login_required
@confirmed_user_required
def index():
    """Wyświetlenie zasubskrybowanych produktów"""
    # TODO:subscriptions/routes - Dodać repozytorium
    products_to_show = (
        db.session.query(User).where(User.id == current_user.id).first().subscriptions
    )

    return render_template("subscriptions/index.html", products=products_to_show)
