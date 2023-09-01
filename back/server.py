from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
# from rq import Queue
# from workers import conn
from datetime import datetime, timedelta
from pymongo import MongoClient
import bcrypt
import jwt
from functools import wraps
from tasks import create_new_chat
import uuid
import random
import string
import os


app = Flask(__name__)
CORS(app, supports_credentials=True)
# q = Queue(connection=conn)


# Create a MongoDB client and establish a connection
client = MongoClient('localhost', 27017)
db = client['mydatabase']
collection = db['chats']


# Your JWT secret key
JWT_SECRET = "345TGHIOPUYFRDFGJNCB81234RVB9HB99YNXZXA0AXHBXLPM"


def verify_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        chat_id = request.json.get('chatId')
        chat_data = collection.find_one({"chat_id": chat_id})
        stored_jwt = chat_data.get('jwt_key')
        print(stored_jwt)

        auth_token = request.cookies.get('authToken')
        print(auth_token)
        if not auth_token:
            return jsonify({"error": "Missing token"}), 401

        try:
            payload = jwt.decode(auth_token, stored_jwt, algorithms=['HS256'])
            # You can access the payload data here, e.g., payload['user_id']
            # You can also store the payload in the request context for further processing
            request.current_user = payload
        except jwt.ExpiredSignatureError:
            print("la")
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            print("koko")
            return jsonify({"error": "Invalid token"}), 401

        return func(*args, **kwargs)

    return wrapper


def generate_unique_id():
    unique_id = str(uuid.uuid4().hex)
    random_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    return unique_id + random_chars


@app.route('/create', methods=['POST'])
def create_chat():

    # Generate unique chat ID
    date = datetime.now().strftime("%Y%m%d%H%M%S")

    # Encrypt password
    password = request.json.get('password')  # Get password from request
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Enqueue the image processing task
    unique_id = date

    chat_data = {
        "chat_id": unique_id,
        "password": hashed_password,
        "jwt_key": generate_unique_id()
    }
    collection.insert_one(chat_data)

    # Generate JWT token
    expiration = datetime.utcnow() + timedelta(hours=1)  # Set token expiration time
    payload = {
        "chat_id": unique_id,
        "exp": expiration
    }
    token = jwt.encode(payload, chat_data.get('jwt_key'), algorithm='HS256')

    # Create response with JWT cookie
    response = make_response(jsonify({"chatId": unique_id,
                                      "token": token,
                                      "exp": expiration}), 200)

    """job = None
            job = q.enqueue(create_new_chat, unique_id, hashed_password, job_id=unique_id)  # Replace with your task function
        else:
            return jsonify({"error": "Failed to enqueue job"}), 500"""

    return response


@app.route('/resume', methods=['POST'])
def resume_chat():

    chat_id = request.json.get('chatId')
    password = request.json.get('password')

    # Retrieve chat data from MongoDB based on chat_id
    chat_data = collection.find_one({"chat_id": chat_id})

    if chat_data:
        stored_password = chat_data.get('password')
        stored_jwt = chat_data.get('jwt_key')

        # Verify password using bcrypt
        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            # Generate and send JWT as a cookie
            expiration = datetime.utcnow() + timedelta(hours=1)  # Set token expiration time
            payload = {
                "chat_id": str(chat_data['_id']),
                "exp": expiration
            }
            token = jwt.encode(payload, stored_jwt, algorithm='HS256')
            # Create response with JWT cookie
            response = make_response(jsonify({"chatId": chat_id,
                                              "token": token,
                                              "exp": expiration}), 200)

            return response, 200
        else:
            return jsonify({"message": "Invalid password"}), 401
    else:
        return jsonify({"message": "Chat not found"}), 404


@app.route('/test_cookie', methods=['POST'])
@verify_token
def test_cookie():
    # You can access the authenticated user's payload using request.current_user
    # Process the request and return the response
    return jsonify({"message": "Credential Test Successful"})


# test function to see if our client can send request
@app.route('/test', methods=['GET'])
def get_test():
    return "good"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    client.close()

