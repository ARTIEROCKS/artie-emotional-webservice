from repository.db import Database


class EmotionalStateService:
    # MongoDB database connection
    db = Database("EmotionalStates")
    client = None

    # Function to insert the emotional state data in the database
    def insert_or_update(self, data, emotional_state):
        # We create or update the emotional state
        emotional_state_query = {"externalId": data["externalId"]}
        document, self.client = self.db.search(emotional_state_query, self.client)

        if document is None:
            new_value = {"emotionalState": emotional_state}
            result, self.client = self.db.update(emotional_state_query, new_value, self.client)
        else:
            new_document = {"externalId": data["externalId"], "emotionalState": emotional_state}
            result, self.client = self.db.insert(new_document, self.client)

        return result, self.client

    # Function to find the sensor data in base of the external id
    def find_by_external_id(self, external_id):
        # Creates the query to get the external id
        sensor_data_query = {"externalId": external_id}
        document, self.client = self.db.search(sensor_data_query, self.client)
        return document, self.client
