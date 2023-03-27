from flask import Blueprint, render_template, flash
from flask_login import login_required
from app import db
from app.models.models import User


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
    flash('dupa', "info")
    return render_template("index.html")