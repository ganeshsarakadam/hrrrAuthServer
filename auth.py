from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token
from flask_pymongo import PyMongo
from datetime import timedelta
from bson.json_util import dumps
from bson.objectid import ObjectId

authServerApp = Flask(__name__)

authServerApp.config['JWT_SECRET_KEY'] = 'hrrr-weather-lawn'  

# TBD Change this
# authServerApp.config['JWT_SECRET_KEY'] = 'hrrr-weather-lawn'  
authServerApp.config["MONGO_URI"] = "mongodb://mongo:27017/lawnUsers"
# authServerApp.config["MONGO_URI"] = "mongodb://localhost:27017/lawnUsers"


jwt = JWTManager(authServerApp) 
mongo = PyMongo(authServerApp)

@authServerApp.route('/token', methods=['POST'])
def login():
    username = request.json.get('username', None)
    # print("username", username)
    user = mongo.db.myCollection.find_one({"username": username})
    # print("User from MongoDB:", user)
    if user is None:
        return jsonify({"msg": "user not found"}), 401

    access_token = create_access_token(identity=username, expires_delta=timedelta(minutes=8))
    return access_token

if __name__ == '__main__':
    authServerApp.run(host="0.0.0.0", port=4200, debug=True)
