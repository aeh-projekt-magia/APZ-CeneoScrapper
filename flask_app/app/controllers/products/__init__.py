from flask import Blueprint

bp = Blueprint('products', __name__)

from app.controllers.products import routes
