from flask.cli import FlaskGroup

from app import create_app, db

import pytest

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command('recreate_db')
def recreate_db():
    from app.models.ItemModel import Item
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command('show')
def show():
    for x in app.config:
        print(x)


@cli.command('populate_Posts')
def populate_Posts():
    from app.models.post import Post
    post_list = [{'title': 'Jakub', 'content': 'Turek'},
                 {'title': 'RObson', 'content': 'Ama'},
                 {'title': 'ema', 'content': 'fyfą'}]
    for x in post_list:
        db.session.add(Post(title=x['title'], content=x['content']))
        db.session.commit()

@cli.command('add_Item')
def add_Item():
    itemId = input("Podaj Id itemu:")
    from app.repository.ItemRepository import addItem
    addItem(itemId, 'test', True, 9.99, "www.google.com")


@cli.command('get_Item')
def get_Item():
    from app.repository.ItemRepository import getItem
    getItem('1234')


@cli.command('get_AllItems')
def get_AllItems():
    from app.repository.ItemRepository import getAllItems
    getAllItems()

@cli.command('del_Item')
def del_Item():
    from app.repository.ItemRepository import deleteItem
    itemId = input("Podaj Id itemu:")
    deleteItem(itemId)

@cli.command('del_AllItems')
def del_AllItems():
    from app.repository.ItemRepository import deleteAllItems
    deleteAllItems()

@cli.command('update_Item')
def update_Item():
    from app.repository.ItemRepository import updateItem
    itemId = input("Podaj Id itemu:")
    updateItem(itemId,True,9.5)

@cli.command("test")
def test():
    """Run tests
    --verbose - shows folders
    -rP - shows printouts from tests #can be deleted later#"""
    pytest.main(['-rP','--verbose', '--rootdir', '.'])


if __name__ == '__main__':
    cli()