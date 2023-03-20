from flask import render_template

from app.main import bp
import os
import markdown as md


# @bp.route('/')
# def index():
#     return render_template('index.html')


@bp.route('/')
def index():
    return render_template("index.html")
