import json, random
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
        next_source = next_comment.source
    else:
        next_body = "Congratulations you have labeled all available comments."
        next_id =-1 #flag to prevent future queries
        next_source = ''
    resp = jsonify({'body':next_body, 'id':next_id, 'count':label_count, 'source':next_source})
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
    score = current_user.twitter_score
    resp = jsonify({'score':score})
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
    #######
    ####### STUBBING 
    ####### Actual score should be calculated by classifier api (not yet setup)
    ####### inefficient double loop is only to highlight that this is stubbing
    harassing_tweets = []
    for tweet in data:
        random_num = random.randint(0,100)
        if random_num >= 80:
            harassing_tweets.append(tweet)
    num_ingested_tweets = len(data)
    num_normal_tweets = num_ingested_tweets - len(harassing_tweets)
    percent_score = float(num_normal_tweets) / float(num_ingested_tweets)
    twitter_score = int(100 * percent_score)
    current_user.twitter_score = twitter_score
    db.session.commit()
    resp = jsonify({'score':twitter_score, 'tweets':harassing_tweets})
    resp.status_code = 200
    ##########
    ###########
    ##
    #/endstub
    # resp = Response(status=200, mimetype='application/json')
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