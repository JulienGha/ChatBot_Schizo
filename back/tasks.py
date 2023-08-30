# tasks.py
import pymongo
import redis


def create_new_chat(chat_id, password):

    # Publish the chat ID to a Redis channel when the job is complete
    conn = redis.Redis(host='localhost', port=6379)
    conn.publish('chat_completed', chat_id)

    # Write chat ID and password to MongoDB
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['database']  # Replace with your actual database name
    chats_collection = db['chats']

    chat_data = {
        "chat_id": chat_id,
        "password": password
    }
    chats_collection.insert_one(chat_data)


def resume_chat(chat_id, password):
    # Publish the chat ID to a Redis channel when the job is complete
    conn = redis.Redis(host='localhost', port=6379)
    conn.publish('chat_completed', chat_id)

    # Write chat ID and password to MongoDB
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['database']  # Replace with your actual database name
    chats_collection = db['chats']



