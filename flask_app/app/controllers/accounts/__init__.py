from flask import Blueprint

bp = Blueprint("accounts", __name__)

from app.controllers.accounts.routes import bp  # noqa:E402,F401
