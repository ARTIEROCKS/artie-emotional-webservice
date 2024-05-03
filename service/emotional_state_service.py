from repository.db import Database
from collections import Counter
import logging
import numpy as np
from datetime import datetime


class EmotionalStateService:
    # MongoDB database connection
    db = Database("EmotionalStates")
    client = None

    # Dictionary from higher to lower importance of emotional states (emotional state, importance)
    emotional_states_importance = {
        0: 7,  # Neutral
        1: 0,  # Anger
        2: 4,  # Contempt
        3: 1,  # Disgust
        4: 3,  # Fear
        5: 2,  # Happy
        6: 5,  # Sadness
        7: 6  # Surprise
    }

    # Dictionary for mapping the id of the emotional state to the class
    emotional_states_mapping = {
        0: "NEUTRAL",
        1: "ANGER",
        2: "CONTEMPT",
        3: "DISGUST",
        4: "FEAR",
        5: "HAPPY",
        6: "SADNESS",
        7: "SURPRISE"
    }

    # Function to insert the emotional state data in the database and the predicted classes
    def insert_or_update(self, data, emotional_state, predictions):
        # We create or update the emotional state
        emotional_state_query = {"externalId": data["externalId"]}
        document, self.client = self.db.search(emotional_state_query, self.client)
        current_time = datetime.utcnow()

        # New predicted state to be added to the history
        history_entry = {
            "emotionalState": emotional_state,
            "predictions": predictions.tolist(),
            "timestamp": current_time
        }

        if document is not None:

            # Add the new state to the history. Preserving existing history if it exists
            emotional_state_history = document.get("emotionalStateHistory", [])
            emotional_state_history.append(history_entry)

            # Update the document with the new values
            new_value = {
                "emotionalState": emotional_state,  # Latest/emotional state
                "predictions": predictions.tolist(),  # Latest predictions
                "emotionalStateHistory": emotional_state_history,  # History of all states and predictions
                "lastUpdate": current_time  # Time of the last update
            }
            result, self.client = self.db.update(emotional_state_query, new_value, self.client)
            logging.debug(
                "Updates emotional state external id: " + data["externalId"] + " - emotional state: " + emotional_state)
        else:
            # Create a new document with the initial values, including the history array
            new_document = {
                "externalId": data["externalId"],
                "emotionalState": emotional_state,
                "predictions": predictions.tolist(),
                "emotionalStateHistory": [history_entry],  # Initialize history with the first entry
                "lastUpdate": current_time
            }

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

    # Define custom_sort function with counter as a default argument
    def custom_sort(self, number, counter):
        return -counter[number], self.emotional_states_importance[number]

    # Function to get the emotional state of a student from a list of emotional states
    def get_emotional_state_from_list(self, emotional_state_list):

        # Getting the column index with the maximum value for each row
        max_indexes = np.argmax(emotional_state_list, axis=1)

        # We count the emotional state repetitions in the list and order them from the most common to the less
        counter = Counter(max_indexes)
        sorted_emotional_states = sorted(set(max_indexes), key=lambda x: self.custom_sort(x, counter))

        # Find the most common emotional state
        most_common_emotional_state = sorted_emotional_states[0]

        return self.emotional_states_mapping[most_common_emotional_state]
