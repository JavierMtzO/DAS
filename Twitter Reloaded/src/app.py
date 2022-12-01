from flask import Flask, jsonify, request, Response
from pymongo import MongoClient
from bson import json_util
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = 'key'
mongo = MongoClient("mongodb+srv://Gustavo:kUbunriOkGpWyAkT@cluster0.r0fukzf.mongodb.net/?retryWrites=true&w=majority")
db = mongo['Twitter_Reloaded']


# User Routes

@app.route('/users', methods=['GET'])
def get_users():
    users = db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype="application/json")

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = db.users.find_one({'_id': ObjectId(id)})
    # print(user[0]._id)
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
      return not_found()


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

@app.route('/tweets', methods=['POST'])
def create_tweet():
    user_id = request.json['user_id']
    content = request.json['content']
    if user_id and content and len(content) <= 300:   
        id = db.tweets.insert_one(
            {'user_id': user_id, 'content': content}).inserted_id
        response = jsonify({
            '_id': str(id),
            'user_id': user_id,
            'content': content
        })
        add_tweet_to_user(user_id, id)
        response.status_code = 201
        return response
    else:
        return not_found()

@app.route('/tweets/<id>', methods=['DELETE'])
def delete_tweet(id):
    db.tweets.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Tweet ' + id + ' Deleted Successfully'})
    response.status_code = 200
    delete_tweet_from_user(id)
    return response


# Response Tweets Routes

@app.route('/restweets', methods=['GET'])
def get_response_tweets():
    restweets = db.restweets.find()
    response = json_util.dumps(restweets)
    return Response(response, mimetype="application/json")

@app.route('/restweets/<id>', methods=['GET'])
def get_response_tweet(id):
    user = db.restweets.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(user)
    return Response(response, mimetype="application/json")

@app.route('/restweets', methods=['POST'])
def create_response_tweet():
    user_id = request.json['user_id']
    content = request.json['content']
    parent = request.json['parent']
    if user_id and content and len(content) <= 300:   
        id = db.restweets.insert_one(
            {'user_id': user_id, 'content': content, 'parent': parent}).inserted_id
        response = jsonify({
            '_id': str(id),
            'user_id': user_id,
            'content': content,
            'parent': parent
        })
        add_tweet_to_user(user_id, id)
        add_response_to_tweet(parent, id)
        response.status_code = 201
        return response
    else:
        return not_found()

@app.route('/restweets/<id>', methods=['DELETE'])
def delete_response_tweet(id):
    db.restweets.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Tweet ' + id + ' Deleted Successfully'})
    response.status_code = 200
    delete_tweet_from_user(id)
    delete_response_from_tweet(id)
    return response

# Utils

def add_tweet_to_user(user_id, tweet_id):
    _id = ObjectId(user_id)
    db.users.update_one({"_id":_id}, {"$addToSet": {"tweets": tweet_id}})

def delete_tweet_from_user(tweet_id):
    _id = ObjectId(tweet_id)
    db.users.update_one({}, {"$pull": {"tweets": _id}})

def add_response_to_tweet(parent_id, tweet_id):
    _id = ObjectId(parent_id)
    db.tweets.update_one({"_id":_id}, {"$addToSet": {"responses": tweet_id}})

def delete_response_from_tweet(tweet_id):
    _id = ObjectId(tweet_id)
    db.tweets.update_one({}, {"$pull": {"responses": _id}})



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
    app.run(debug=True, port=3000)