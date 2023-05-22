from flask import Blueprint

bp = Blueprint("scheduler", __name__)

from app.controllers.scheduler.routes import bp
