from flask import Blueprint

bp = Blueprint("scheduler", __name__)

from app.controllers.scheduler.routes import bp # noqa:E402,F401
