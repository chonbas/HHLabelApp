import json
from flask import render_template, redirect, Response,request, url_for, flash, g, jsonify, send_file
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import api
from .. import db
from ..models import User, Comment, Label

@api.route('/getComment', methods=['GET'])
@login_required
def getComment():
    label_count = current_user.label_count
    next_comment = Comment.query.get(label_count+1) 
    if next_comment is not None:
        next_body = next_comment.body
        next_id = next_comment.id
    else:
        next_body = "Congratulations you have labeled all available comments."
        next_id =-1 #flag to prevent future queries
    resp = jsonify({'body':next_body, 'id':next_id, 'count':label_count})
    resp.status_code = 200
    return resp

@api.route('/saveComment', methods=['POST'])
@login_required
def saveComment():
    label_count = current_user.label_count
    next_comment = Comment.query.get(label_count+1) 
    if next_comment is None:
        resp = Response(status=200, mimetype='application/json')
        return resp
    data = json.loads(request.data.decode())
    comment_id = data['comment_id']
    comment_update = Comment.query.filter_by(id=comment_id).first()
    current_user.label_count += 1
    new_label = Label(harassment =  data['label'], category = data['category'])
    new_label.comment = comment_update
    new_label.labeler = current_user
    db.session.add(new_label)
    db.session.commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


@api.route('/leaderBoard', methods=['GET'])
@login_required
def leaderBoard():
    all_users = User.query.all()
    label_counted_users = [{'username':u.username, 'labelCount':len(u.labeled.all())} for u in all_users]
    sorted_users = sorted(label_counted_users, key=lambda user: user['labelCount'], reverse=True)
    resp = jsonify({'leaders': sorted_users})
    resp.status_code = 200
    return resp
        
@api.route('/totals', methods=['GET'])
@login_required
def getTotals():
    all_users = User.query.all()
    comments = Comment.query.all()
    total_labels = 0
    harass_labels = 0
    for u in all_users:
         labels = u.labeled.all()
         total_labels += len(labels)
         for l in labels:
             if l.harassment:
                 harass_labels += 1
    resp = jsonify({'total_labels': total_labels, 'harass_labels':harass_labels, 'total_comments':len(comments)})
    resp.status_code = 200
    return resp

@api.route('/checkTwitter', methods=['GET'])
@login_required
def checkTwitter():
    status = current_user.twitter_data
    resp = jsonify({'status':status})
    resp.status_code = 200
    return resp

@api.route('/checkFb', methods=['GET'])
@login_required
def checkFB():
    status = current_user.facebook_data
    resp = jsonify({'status':status})
    resp.status_code = 200
    return resp

@api.route('/ingestTwitter', methods=['POST'])
@login_required
def ingestTwitter():
    data = json.loads(request.data.decode())
    for tweet in data:
        new_comment = Comment(body=tweet['body'], source='twitter')
        db.session.add(new_comment)
    current_user.twitter_data = True
    db.session.commit()
    resp = Response(status=200, mimetype='application/json')
    return resp
    

@api.route('/downloadComments', methods=['GET'])
@login_required
def downloadComments():
    import csv, os
    with open('currentDump.csv', 'wb') as csvfile:
        csvfile.truncate()
        fieldnames = ['body']
        users = User.query.all()
        for i in xrange(0, len(users)):
            fieldnames.append('label_' + str(i))
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        comments = Comment.query.all()
        for c in comments:
            labels = c.labels.all()
            try:
                row = {fieldnames[0]:c.body}
                for i in xrange(0, len(labels)):
                    row[fieldnames[i+1]] = labels[i].harassment
                writer.writerow(row)
            except(UnicodeEncodeError):
                pass
    basedir = os.path.abspath(os.path.dirname(__file__))[:-7]
    return send_file(basedir+'currentDump.csv')