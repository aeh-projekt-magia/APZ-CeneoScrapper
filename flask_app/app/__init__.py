from flask import Flask

from app.extensions import db, bcrypt, migrate, login_manager
from config import DevelopmentConfig, TestingConfig
from app.models.models import User


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "accounts.login"
    login_manager.login_message_category = "danger"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == int(user_id)).first()

    bcrypt.init_app(app)

    migrate.init_app(app, db)

    # from app.controllers.main import bp as main_bp
    # app.register_blueprint(main_bp)

    from app.controllers.main.routes import bp as main_bp
    app.register_blueprint(main_bp)

    from app.controllers.accounts.routes import bp as accounts_bp
    app.register_blueprint(accounts_bp)

    from app.controllers.products import bp as products_bp
    app.register_blueprint(products_bp, url_prefix='/products')

    app.shell_context_processor({'app': app, 'db': db})
    return app
