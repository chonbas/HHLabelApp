import json
from flask import render_template, redirect, Response, request, url_for, flash, g, jsonify
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import auth
from .. import db
from ..models import User


@auth.route('/check', methods=['GET'])
def check():
    status = current_user.is_authenticated
    user = "" 
    if status:
        user = current_user.username
    resp = jsonify({'status':status, 'user':user})
    resp.status_code = 200
    return resp

@auth.route('/auth/toggleReturn', methods=['GET'])
@login_required
def toggleReturn():
    current_user.return_user = True
    db.session.commit()
    resp = Response(status=200)
    return resp


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

@auth.route('/auth/logout', methods=['GET'])
@login_required
def api_logout():
    logout_user()
    resp = Response(status=200)
    return resp