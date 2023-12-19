from repository.db import Database
import logging


class EmotionalStateService:
    # MongoDB database connection
    db = Database("EmotionalStates")
    client = None

    # Function to insert the emotional state data in the database
    def insert_or_update(self, data, emotional_state):
        # We create or update the emotional state
        emotional_state_query = {"externalId": data["externalId"]}
        document, self.client = self.db.search(emotional_state_query, self.client)

        if document is not None:
            new_value = {"emotionalState": emotional_state}
            result, self.client = self.db.update(emotional_state_query, new_value, self.client)
            logging.debug(
                "Updates emotional state external id: " + data["externalId"] + " - emotional state: " + emotional_state)
        else:
            new_document = {"externalId": data["externalId"], "emotionalState": emotional_state}
            result, self.client = self.db.insert(new_document, self.client)
            logging.debug(
                "Inserts emotional state external id: " + data["externalId"] + " - emotional state: " + emotional_state)

        return result

    # Function to find the sensor data in base of the external id
    def find_by_external_id(self, external_id):
        # Creates the query to get the external id
        sensor_data_query = {"externalId": external_id}
        document, self.client = self.db.search(sensor_data_query, self.client)

        if document is None:
            document = {"externalId": external_id, "emotionalState": None}
        else:
            document["_id"] = str(document["_id"])

        logging.debug("Found emotional state by external id: " + external_id)
        return document
