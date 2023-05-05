from flask.cli import FlaskGroup
import click
import pytest
from app import create_app, db
from app.models.UserModel import User
from app.models.ItemModel import Item
from app.models.PriceHistoryModel import PriceHistory

import datetime

# app=create_app();app.app_context().push()


# from app.models.models import Products, Reviews
# from app.models.

# app = create_app()
cli = FlaskGroup(create_app=create_app)


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
@click.option('-q', default =1, help="How many records")
@click.option('-r', default=True, help="Make random choice")
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
    itemId = input("Podaj Id itemu:")
    from app.repository.ItemRepository import addItem

    addItem(db, itemId, "test", True, 9.99, "www.google.com")


@cli.command("get_Item")
def get_Item():
    from app.repository.ItemRepository import getItem

    getItem("1234")


@cli.command("get_AllItems")
def get_AllItems():
    from app.repository.ItemRepository import getAllItems

    getAllItems()


@cli.command("del_Item")
def del_Item():
    from app.repository.ItemRepository import deleteItem

    itemId = input("Podaj Id itemu:")
    deleteItem(itemId)


@cli.command("del_AllItems")
def del_AllItems():
    from app.repository.ItemRepository import deleteAllItems

    deleteAllItems()


@cli.command("update_Item")
def update_Item():
    from app.repository.ItemRepository import updateItem

    itemId = input("Podaj Id itemu:")
    updateItem(itemId, True, 9.5)


@cli.command("add_User")
def add_User():
    email = input("Podaj email:")
    from app.repository.UserRepository import addUser

    addUser(email, "empty", False)


@cli.command("get_AllUsers")
def get_AllUsers():
    from app.repository.UserRepository import getAllUsers

    getAllUsers()


if __name__ == "__main__":
    cli()
