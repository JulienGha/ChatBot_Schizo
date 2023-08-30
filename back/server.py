from flask import Flask, request, jsonify
from flask_cors import CORS
from rq import Queue
from workers import conn
from datetime import datetime
from pymongo import MongoClient
import os


app = Flask(__name__)
CORS(app)
q = Queue(connection=conn)


# Create a MongoDB client and establish a connection
client = MongoClient('localhost', 27017)
db = client['mydatabase']
collection = db['chats']


@app.route('/create', methods=['POST'])
def post_image():
    job = None

    # to ensure that our job_id is unique we use the current time
    unique_id = datetime.now().strftime("%Y%m%d%H%M%S")

    # Enqueue the image processing task
    temp_filename = unique_id
    # Our docker grants access to the data repository for our app
    job = q.enqueue(run_tesseract, temp_filename, job_id=unique_id)

    if job:
        return jsonify({"task_id": unique_id}), 202
    else:
        return jsonify({"error": "Failed to enqueue job"}), 500


@app.route('/resume', methods=['GET'])
def get_image():
    # Our front saved the job_id, when it sends a request to access the status of the detection it used that one
    task_id = request.args.get('task_id')
    if not task_id:
        return jsonify({"error": "task_id is required"}), 400

    job = q.fetch_job(task_id)
    if not job:
        return jsonify({"error": "No such task"}), 404

    if job.is_finished:
        return jsonify({"result": job.result}), 200
    else:
        return jsonify({"result": None}), 202


# test function to see if our client can send request
@app.route('/test', methods=['GET'])
def get_test():
    new_document = {"name": "John", "age": 30}
    collection.insert_one(new_document)
    return "good"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    client.close()

