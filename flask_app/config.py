import os

from app.repository.item.impl_item_repository import ImplItemRepository
from app.repository.item.item_repository import ItemRepository
from app.repository.price_history.impl_price_history_repository import ImplPriceHistoryRepository
from app.repository.price_history.price_history_repository import PriceHistoryRepository
from app.repository.user.impl_user_repository import ImplUserRepository
from app.repository.user.user_repository import UserRepository
from app.services.ceneo.ceneo_item import CeneoItem
from app.services.ceneo.item_interface import ItemInterface
from injector import singleton

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get("SECRET_KEY", default="zgadnij")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URI"
    ) or "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 4
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    SECURITY_PASSWORD_SALT = os.environ.get(
        "SECURITY_PASSWORD_SALT", default="very-important"
    )

    EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")


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
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_TEST_URI") or "sqlite:///:memory:"
    )
    """moze tez byc baza in memory, 'sqlite:///:memory:'"""
    """Min 4 rounds, max 31"""
    BCRYPT_LOG_ROUNDS = 4
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    DEBUG = False
    DEBUG_TB_ENABLED = False


class Dependencies:
    @staticmethod
    def configure(binder):
        binder.bind(ItemInterface, to=CeneoItem, scope=singleton)
        binder.bind(ItemRepository, to=ImplItemRepository, scope=singleton)
        binder.bind(UserRepository, to=ImplUserRepository, scope=singleton)
        binder.bind(PriceHistoryRepository, to=ImplPriceHistoryRepository, scope=singleton)
