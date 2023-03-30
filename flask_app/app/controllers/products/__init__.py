from flask import Blueprint

bp = Blueprint('products', __name__)

"""Not a mistake, this import is crucial for app"""
from app.controllers.products.routes import bp

