import os

if os.path.exists('.env'):
    print('Importing environment from .env ...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

from app import create_app, db
from app.models import User, Comment
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand

app = create_app('production')

manager = Manager(app)
migrate = Migrate(app,db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Comment=Comment)

@manager.command
def start_db():
    import csv
    db.create_all()
    with open('reddit_downvoted_15k.csv') as csvfile:
        file = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in file:
            if len(row) == 0:
                continue
            text = unicode(row[0], errors='replace')
            new_comment = Comment(body=text)
            db.session.add(new_comment)
    db.session.commit()
    return

@manager.command
def prune_db():
    comments = Comment.query.all()
    for c in comments:
        if c.body == '[deleted]' or c.body == 'body':
            db.session.delete(c)
    db.session.commit()

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
