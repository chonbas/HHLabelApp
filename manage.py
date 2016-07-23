# -----------------------------------------------------------
# manage.py
# Description:
# Framework to launch application in development environment.
#
# Usage:
# python manage.py runserver : runs server locally
# python manage.py start_db : resets database with specified seed file
# python manage.py prune_db :  remove different irrelevant comments from db
# python manage.py shell : interactive shell environment that allows database queries and 
# code testing
# python manage.py db : Migrate database to match new schema as specified in app/models.py
# -----------------------------------------------------------

import os
from app import create_app, db
from app.models import User, Comment
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand

app = create_app('default')

manager = Manager(app)
migrate = Migrate(app,db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Comment=Comment)


# -----------------------------------------------------------
# Function: start_db()
# Description:
# Drops existing database, and recreates models.
# Seeds database by pulling comments from csv file specified by 
# SEED_FILE_PATH.
# The file 'mini_test.csv' is included with only 3 comments for testing purposes.
# Usage:
# python manage.py start_db
# -----------------------------------------------------------
@manager.command
def start_db():
    SEED_FILE_PATH = 'mini_test.csv' 
    #SEED_FILE_PATH = 'rawseed.csv'
    import csv
    db.drop_all()
    db.create_all()
    with open(SEED_FILE_PATH) as csvfile:
        file = csv.reader(csvfile, delimiter=',', quotechar='"')
        row_ind = 0
        for row in file:
            if row_ind == 0:
                row_ind = 1
                continue
            if len(row) == 0:
                continue
            text = unicode(row[0], errors='replace')
            new_comment = Comment(body=text, source="reddit")
            db.session.add(new_comment)
    db.session.commit()
    return


# -----------------------------------------------------------
# Function: prune_Db
# Description:
# Prunes comments from database that match specified strings.
# Purpose is to remove comments from Reddit dump that do not include relevant
# comment data for labeling.
# Current rawseed.csv file is already pruned.
# Usage:
# python manage.py prune_db
# -----------------------------------------------------------
@manager.command
def prune_db():
    comments = Comment.query.all()
    for c in comments:
        if c.body == '[deleted]' or c.body == 'body' or c.body =='[removed]':
            db.session.delete(c)
    db.session.commit()

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
