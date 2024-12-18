import pika
import time
import random
import datetime
import os
from pymongo import MongoClient
import constants
import json

MONGO_URI = os.getenv("MONGO_URI", constants.MONGO_URL)
client = MongoClient(MONGO_URI)
db = client[constants.DB_NAME]
logs_collection = db[constants.COLLECTION_NAME] 
    
def store_raw_logs(ch, method, properties, body):
    try:
        log_message = json.loads(body.decode())
        logs_collection.insertOne(log_message)
        print("Log stored successfully in MongoDB.")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Failed to process log: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

def collect_logs():
    connection = pika.BlockingConnection(pika.URLParameters(constants.RABBITMQ_URI))
    channel = connection.channel()

    # Declare exchange and queues
    channel.exchange_declare(exchange=constants.EXCHANGE_NAME, exchange_type="topic")
    channel.queue_declare(constants.QUEUE_NAME, durable=True)

    # bind Queue to exchange and receive all the logs
    # # substitutes zero or more words
    channel.queue_bind(queue=constants.QUEUE_NAME, 
                       exchange=constants.EXCHANGE_NAME, 
                       routing_key='#')
    
    channel.basic_consume(queue=constants.QUEUE_NAME, on_message_callback=store_raw_logs)
    channel.start_consuming()


if __name__ == "__main__":
    collect_logs()
