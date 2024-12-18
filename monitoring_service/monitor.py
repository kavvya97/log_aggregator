import pika
import time
import constants
import json
from collections import deque

error_log_window = deque()

def connect_to_rabbitmq():
    connection = pika.BlockingConnection(pika.URLParameters(constants.RABBITMQ_URI))
    channel = connection.channel()

    # declare queues and exchanges
    channel.exchange_declare(exchange=constants.EXCHANGE_NAME, exchange_type="topic")
    channel.queue_declare(queue=constants.QUEUE_NAME, durable=True)

    # bind Queues to exchange
    channel.queue_bind(constants.QUEUE_NAME, 
                       exchange=constants.EXCHANGE_NAME, 
                       routing_key="*.error")
    channel.queue_bind(constants.QUEUE_NAME, 
                       exchange=constants.EXCHANGE_NAME, 
                       routing_key="*.warn")
    return channel

def process_log_message(ch, method, properties, body):
    log_data = json.loads(body.decode())
    timestamp = log_data.get("timestamp")
    service_name = log_data.get("service_name")
    severity = log_data.get("severity")
    message = log_data.get("log")

    print(f"[{timestamp}] [{service_name}] [{severity.upper()}] {message}")

    if severity == "error":
        add_to_error_window(timestamp, service_name, message)
        check_error_threshold()

def add_to_error_window(timestamp, service_name, message):
    current_time = time.time()
    error_log_window.append((current_time, service_name, message))
    while error_log_window and error_log_window[0][0] < current_time - constants.TIME_WINDOW:
        error_log_window.popleft()

def check_error_threshold():
    if len(error_log_window) >= constants.ERROR_THRESHOLD:
        print(f"\n[ALERT] High error rate detected! {len(error_log_window)} errors in the last {constants.TIME_WINDOW} seconds.\n")

    
def start_monitoring():
    channel = connect_to_rabbitmq()
    channel.basic_consume(queue=constants.QUEUE_NAME, on_message_callback=process_log_message, auto_ack=True)
    channel.start_consuming()


if __name__ == "__main__":
    start_monitoring()