from pymongo import MongoClient
import constants
import os
from flask import Flask, request, jsonify

MONGO_URI = os.getenv("MONGO_URI", constants.MONGO_URL)
client = MongoClient(MONGO_URI)
db = client[constants.DB_NAME]
logs_collection = db[constants.COLLECTION_NAME] 

app = Flask(__name__)

@app.route("/logs/<service_name>", methods=["GET"])
def get_logs_by_service(service_name):
    log_list = list()
    for log in logs_collection.find({"service": service_name}):
        log["_id"] = str(log["_id"])
        log_list.append(log)
    return jsonify({"message": "Logs retrieved successfully", "logs": log_list})

@app.route("/logs/<service_name>/<severity>", methods=["GET"])
def get_logs_by_service_and_severity(service_name, severity):
    log_list = list()
    for log in logs_collection.find({"service": service_name, "severity": severity}):
        log["_id"] = str(log["_id"])
        log_list.append(log)
    return jsonify({"message": "Logs retrieved successfully", "logs": log_list})

if __name__ == "__main__":
    app.run(host="localhost", port=5000)

