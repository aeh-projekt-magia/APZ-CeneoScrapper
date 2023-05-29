from flask import Flask, render_template
from app import containers
from app.extensions import db, bcrypt, migrate, login_manager
from config import DevelopmentConfig, ProductionConfig, TestingConfig


def create_app(
    config_class=DevelopmentConfig,
):
    container = containers.Container()
    container.init_resources()

    app = Flask(__name__)
    app.config.from_object(config_class)
    app.container = container

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "accounts.login"
    login_manager.login_message_category = "danger"
    # TODO: Zabezpieczenia! + może dodać fresh_login
    # login_manager.session_protection = "strong" lub None lub 'basic'

    from app.models.UserModel import User

    @login_manager.user_loader
    def load_user(userId):
        return User.query.filter(User.id == int(userId)).first()

    bcrypt.init_app(app)

    migrate.init_app(app, db)

    from app.controllers.main.routes import bp as main_bp

    app.register_blueprint(main_bp)

    from app.controllers.accounts.routes import bp as accounts_bp

    app.register_blueprint(accounts_bp)

    from app.controllers.products.routes import bp as products_bp

    app.register_blueprint(products_bp, url_prefix="/products")

    from app.controllers.subscriptions import bp as subscriptions_bp

    app.register_blueprint(subscriptions_bp, url_prefix="/subscriptions")

    from app.controllers.scheduler import bp as scheduler_bp

    app.register_blueprint(scheduler_bp, url_prefix="/scheduler")

    app.shell_context_processor({"app": app, "db": db})

    """No use, since every page is user login required"""

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template("errors/500.html"), 500

    return app
