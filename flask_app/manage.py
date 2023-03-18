from flask.cli import FlaskGroup

from app import create_app, db

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command('recreate_db')
def recreate_db():
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


if __name__ == '__main__':
    cli()
