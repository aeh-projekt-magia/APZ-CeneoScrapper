from flask.cli import FlaskGroup
import pytest
from app import create_app, db
from app.models.models import User
from config import DevelopmentConfig, ProductionConfig, TestingConfig


from app.repositories import ProductsRepository, ReviewsRepository
from app.models.models import Products, Reviews

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
        print(
            f"User: {user.id}: {user.email}, is_confirmed: {user.is_confirmed}, is_admin: {user.is_admin}"
        )

@cli.command("towar")
def towar():
    """Add some towar to database"""
    repo_prod = ProductsRepository.SqlAlchemyRepository(db.session)
    new_product = Products(
        name="Iphone 15 pro max ultra giga mega",
        category="Smartphone",
        price="90000 zł",
        available_shops_count="Available in 50 shops",
        reviews_count="12 reviews",
        description="Smartfon Apple z ekranem 6,1 cala, wyświetlacz OLED. Aparat 12 Mpix, pamięć 4 GB RAM. Obsługuje sieć: 5G",
    )
    

    repo_rev = ReviewsRepository.SqlAlchemyRepository(db.session)

    new_review = Reviews(
        name="jakub",
        stars="5",
        description="Fajny no fajny polecam każdemu",
        zalety=["dobry", "fajny", "szybki"],
        wady=["drogi", "śliski"],
        recommendation="Polecam",
        date=[],
        parent=new_product,
    )
    new_review2 = Reviews(
        name="robert",
        stars="4",
        description="Fajny no fajny polecam każdemu",
        zalety=["dobry", "fajny", "szybki"],
        wady=["drogi", "śliski"],
        recommendation="Polecam",
        date=[],
        parent=new_product,
    )
    new_review3 = Reviews(
        name="jakub",
        stars="5",
        description="Fajny no fajny polecam każdemu",
        zalety=["dobry", "fajny", "szybki"],
        wady=["drogi", "śliski"],
        recommendation="Polecam",
        date=[],
        parent=new_product,
    )
    new_review4 = Reviews(
        name="robert",
        stars="4",
        description="Fajny no fajny polecam każdemu",
        zalety=["dobry", "fajny", "szybki"],
        wady=["drogi", "śliski"],
        recommendation="Polecam",
        date=[],
        parent=new_product,
    )

    repo_rev.add_all([new_review, new_review2, new_review3, new_review4])
    repo_prod.add(new_product)
    db.session.commit()


@cli.command("test")
def test():
    """Run tests
    --verbose - shows folders
    -rP - shows printouts from tests #can be deleted later#"""
    pytest.main(["-rP", "--verbose","--rootdir", "."])


@cli.command("test_clean")
def test_clean():
    """Run tests with no extra flags"""
    pytest.main(["--rootdir", "."])


@cli.command("test_extra")
def test_extra():
    """Run tests with --setup-show (fixtures)"""
    pytest.main(["-rP", "--verbose", "--setup-show", "--rootdir", "."])


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


if __name__ == "__main__":
    cli()
