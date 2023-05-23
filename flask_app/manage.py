from flask.cli import FlaskGroup
import click
import pytest
from app import create_app, db
from app.models.UserModel import User
from app.models.ItemModel import Item
from app.models.PriceHistoryModel import PriceHistory
from app.repository.item.impl_item_repository import ImplItemRepository
from app.repository.user.impl_user_repository import ImplUserRepository

import datetime

# app=create_app();app.app_context().push()


# from app.models.models import Products, Reviews
# from app.models.

# app = create_app()


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
@click.option("-q", default=1, help="How many records")
@click.option("-r", default=True, help="Make random choice")
def towar(q, r):
    """Add some towar to database"""
    from db_seed import towar

    towar(quantity=q, random=r)


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
        offer_url="www.google.com",
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
    new_item = Item(item_id=item_id, is_available=True, lowest_price=9.5)
    item_repo.update_item(new_item)


@cli.command("add_User")
def add_User():
    email = input("Podaj email:")
    user = User(email=email, password="empty", is_admin=False)

    user_repo.add_user(user)


@cli.command("get_AllUsers")
def get_AllUsers():
    user_repo.get_all_users()


if __name__ == "__main__":
    cli()
