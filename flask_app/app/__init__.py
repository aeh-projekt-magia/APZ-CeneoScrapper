from flask import Flask, render_template

from app.extensions import db, bcrypt, migrate, login_manager

from config import DevelopmentConfig, Config


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "accounts.login"
    login_manager.login_message_category = "danger"

    from app.models.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == int(user_id)).first()

    bcrypt.init_app(app)

    migrate.init_app(app, db)


    from app.controllers.main.routes import bp as main_bp
    app.register_blueprint(main_bp)

    from app.controllers.accounts.routes import bp as accounts_bp
    app.register_blueprint(accounts_bp)

    from app.controllers.products.routes import bp as products_bp
    app.register_blueprint(products_bp, url_prefix='/products')

    from app.controllers.subscriptions import bp as subscriptions_bp
    app.register_blueprint(subscriptions_bp, url_prefix='/subscriptions')

    app.shell_context_processor({'app': app, 'db': db})


    """No use, since every page is user login required"""
    # @app.errorhandler(401)
    # def unauthorized_page(error):
    #     return render_template("errors/401.html"), 401

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("errors/404.html"), 404


    @app.errorhandler(500)
    def server_error_page(error):
        return render_template("errors/500.html"), 500

    return app
