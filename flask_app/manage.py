from flask.cli import FlaskGroup
import pytest
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
    """Run tests
    --verbose - shows folders
    -rP - shows printouts from tests #can be deleted later#"""
    pytest.main(['-rP','--verbose', '--rootdir', '.'])

@cli.command("test_clean")
def test_clean():
    """Run tests with no extra flags"""
    pytest.main(['--rootdir', '.'])

@cli.command("test_extra")
def test_extra():
    """Run tests with --setup-show (fixtures)"""
    pytest.main(['-rP','--verbose','--setup-show', '--rootdir', '.'])

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
