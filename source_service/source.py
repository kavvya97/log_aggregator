import pika
import time
import random
import datetime
import json
from constants import SERVICES_LIST, SEVERITY

# rabbitmq uri
RABBITMQ_URI = "amqp://guest:guest@localhost:5672/"

def get_rabbitmq_channel():
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URI))
    channel = connection.channel()
    return channel, connection

def generate_log():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    service_name = random.choice(SERVICES_LIST)
    severity = random.choice(SEVERITY)
    message = f"{timestamp} {service_name} {severity} Log message generated"
    routing_key = f"{service_name}.{severity}"
    return routing_key, message

def send_logs():
    channel, connection = get_rabbitmq_channel()
    channel.exchange_declare('logs_exchange', exchange_type="topic")

    try:
        # send the logs
        while True:
            routing_key, message = generate_log()

            # published log messsages to a exchange
            channel.basic_publish(exchange="logs_exchange",
                                  routing_key=routing_key,
                                  body=message)
            
            print(f" [x] Sent '{message}' to '{routing_key}'")
            time.sleep(random.randint(1, 5))

    except KeyboardInterrupt:
        print("Stopping LogSource Service...")
    finally:
        connection.close()

if __name__ == "__main__":
    send_logs()

