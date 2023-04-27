from flask import render_template
from flask_login import login_required

from app.controllers.main import bp


@bp.route("/")
@login_required
def home():
    return render_template("index.html")
