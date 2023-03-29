import unittest

from flask.cli import FlaskGroup

from app import create_app, db
from app.models.models import User

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command('recreate_db')
def recreate_db():
    """Migrate database"""
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command('show')
def show():
    """Show app.config"""
    for x in app.config:
        print(x)


@cli.command('show_users')
def show_users():
    """Query all users in database"""
    users = User.query.all()

    for user in users:
        print(f'User: {user.id}: {user.email}, is_confirmed: {user.is_confirmed}, is_admin: {user.is_admin}')


@cli.command("test")
def test():
    """Runs the unit tests without coverage."""
    tests = unittest.TestLoader().discover("app/tests", pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    else:
        return 1


@cli.command("create_admin")
def create_admin():
    """Create admin user"""
    try:
        admin_user = User(email='j@j.com', password='123456', is_admin=True, is_confirmed=True)
        db.session.add(admin_user)
        db.session.commit()
        print(f'Created admin account')
    except Exception as e:
        print(f'Failed to create admin acccount! {e}')



@cli.command('populate_Posts')
def populate_Posts():
    from app.models.post import Post
    post_list = [{'title': 'Jakub', 'content': 'Turek'},
                 {'title': 'RObson', 'content': 'Ama'},
                 {'title': 'ema', 'content': 'fyfą'}]
    for x in post_list:
        db.session.add(Post(title=x['title'], content=x['content']))
        db.session.commit()


if __name__ == '__main__':
    cli()

test_app = create_app()