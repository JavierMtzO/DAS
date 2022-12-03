from flask import Flask, jsonify, request, Response, session
from pymongo import MongoClient
from bson import json_util
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)

# Principio de Segregación de la Interfaz
# El dashboard de eventos es una interfaz totalmente independiente de la aplicación Twitter Reloaded
# Aunque el dashboard se vea afectado por la apliación, los usuarios de esta no hacen uso de las funciones
# del dashboard, por lo tanto, no es necesario de estén conectadas.

##### Connection to MongoDB #####

app.secret_key = 'key'
mongo = MongoClient("mongodb+srv://Gustavo:kUbunriOkGpWyAkT@cluster0.r0fukzf.mongodb.net/?retryWrites=true&w=majority")
db = mongo['Twitter_Reloaded']

##### Classes #####

# Principio de Responsabilidad Única:
# Se creó la clase Hash, la cual contiene funciones para encriptar y desencriptar contraseñas
# Gracias a esto, las funciones de crear usuario y verificar login tienen una sola responsabilidad
class Hash:
    def __init__(self, password):
        self.password = password
    def encrypt(self):
        return generate_password_hash(self.password)
    def decrypt(self, hashed_pass):
        return check_password_hash(hashed_pass, self.password)


class Event:
    def __init__(self, event_type):
        self.type = event_type
        self.user = session['username']
        self.timestamp = datetime.now()

    def register(self):
        db.events.insert_one(
                {"type":self.type,
                "user": self.user,
                "timestamp": self.timestamp})

class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
    def insert(self):
        return db.users.insert_one(
            {'username': self.username, 'email': self.email, 'password': self.password}).inserted_id
    def update(self, _id):
        db.users.update_one(
            {'_id': ObjectId(_id['$oid'])  if '$oid' in _id else ObjectId(_id)}, 
            {'$set': {'username': self.username, 'email': self.email, 'password': self.password}})

class Tweet:
    def __init__(self, user_id, username, content):
        self.user_id = user_id
        self.username = username
        self.content = content
    def insert(self):
        return db.tweets.insert_one({
                'user_id': self.user_id, 'username':self.username, 'content': self.content, 'timestamp': datetime.now(),
                }).inserted_id

# Principio de Sustitución de Liskov
# La única diferencia entre la clase 'ResponseTweet' y su clase padre 'Tweet' es que se modifica el método 'insert'
# Ambos cuentan con los mismos atributos, y si la clase heredada se sustituyera por la clase padre, aún funcionaría correctamente
class ResponseTweet(Tweet):
    def insert(self, parent):
        return db.tweets.insert_one({
                'user_id': self.user_id, 'username':self.username, 'content': self.content, 'parent': parent, 'timestamp': datetime.now(),
                }).inserted_id


##### Login / Logout Routes #####

# Decorators
# Todas las rutas utilizan un decorador que agrega nueva funcionalidad a la variable app, el cual es un objeto de tipo Flask
@app.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    if email and password:
        user = db.users.find_one({'email': email})
        hashpass = Hash(password)
        correct_login = hashpass.decrypt(user['password'])
        if correct_login:
            session['user_id'] = str(user['_id'])
            session['username'] = str(user['username'])
            response = json_util.dumps(session)
            new_event = Event("open_application")
            new_event.register()
            return Response(response, mimetype="application/json")
        return not_found()

@app.route('/logout', methods=['GET'])
def logout():
    session.pop("user_id", None)
    session.pop("username", None)
    return json_util.dumps({"Logout":"Success"})


##### User Routes #####

# Principio de Abierto/Cerrado
# Cada uno de los verbos HTTP para las rutas tiene una función propia.
# De esta manera, si se quiere agregar otro verbo, por ejemplo, un 'PATCH' a la ruta /users,
# se puede hacer agregando una función nueva, sin necesidad de modificar funciones existentes.
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
            return json_util.dumps({"Error":"Username or Email already in use."})
        
        hashpass = Hash(password)
        hashed_password = hashpass.encrypt()

        new_user = User(username, email, hashed_password)
        id = new_user.insert()

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
        hashpass = Hash(password)
        hashed_password = hashpass.encrypt()

        old_user = User(username, email, hashed_password)
        old_user.update(_id)

        response = jsonify({'message': 'User' + _id + 'Updated Successfuly'})
        response.status_code = 200
        return response
    else:
      return unauthorized()


##### Tweets Routes #####

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
    user_id = session['user_id']
    username = session['username']
    content = request.json['content']
    if 'parent' in request.json:
        parent = request.json['parent']
    else:
        parent = None
    if check_user(user_id) == False:
        return unauthorized()
    if user_id and username and content and len(content) <= 300:   
        if parent:
            new_tweet = ResponseTweet(user_id, username, content)
            id = new_tweet.insert(parent)
            response = jsonify({
                '_id': str(id),
                'user_id': user_id,
                'content': content,
                'parent': parent,
                'timestamp': datetime.now()
            })
            add_response_to_tweet(parent, id, content)
            new_event = Event("reply_tweet")
            new_event.register()
        else:
            new_tweet = Tweet(user_id, username, content)
            id = new_tweet.insert()
            response = jsonify({
                '_id': str(id),
                'user_id': user_id,
                'content': content,
                'timestamp': datetime.now()
            })
            new_event = Event("create_tweet")
            new_event.register()
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

##### Utils #####

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