from flask import Blueprint

bp = Blueprint("subscriptions", __name__)

"""Not a mistake, this import is crucial for app"""
from app.controllers.subscriptions.routes import bp # noqa:E402,F401
