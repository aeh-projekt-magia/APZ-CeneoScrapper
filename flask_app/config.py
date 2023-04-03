import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY', default='zgadnij')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 4
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT", default="very-important")

    EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    WTF_CSRF_ENABLED = False
    DEBUG_TB_ENABLED = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    DEBUG_TB_ENABLED = True
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test_app.db')
    """Min 4 rounds, max 31"""
    BCRYPT_LOG_ROUNDS = 4
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    DEBUG = False
    DEBUG_TB_ENABLED = False
