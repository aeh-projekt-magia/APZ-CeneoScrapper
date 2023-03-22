from flask import Blueprint

bp = Blueprint('accounts', __name__)

from app.controllers.accounts import routes
