import pika
import os
import json
import logging
from datetime import datetime
from service.sensor_data_service import SensorDataService
from service.emotional_state_service import EmotionalStateService
from service.video_service import transform_video_to_images, normalize_images
import tensorflow as tf


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

    logging.info("Start consuming the queue: " + rabbitmq_queue)

    # RabbitMQ connection
    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
    logging.info("Logging with credentials")

    parameters = pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, virtual_host=rabbitmq_vhost,
                                           credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # Creation of the queue if it doesn't exist
    channel.queue_declare(queue=rabbitmq_queue, durable=True, auto_delete=False)

    # Sensor data service
    logging.info("Instantiate the sensor data service")
    sensor_data_service = SensorDataService()

    # Emotional state service
    logging.info("Instantiate the emotional state service")
    emotional_state_service = EmotionalStateService()

    # Loading keras model
    model = tf.keras.saving.load_model("model/fer.h5")

    # Subscription to the queue
    channel.basic_consume(queue=rabbitmq_queue,
                          on_message_callback=lambda ch, method, properties, body: callback(ch, method, properties,
                                                                                            body, sensor_data_service,
                                                                                            emotional_state_service,
                                                                                            model))

    # Waiting for new messages
    logging.info("Waiting for new messages...")
    print('Waiting for new messages...')
    channel.start_consuming()


# Function to process the message queue
def callback(ch, method, properties, body, sensor_data_service, emotional_state_service, model):

    date_format = "%d/%m/%Y, %H:%M:%S %Z"

    # Getting the video from json, transforming into frames and normalizing
    data = load_json_data(body)
    video = data['data'][1:-1]
    frames = transform_video_to_images(video)
    normalized_frames = normalize_images(frames)

    logging.info("Performing the prediction...")
    predictions = model.predict(normalized_frames)
    prediction_class = emotional_state_service.get_emotional_state_from_list(predictions)

    # Inserts the data in the database with the prediction
    emotional_state_service.insert_or_update(data, prediction_class, predictions)
    logging.info("Emotional State: " + prediction_class)

    if not data['date'] is None:
        data['date'] = datetime.strptime(data['date'], date_format)
    if not data['fromDate'] is None:
        data['fromDate'] = datetime.strptime(data['fromDate'], date_format)
    if not data['toDate'] is None:
        data['toDate'] = datetime.strptime(data['toDate'], date_format)

    sensor_data_service.insert(data)
    logging.info("Inserts the data in db: " + data)

    # Remove the message from the queue
    ch.basic_ack(delivery_tag=method.delivery_tag)
