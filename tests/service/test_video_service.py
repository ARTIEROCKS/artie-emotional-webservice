import unittest
import cv2
import base64
import numpy as np
from service.video_service import normalize_images
from service.video_service import transform_video_to_images


class TestVideoService(unittest.TestCase):

    def test_normalize_images(self):
        # Load images from the test directory
        images = []
        for i in range(1, 12):
            image_path = f"tests/images/S005_001_000000{i:02d}.png"
            image = cv2.imread(image_path)
            images.append(image)

        # Normalize the images
        normalized_images = normalize_images(images)

        # Check if the shape of the normalized images is correct
        for normalized_image in normalized_images:
            self.assertEqual(normalized_image.shape, (48, 48))

        # Check if the data type of the normalized images is correct
        self.assertEqual(normalized_images.dtype, np.uint8)

    def test_transform_video_to_images(self):
        # Path to the test video
        video_path = "tests/videos/S1_disgust_1.mp4"

        # Read the video in bytes
        with open(video_path, "rb") as video_file:
            video_bytes = video_file.read()

        # Codec in base64
        video_base64 = base64.b64encode(video_bytes).decode("utf-8")
        data = "data:image/jpeg;base64," + video_base64

        # Call the function to transform video to images
        images = transform_video_to_images(data)

        # Check if images are extracted
        self.assertTrue(len(images) > 0)
        for image in images:
            self.assertIsNotNone(image)


if __name__ == '__main__':
    unittest.main()
