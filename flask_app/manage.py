from flask.cli import FlaskGroup
import pytest
from app import create_app, db
from app.models.UserModel import User
from app.models.ItemModel import Item
from app.models.PriceHistoryModel import PriceHistory
from app.repository.item.impl_item_repo import ImplItemRepository

import datetime

# app=create_app();app.app_context().push()


# from app.models.models import Products, Reviews
# from app.models.

# app = create_app()
from repository.user.impl_user_repository import ImplUserRepository

cli = FlaskGroup(create_app=create_app)
item_repo = ImplItemRepository()
user_repo = ImplUserRepository()

@cli.command("recreate_db")
def recreate_db():
    """Migrate database"""
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("show_users")
def show_users():
    """Query all users in database"""
    users = User.query.all()

    for user in users:
        print(f"{user.id=}, {user.email=}, {user.is_confirmed=}, {user.is_admin=}")


@cli.command("towar")
def towar():
    """Add some towar to database"""

    user = User.query.filter_by(id=1).first()

    new_product = Item(
        name="Iphone 17",
        category="Smartphone",
        price="5000 zł",
        available_shops_count="Available in 50 shops",
        reviews_count="12 reviews",
        description="Smartfon Apple z ekranem 6,1 cala, wyświetlacz OLED.\
             Aparat 12 Mpix, pamięć 4 GB RAM. Obsługuje sieć: 5G",
        image_url="https://image.ceneostatic.pl/data/products/115107321/i-apple-iphone-14-128gb-polnoc.jpg",
    )

    new_price_history = []
    for index, x in enumerate(range(25)):
        new_price_history.append(
            PriceHistory(
                item=new_product,
                price=6000 - index * 200,
                date=datetime.datetime.now() - datetime.timedelta(days=index),
            )
        )

    # Subscription()

    user.subscriptions.append(new_product)
    try:
        db.session.add(new_product)
        db.session.add_all(new_price_history)
        db.session.commit()
    except Exception:
        db.session.rollback()


@cli.command("test")
def test():
    """Run tests
    --verbose - shows folders
    -rP - shows printouts from tests #can be deleted later#"""
    pytest.main(["-rP", "--verbose", "--rootdir", "."])


@cli.command("coverage")
def coverage():
    """Run pytest coverage test"""
    pytest.main(["--cov"])


@cli.command("create_admin")
def create_admin():
    """Create admin user"""
    try:
        admin_user = User(
            email="j@j.com", password="123456", is_admin=True, is_confirmed=True
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Created admin account")
    except Exception as e:
        print(f"Failed to create admin acccount! {e}")


@cli.command("add_Item")
def add_Item():
    item_id = input("Podaj Id itemu:")
    item = Item(
        item_id=item_id,
        name="test",
        is_available=True,
        lowest_price=9.99,
        offer_url="www.google.com"
    )

    item_repo.add_item(item)


@cli.command("get_Item")
def get_Item():
    item_repo.get_item_by_id("1234")


@cli.command("get_AllItems")
def get_AllItems():
    item_repo.get_all_items()


@cli.command("del_Item")
def del_Item():
    item_id = input("Podaj Id itemu:")
    item_repo.delete_item_by_id(item_id)


@cli.command("del_AllItems")
def del_AllItems():
    item_repo.delete_all_items()


@cli.command("update_Item")
def update_Item():
    item_id = input("Podaj Id itemu:")
    new_item = Item(
        item_id=item_id,
        is_available=True,
        lowest_price=9.5
    )
    item_repo.update_item(new_item)


@cli.command("add_User")
def add_User():
    email = input("Podaj email:")
    user = User(
        email=email,
        password="empty",
        is_admin=False
    )

    user_repo.add_user(user)


@cli.command("get_AllUsers")
def get_AllUsers():
    user_repo.get_all_users()


if __name__ == "__main__":
    cli()
