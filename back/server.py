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


def verify_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        # Determine the method and extract chat_id accordingly
        if request.method == 'POST':
            chat_id = request.json.get('chat_id')
        elif request.method == 'GET':
            chat_id = request.args.get('chat_id')
        elif request.method == 'PATCH':
            chat_id = request.json.get('chat_id')
        else:
            return jsonify({"error": "Unsupported HTTP method"}), 400

        chat_data = collection.find_one({"chat_id": chat_id})
        stored_jwt = chat_data.get('jwt_key')

        auth_token = request.cookies.get('authToken')

        if not auth_token:
            return jsonify({"error": "Missing token"}), 401

        try:
            payload = jwt.decode(auth_token, stored_jwt, algorithms=['HS256'])
            request.current_user = payload
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
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
        "jwt_key": generate_unique_id(),
        "messages": []
    }
    collection.insert_one(chat_data)

    # Generate JWT token
    expiration = datetime.utcnow() + timedelta(hours=24)  # Set token expiration time
    payload = {
        "chat_id": unique_id,
        "exp": expiration
    }
    token = jwt.encode(payload, chat_data.get('jwt_key'), algorithm='HS256')

    # Create response with JWT cookie
    response = make_response(jsonify({"chat_id": unique_id,
                                      "token": token,
                                      "exp": expiration}), 200)

    """job = None
            job = q.enqueue(create_new_chat, unique_id, hashed_password, job_id=unique_id)  # Replace with your task function
        else:
            return jsonify({"error": "Failed to enqueue job"}), 500"""

    return response


@app.route('/resume', methods=['POST'])
def resume_chat():

    chat_id = request.json.get('chat_id')
    password = request.json.get('password')

    # Retrieve chat data from MongoDB based on chat_id
    chat_data = collection.find_one({"chat_id": chat_id})

    if chat_data:
        stored_password = chat_data.get('password')
        stored_jwt = chat_data.get('jwt_key')

        # Verify password using bcrypt
        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            # Generate and send JWT as a cookie
            expiration = datetime.utcnow() + timedelta(hours=24)  # Set token expiration time
            payload = {
                "chat_id": str(chat_data['_id']),
                "exp": expiration
            }
            token = jwt.encode(payload, stored_jwt, algorithm='HS256')
            # Create response with JWT cookie
            response = make_response(jsonify({"chat_id": chat_id,
                                              "token": token,
                                              "exp": expiration}), 200)

            return response, 200
        else:
            return jsonify({"message": "Invalid password"}), 401
    else:
        return jsonify({"message": "Chat not found"}), 404


@app.route('/get_messages', methods=['GET'])
@verify_token
def get_messages():
    chat_id = request.args.get('chat_id')
    chat_data = collection.find_one({"chat_id": chat_id})

    # Extract messages field from the MongoDB document and return it
    messages = chat_data.get("messages", [])

    return jsonify({"messages": messages})


@app.route('/post_messages', methods=['POST'])
@verify_token
def post_messages():
    chat_id = request.json.get('chat_id')
    message_content = request.json.get('message')  # Assuming message is part of request JSON
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Format it as you like

    new_message = {
        "user": "user",
        "content": message_content,
        "date": current_date
    }

    # Add the new message to the 'messages' field in the MongoDB document
    collection.update_one({"chat_id": chat_id}, {"$push": {"messages": new_message}})

    return jsonify({"status": "Message added",
                    "date": current_date})


# test function to see if our client can send request
@app.route('/test', methods=['GET'])
def get_test():
    return "good"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    client.close()

