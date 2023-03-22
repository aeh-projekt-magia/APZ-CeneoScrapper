# from flask import render_template
#
# from app.controllers.main import bp
#
# @bp.route('/')
# def index():
#     return render_template("index.html")


from flask import Blueprint, render_template
from flask_login import login_required

core_bp = Blueprint("core", __name__)


@core_bp.route("/")
@login_required
def home():
    return render_template("index.html")
