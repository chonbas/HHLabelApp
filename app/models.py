import hashlib, sys
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request, url_for
from flask_login import UserMixin, AnonymousUserMixin
from . import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    return_user = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(128))
    labeled = db.relationship('Label', backref='labeler', lazy='dynamic')
    label_count = db.Column(db.Integer, default=0)
    facebook_data = db.Column(db.Boolean, default=False)
    twitter_data = db.Column(db.Boolean, default=False)
    google_data = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
    
    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password, salt_length=8)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class AnonymousUser(AnonymousUserMixin):
    pass 
    
login_manager.anonymous_user = AnonymousUser   

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    source = db.Column(db.String(64))
    labels = db.relationship('Label', backref='comment', lazy='dynamic')

class Label(db.Model):
    __tablename__ = 'labels'
    id = db.Column(db.Integer, primary_key=True)
    labeler_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    category = db.Column(db.String(64))
    harassment = db.Column(db.Boolean)
