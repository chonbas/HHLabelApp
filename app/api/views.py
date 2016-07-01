import json
from flask import render_template, redirect, Response,request, url_for, flash, g, jsonify, send_file
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import api
from .. import db
from ..models import User, Comment

@api.route('/getComment', methods=['GET'])
@login_required
def getComment():
    next_comment = Comment.query.filter_by(label = None).first()
    label_count = len(current_user.labeled.all())
    resp = jsonify({'body':next_comment.body, 'id':next_comment.id, 'count':label_count})
    resp.status_code = 200
    return resp

@api.route('/saveComment', methods=['POST'])
@login_required
def saveComment():
    data = json.loads(request.data.decode())
    comment_id = data['comment_id']
    comment_update = Comment.query.filter_by(id=comment_id).first()
    comment_update.label = data['label']
    comment_update.labeler = current_user
    db.session.commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


@api.route('/leaderBoard', methods=['GET'])
@login_required
def leaderBoard():
    all_users = User.query.all()
    label_counted_users = [{'username':u.username, 'labelCount':len(u.labeled.all())} for u in all_users]
    sorted_users = sorted(label_counted_users, key=lambda user: user['labelCount'], reverse=True)
    total = 0
    harass = 0
    for u in sorted_users:
        total += u['labelCount']
    for u in all_users:
        comments = u.labeled.all()
        for c in comments:
            if c.label == "Harassment":
                harass += 1
    resp = jsonify({'leaders': sorted_users, 'total':total, 'harass':harass})
    resp.status_code = 200
    return resp
        


@api.route('/downloadComments', methods=['GET'])
@login_required
def downloadComments():
    import csv, os
    with open('currentDump.csv', 'wb') as csvfile:
        csvfile.truncate()
        fieldnames = ['body', 'label','labeler']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        comments = Comment.query.all()
        for c in comments:
            if c.label is not None:
                try:
                    writer.writerow({fieldnames[0]:c.body, fieldnames[1]:c.label, fieldnames[2]:c.labeler.username})
                except(UnicodeEncodeError):
                    pass
    basedir = os.path.abspath(os.path.dirname(__file__))[:-7]
    return send_file(basedir+'currentDump.csv')


    
