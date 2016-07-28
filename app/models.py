# -----------------------------------------------------------
# File: app/models.py
#
# Description:
# This file specifies the database schema/models.
# Currently three models and related tables are specified:
# Users
# Comments
# Labels
# Usage:
# These models are inserted into the database through SQLAlchemy
#
# For specific documentation on Flask-SQLAlchemy:
# Visit: http://flask-sqlalchemy.pocoo.org/2.1/
#
# Quick Reference:
#---------------------------------------------------------------
# To QUERY:
# user = User.query.get(ID)
#   - This queries the User table and extracts the object associated with
#       given ID.
#   - If no object found with matching ID, none is returned
# user = User.query.filter_by(username='SOMEUSER').first()
#   - Queries User table for a user whose username contains the specified string.
#   - the final first() function specifies to only pull the first item matching this query
# users = User.query.all()
#   -Pulls all users from the table and returns a list of user objects
# Of note, all user/comment/label objects are interactalbe as Python objects
# thanks to SQLAlchemy.
# ie:
# user = User.query.get(ID)
# username = user.username
# label_count = user.label_count
# To pull a user's labels, however, we need to go an extra step:
# users_labels = user.labeled.all()
# ^users_labels is now a list of Label objects associated with this user
# THe reason for this is that the labels are set as a dynamic relationship with the users
# As such, the user object only stores a Query object that needs to be exectued before having
# access to the specific labels.
#
# -----------------------------------------------------------------
# To UPDATE:
# user = User.query.get(ID)
# new_username = 'NEWUSER'
# user.username = new_username
# db.session.commit()
# ----------------------------------------------------------
# To INSERT:
# user = User(email='a@b.c', username='usersname', password='password')
# db.session.add(user)
# db.session.commit()
#--------------------------------------------------------------
# To DELETE:
# user = User.query.get(ID)
# db.session.delete(user)
# db.sesion.commit()
#-----------------------------------------------------------------------------

import hashlib, sys
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request, url_for
from flask_login import UserMixin, AnonymousUserMixin
from . import db, login_manager


# User Model:
# ------------------------------------
# Specifies fields for User table/object
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True) 
    return_user = db.Column(db.Boolean, default=False) #flag if return user  used to check if tutorial is required on login
    password_hash = db.Column(db.String(128)) #password hash
    labeled = db.relationship('Label', backref='labeler', lazy='dynamic') #array of queries tied to labels assigned
    label_count = db.Column(db.Integer, default=0) #count of how many labels a user has made
    twitter_score = db.Column(db.Integer) #store last computed twitter score so user can refer to it
    twitter_recent_id = db.Column(db.String(64), default='') #store most recent tweet_id to ensure no duplicats ingested


    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
    
    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')
    
    #@password.setter
    #---------------------------------------------------
    #When a new user is created, or when a new password is specified,
    #This takes int he plain-text password, concatenates it with a 
    #unique crypto secure pseudo randomly generated salt 
    #and then hashes it to ensure user security.
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password, salt_length=8)

    #user.verify_password(TESTPASSWORD)
    #----------------------------------------------
    # Method to take in a plaintext password, hash and salt it and compare it to the stored password
    # Returns true if valid, false else
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

#AnonymousUser Class is utilized by our Login-Manager
#To keep track of non-logged in users.
#This is required to be able to differentiate betweetn users that are and are not authenticated
class AnonymousUser(AnonymousUserMixin):
    pass 
    
login_manager.anonymous_user = AnonymousUser   

#Loads a user as the active logged in user to the session
#In order to utilize this method:
#This method is used by the login_manager and should NOT be called
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#Comment Model:
#-----------------------------------
#Specifies schema for comment objects
class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    source = db.Column(db.String(64)) #string to store source - currently 'reddit' or 'twitter', used to render source icon
    labels = db.relationship('Label', backref='comment', lazy='dynamic')# establishes dynamic relationship to labels associated with this comment


#Label Model:
# -----------------------------------
# Specifies schema for Label objects
class Label(db.Model):
    __tablename__ = 'labels'
    id = db.Column(db.Integer, primary_key=True)
    labeler_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    category = db.Column(db.String(64)) #string to store specific categorical label for harassment comments
    harassment = db.Column(db.Boolean)
