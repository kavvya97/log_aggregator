import constants
from pymongo import MongoClient
import os
import schedule
import time
from datetime import datetime, timedelta


MONGO_URI = os.getenv("MONGO_URI", constants.MONGO_URL)
client = MongoClient(MONGO_URI)
db = client[constants.DB_NAME]
logs_collection = db[constants.COLLECTION_NAME] 

def remove_old_logs():
    cutoff_time = datetime.now() - timedelta(days=constants.RETENTION_DAYS)
    logs_collection.delete_many({"timestamp": {"$lt": cutoff_time}})

def start_cron_job():
    schedule.every().day.at("00:00").do(remove_old_logs)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    start_cron_job()