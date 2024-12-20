# Function to insert data into the sensor data collection
from repository.db import Database
import logging


class SensorDataService:
    # MongoDB database connection
    db = Database("SensorData")
    client = None

    # Function to insert the sensor data in the database
    def insert(self, data):
        # Inserts the data in the database
        result, self.client = self.db.insert(data, self.client)
        return result

    # Function to find the sensor data in base of the external id
    def find_by_external_id(self, external_id):
        # Creates the query to get the external id
        logging.debug("Find by external id sensor data: " + external_id)
        sensor_data_query = {"externalId": external_id}
        document, self.client = self.db.search(sensor_data_query, self.client)
        return document
