# -----------------------------------------------------------
# app/api/views.py
# Description:
# REST API endpoint definitions to handle
# labeling of comments, retrieving of comments, 
# as well as leaders, totals, and ability to ingest new comments.
#
# Usage:
# From front-end, can make queries to app.com/api/ENDPOINT
# All endpoints return either JSON or associated status code
# -----------------------------------------------------------
import json, random
from flask import render_template, redirect, Response,request, url_for, flash, g, jsonify, send_file
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import api
from .. import db
from ..models import User, Comment, Label



#-------------------------------------------------
# app.com/getComment
#-------------------------------------------------
# API endpoint that:
# Accesses associated user's current label_count,
# and then utilizes this label count as the index with which to pull 
# the next comment in the database.
# Currently this ensures every user looks at the same comments
#----
# Route queries the database for the next comment,
# if one exists, it is returned to the client.
# else client receives JSON response indicating all comments have been labeled.
#----------------------------------------------------------------------------
@api.route('/getComment', methods=['GET'])
@login_required
def getComment():
    label_count = current_user.label_count
    next_comment = Comment.query.get(label_count+1) 
    #if there is a next comment
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

#-----------------------------------------------------------
# app.com/saveComment
#-----------------------------------------------------------
# API endpoint that:
# Takes in POST request with JSON embedded into POST request's body
# that indicates the associated comment's id, label, and category
# We first pull the comment from the db using the given id,
# then we increment the current_user's label count (as they are assigning a new label)
# and finally, we create a new label, associate it with the comment and the user,
# and insert it into the db 
# Response is sent back with status 200 upon completion
#-------------------------------------------------------------
@api.route('/saveComment', methods=['POST'])
@login_required
def saveComment():
    # # commented out because not sure what it does. need to test to ensure it was neeeded
    # label_count = current_user.label_count
    # next_comment = Comment.query.get(label_count+1) 
    # if next_comment is None:
    #     resp = Response(status=200, mimetype='application/json')
    #     return resp
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

#-------------------------------------------
# app.com/leaderBoard
#---------------------------------------------
# API endpoint that takes a GET request,
# currently it pulls all users from the database,
# sorts them in descending order by number of labels,
# and returns this list as JSON back to the client.
#({'leaders': sorted_users})
#-----------------------------------------------------
@api.route('/leaderBoard', methods=['GET'])
@login_required
def leaderBoard():
    all_users = User.query.all()
    label_counted_users = [{'username':u.username, 'labelCount':len(u.labeled.all())} for u in all_users]
    sorted_users = sorted(label_counted_users, key=lambda user: user['labelCount'], reverse=True)
    resp = jsonify({'leaders': sorted_users})
    resp.status_code = 200
    return resp

#--------------------------------------------------------
# app.com/totals
#---------------------------------------------------------
# API endpoint that takes GET request,
# iterates through all users and comments,
# counting the total number of labels in the database, as well 
# as the total number of labels that are harassment.
# also counts total number of comments ingested into database.
# Returns this information as JSON 
# ({'total_labels': total_labels, 'harass_labels':harass_labels, 'total_comments':len(comments)})
#----------------------------------------------------------- 
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

#----------------------------------------------------------
# app.com/checkTwitter 
#----------------------------------------------------------
# API endpoint that returns JSON with 
# current_user's last recorded score for Twitter 
# {'score':score}
#----------------------------------------------------------
@api.route('/checkTwitter', methods=['GET'])
@login_required
def checkTwitter():
    score = current_user.twitter_score
    resp = jsonify({'score':score})
    resp.status_code = 200
    return resp

#-----------------------------------------------------------
# app.com/ingestTwitter
# ----------------------------------------------------------
# API endpoint that takes in a POST request with array of tweets embedded into 
# request's body. 
# We extract the tweets from the array, and ingest them directly into the database
#-----------------------------------------------------------
# WORK IN PROGRES:
# Currently I have added in a code stub to simulate interaction with 
# the classification model.
# This goes through the tweets, and randomly 'classifies' it as harassing or not.
# the unlucky comments get added to an array that is returned to the client
# along with the score ( num of non-harassing commnets / total number of comments) * 100
#--------------------------------------------------------------
# When NLP Model API is set-up,
# this method will have to forward the ingested tweets onto the model api
# receive the harassing tweets as well as the score from there, and forward them back to the client
#------------------------------------------------------
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
    

# *******************DEVELOPMENT ONLY ***************************
#------------------------------------------------------------------
# app.com/downloadComments
# -----------------------------------------------------------------
# *******************DEVELOPMENT ONLY ***************************
#-------------------------------------------------------------------
# This endpoint is currenlty used in development/testing 
# to generate a downloadable csv file of the current labeled comments
# This is used primarily as an easy menas to dump labelled data from 
# the analysts that have been labeling data for us using this application.
#-----------------------------------------------------------------------
# *******************DEVELOPMENT ONLY ***************************
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