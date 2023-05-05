import pika
import os
import json
from datetime import datetime
from repository.db import Database

# Function to transform a txt json to an object
def load_json_data(txt_json_data):
    data = json.loads(txt_json_data)
    return data

# Function to consume the queue
def start_consuming():

    # Getting the connection data from the environment variables
    rabbitmq_host = os.getenv('APP_RABBITMQ_HOST', 'localhost')
    rabbitmq_port = os.getenv('APP_RABBITMQ_PORT', 5672)
    rabbitmq_user = os.getenv('APP_RABBITMQ_USER', 'guest')
    rabbitmq_password = os.getenv('APP_RABBITMQ_PASSWORD', 'guest')
    rabbitmq_vhost = os.getenv('APP_RABBITMQ_VHOST', '/')
    rabbitmq_queue = 'emotionalStateRequests'

    # RabbitMQ connection
    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
    parameters = pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, virtual_host=rabbitmq_vhost,
                                           credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # Creation of the queue if it doesn't exist
    channel.queue_declare(queue=rabbitmq_queue, durable=True)

    # MongoDB database connection
    db = Database()
    client = None

    # Subscription to the queue
    channel.basic_consume(queue=rabbitmq_queue, on_message_callback=lambda ch, method, properties, body: callback(ch, method, properties, body, channel, db, client))

    # Waiting for new messages
    print('Waiting for new messages...')
    channel.start_consuming()


# Function to process the message queue
def callback(ch, method, properties, body, channel, db, client):

    # TODO: Make the prediction here
    print("Doing the prediction....")
    prediction = "NONE"
    date_format = "%d/%m/%Y, %H:%M:%S %Z"

    # Inserts the data in the database with the prediction
    data = load_json_data(body)
    data['emotionalState'] = prediction
    data['date'] = datetime.strptime(data['date'], date_format)
    data['fromDate'] = datetime.strptime(data['fromDate'], date_format)
    data['toDate'] = datetime.strptime(data['toDate'], date_format)

    result, client = db.insert(data, client)

    # Remove the message from the queue
    channel.basic_ack(delivery_tag=method.delivery_tag)
