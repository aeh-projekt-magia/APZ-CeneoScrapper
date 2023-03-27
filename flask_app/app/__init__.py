from flask import Flask

from app.extensions import db
from flask_app.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from app.controllers.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.controllers.products import bp as products_bp
    app.register_blueprint(products_bp, url_prefix='/products')

    return app
