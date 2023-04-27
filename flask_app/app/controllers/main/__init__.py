from flask import Blueprint

bp = Blueprint("main", __name__)

"""Not a mistake, this import is crucial for app"""
from app.controllers.main.routes import bp # noqa:E402,F401
