from flask import Flask, jsonify, request, Response, session
from pymongo import MongoClient
from bson import json_util
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.secret_key = 'key'
mongo = MongoClient("mongodb+srv://Gustavo:kUbunriOkGpWyAkT@cluster0.r0fukzf.mongodb.net/?retryWrites=true&w=majority")
db = mongo['Twitter_Reloaded']

#Login / Logout Routes

@app.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    if email and password:
        user = db.users.find_one({'email': email})
        correct_login = check_password_hash(user['password'], password)
        if correct_login:
            session['user_id'] = str(user['_id'])
            session['username'] = str(user['username'])
            response = json_util.dumps(session)
            db.events.insert_one(
                {"type":"open_application",
                "user": session['username'],
                "timestamp": datetime.now()})
            return Response(response, mimetype="application/json")
        return not_found()

@app.route('/logout', methods=['GET'])
def logout():
    session.pop("user_id", None)
    session.pop("username", None)
    return json_util.dumps({"Logout":"Success"})

# User Routes

@app.route('/users', methods=['GET'])
def get_users():
    users = db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype="application/json")

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = db.users.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(user)
    return Response(response, mimetype="application/json")

@app.route('/users', methods=['POST'])
def create_user():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    if username and email and password:
        username_exists = db.users.find_one({'username': username})
        email_exists = db.users.find({'email': email})
        if username_exists is not None and email_exists is not None:
            return not_found()
        hashed_password = generate_password_hash(password)
        id = db.users.insert_one(
            {'username': username, 'email': email, 'password': hashed_password}).inserted_id
        response = jsonify({
            '_id': str(id),
            'username': username,
            'password': password,
            'email': email
        })
        response.status_code = 201
        return response
    else:
        return not_found()

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    db.users.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'User ' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response

@app.route('/users/<_id>', methods=['PUT'])
def update_user(_id):
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    if username and email and password and _id:
        hashed_password = generate_password_hash(password)
        db.users.update_one(
            {'_id': ObjectId(_id['$oid'])  if '$oid' in _id else ObjectId(_id)}, 
            {'$set': {'username': username, 'email': email, 'password': hashed_password}})
        response = jsonify({'message': 'User' + _id + 'Updated Successfuly'})
        response.status_code = 200
        return response
    else:
      return unauthorized()


# Tweets Routes

@app.route('/tweets', methods=['GET'])
def get_tweets():
    tweets = db.tweets.find()
    response = json_util.dumps(tweets)
    return Response(response, mimetype="application/json")

@app.route('/tweets/<id>', methods=['GET'])
def get_tweet(id):
    user = db.tweets.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(user)
    return Response(response, mimetype="application/json")

@app.route('/newtweets', methods=['GET'])
def get_new_tweets():
    new_tweets = db.tweets.find({"parent":{"$exists":False}}).sort("timestamp", -1).limit(10)
    response = json_util.dumps(new_tweets)
    return Response(response, mimetype="application/json")

@app.route('/tweets', methods=['POST'])
def create_tweet():
    user_id = request.json['userId']
    username = request.json['username']
    content = request.json['content']
    if 'parent' in request.json:
        parent = request.json['parent']
    else:
        parent = None
    # if check_user(user_id) == False:
        # return unauthorized()
    if user_id and username and content and len(content) <= 300:   
        if parent:
            id = db.tweets.insert_one({
                'user_id': user_id, 'username':username, 'content': content, 
                'parent': parent, 'timestamp': datetime.now()
                }).inserted_id
            response = jsonify({
                '_id': str(id),
                'user_id': user_id,
                'content': content,
                'parent': parent,
                'timestamp': datetime.now()
            })
            add_response_to_tweet(parent, id, content)
            db.events.insert_one(
                {"type":"reply_tweet",
                "user": session['username'],
                "timestamp": datetime.now()})
        else:
            id = db.tweets.insert_one({
                'user_id': user_id, 'username':username, 'content': content, 'timestamp': datetime.now()
                }).inserted_id
            response = jsonify({
                '_id': str(id),
                'user_id': user_id,
                'content': content,
                'timestamp': datetime.now()
            })
            db.events.insert_one(
                {"type":"create_tweet",
                "user": request.json['username'],
                "timestamp": datetime.now()})
        add_tweet_to_user(user_id, id, content)
        response.status_code = 201
        return response
    else:
        return not_found()

@app.route('/tweets/<id>', methods=['DELETE'])
def delete_tweet(id):
    tweet = db.tweets.find_one({'_id': ObjectId(id)})
    if check_user(tweet['user_id']) == False:
        return unauthorized()
    db.tweets.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Tweet ' + id + ' Deleted Successfully'})
    response.status_code = 200
    delete_tweet_from_user(id)
    delete_response_from_tweet(id)
    return response

# Utils

def add_tweet_to_user(user_id, tweet_id, content):
    _id = ObjectId(user_id)
    db.users.update_one({"_id":_id}, {"$addToSet": {"tweets": {"tweet_id": tweet_id, "content": content}}})

def delete_tweet_from_user(tweet_id):
    _id = ObjectId(tweet_id)
    db.users.update_one({}, {"$pull": {"tweets": {"tweet_id": _id}}})

def add_response_to_tweet(parent_id, tweet_id, content):
    _id = ObjectId(parent_id)
    db.tweets.update_one({"_id":_id}, {"$addToSet": {"responses": {"response_id": tweet_id, "content": content}}})

def delete_response_from_tweet(tweet_id):
    _id = ObjectId(tweet_id)
    db.tweets.update_one({}, {"$pull": {"responses": {"response_id": _id }}})

def check_user(user_id):
    if ("user_id" not in session) or (user_id != session['user_id']):
        return False
    else:
        return True
    

# Page Unauthorized
@app.errorhandler(401)
def unauthorized(error=None):
    message = {
        'message': 'Unauthorized: Cannot Access Resource ' + request.url,
        'status': 401
    }
    response = jsonify(message)
    response.status_code = 401
    return response


# Page Not Found
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == "__main__":
    app.run(debug=True, port=3001)