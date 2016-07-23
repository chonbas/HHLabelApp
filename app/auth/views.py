# -----------------------------------------------------------
# app/auth/views.py
# Description:
# REST API endpoint definitions for authentication. 
# Handles login, logout, registrations, and means to check session
# for active logged in user.
#
# Usage:
# From front-end, can make queries to app.com/auth/ENDPOINT
# All endpoints return either JSON or associated status code
# -----------------------------------------------------------
import json
from flask import render_template, redirect, Response, request, url_for, flash, g, jsonify
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import auth
from .. import db
from ..models import User

#-----------------------------------------------
# app.com/check
#-----------------------------------------------
# Provides queryable endpoint so back-end can read session information from request,
# access session state, and determine if a user is logged in or not.
# Returns JSON ({status: [TRUE/FALSE depending on user authentication, 
#               user: USERNAME of logged in user, if one is logged in]})
#
@auth.route('/check', methods=['GET'])
def check():
    status = current_user.is_authenticated
    user = "" 
    if status:
        user = current_user.username
    resp = jsonify({'status':status, 'user':user})
    resp.status_code = 200
    return resp

#-------------------------------------------------
# app.com/auth/toggleReturn
#-------------------------------------------------
# Endpoint used by client to flag that this user has gone through the entire
# onboarding/tutorial process.
#--------------------------------------------
@auth.route('/auth/toggleReturn', methods=['GET'])
@login_required
def toggleReturn():
    current_user.return_user = True
    db.session.commit()
    resp = Response(status=200)
    return resp

#---------------------------------------------------
# app.com/auth/register
#---------------------------------------------------
# Endpoint used for registration.
# Takes in a POST request with form data embedded as JSON 
# in the request's body.
# Parses the form data out of the request body,
# checks to see if email is in use (if it is returns status indicating this)
# checks to see if username taken (if it is returns status indicating this)
# If both checks are passed, then new user is created and inserted into database
#---------------------------------------------------
@auth.route('/auth/register', methods=['POST'])
def api_register():
    data = json.loads(request.data.decode())
    email_test = User.query.filter_by(email=data['email']).first()
    if email_test is not None:
        resp = jsonify({'status':'email_in_use'})
        resp.status_code = 200
        return resp
    user_test  = User.query.filter_by(username=data['username']).first()
    if user_test is not None:
        resp = jsonify({'status':'user_in_use'})
        resp.status_code = 200
        return resp
    user = User(email=data['email'],
                username=data['username'],
                password=data['password'])
    db.session.add(user)
    db.session.commit()
    resp = jsonify({'status':'success'})
    resp.status_code = 200
    return resp

#------------------------------------------------------
# app.com/auth/login 
#-------------------------------------------------------
#Endpoint used by client to login a user.email
#Takes in a POST request with login-form data embedded as JSON into
#request body.
#Parses form data out of the request body, 
#Then chekcs to see username given exists,
# and password matches associated user's password,
#if this check passes, user is logged in and 
#response is sent back with JSON indicating 
#logged in user's username as well as their onboarding/tutorial status 
#(ie, are they a new or returning user)
#---
#If username does not exist or passsword is incorrect,
#sends JSON back indicating False for logged in success status.
#------------------------------------------------
@auth.route('/auth/login', methods=['POST'])
def api_login():
    data = json.loads(request.data.decode())
    user = User.query.filter_by(email=data['email']).first()
    if user is not None and user.verify_password(data['password']):
        login_user(user, data['remember_me'])
        resp = jsonify({'status':True, 'user':user.username, 'return':user.return_user})
        resp.status_code = 200
        return resp
    resp = jsonify({'status':False})
    resp.status_code = 200
    return resp
    
#-------------------------------------------------------------
# app.com/auth/logout 
#------------------------------------------------------------
#Endpoint used by client to log a user out
#Simply logs out the user specified by the session 
#that is referenced in the request.
@auth.route('/auth/logout', methods=['GET'])
@login_required
def api_logout():
    logout_user()
    resp = Response(status=200)
    return resp