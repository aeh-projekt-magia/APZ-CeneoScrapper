from flask import Blueprint, render_template, flash
from flask_login import login_required

from app.models.models import User, Product, Review
from app.controllers.main import bp


@bp.route("/")
@login_required
def home():
    return render_template("index.html")

