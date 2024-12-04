import unittest
from service.emotional_state_service import EmotionalStateService
from service.video_service import transform_video_to_images, normalize_images
import base64
import json
from keras.models import load_model


class TestEmotionalStateService(unittest.TestCase):

    def setUp(self):
        # Initialize any objects or variables needed for testing
        self.service = EmotionalStateService()

    def test_get_emotional_state_from_list_json(self):
        # Path to the JSON file
        json_path = "tests/json/artie.EmotionalStates_1.json"
        # Expected output
        expected_output = "SURPRISE"  # Change this based on the expected service output

        # Load the JSON
        with open(json_path, "r") as file:
            data = json.load(file)

        # Extract predictions
        predictions = [item["predictions"] for item in data]

        # Flatten the predictions list if needed
        flattened_predictions = [pred for sublist in predictions for pred in sublist]

        # Call the service method
        prediction_class = self.service.get_emotional_state_from_list(flattened_predictions)

        # Verify the result
        self.assertEqual(prediction_class, expected_output)

    def test_get_emotional_state_from_list(self):
        # Path to the test video
        video_path = "tests/videos/S1_disgust_1.mp4"
        expected_output = "FEAR"  # Expected output based on the provided mapping

        # Read the video in bytes
        with open(video_path, "rb") as video_file:
            video_bytes = video_file.read()

        # Codec in base64
        video_base64 = base64.b64encode(video_bytes).decode("utf-8")
        data = "data:image/jpeg;base64," + video_base64

        # Call the function to transform video to images
        frames = transform_video_to_images(data)
        normalized_frames = normalize_images(frames)

        # Loading keras model
        model = load_model("model/fer.h5")
        predictions = model.predict(normalized_frames)

        # Call the method under test
        prediction_class = self.service.get_emotional_state_from_list(predictions)

        # Check if the result matches the expected output
        self.assertEqual(expected_output, prediction_class, "Incorrect emotional state returned")

    def test_insert_or_update(self):
        # Path to the test video
        video_path = "tests/videos/S1_disgust_1.mp4"

        # Read the video in bytes
        with open(video_path, "rb") as video_file:
            video_bytes = video_file.read()

        # Codec in base64
        video_base64 = base64.b64encode(video_bytes).decode("utf-8")
        data = "data:image/jpeg;base64," + video_base64

        # Call the function to transform video to images
        frames = transform_video_to_images(data)
        normalized_frames = normalize_images(frames)

        # Loading keras model
        model = load_model("model/fer.h5")
        predictions = model.predict(normalized_frames)

        # Call the method under test
        prediction_class = self.service.get_emotional_state_from_list(predictions)

        # Check if the result matches the expected output
        json_data = {"externalId": "001", "data": data}
        result = self.service.insert_or_update(json_data, prediction_class, predictions)

        self.assertNotEqual(result, None)


if __name__ == '__main__':
    unittest.main()
