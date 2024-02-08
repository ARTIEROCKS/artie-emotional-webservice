from base64 import b64decode
import cv2
import tempfile
import logging
from tqdm import tqdm
import numpy as np
import os


# Function to transform a video into frames
def transform_video_to_images(data):

    logging.info("Getting frames from video file")
    frames = []
    if data != 'data:':
        try:
            header, encoded = data.split(",", 1)
            video_data = b64decode(encoded)

            # Create a temporary file to store the video
            with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
                temp_file.write(video_data)
                temp_file_path = temp_file.name

            # Convert the video to frames
            cap = cv2.VideoCapture(temp_file_path)

            # Checks if the video has been correctly opened
            if not cap.isOpened():
                logging.error(f"Error opening the file video")
            else:
                # Transforms the video into a frame sequence
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    frames.append(frame)

                # Release the video capturer
                cap.release()

                # Deletes the temporary file
                temp_file.close()
                os.unlink(temp_file_path)

        except Exception as e:
            logging.error(f"Error during video processing: {str(e)}")

    return frames


# Function to normalize images to 48x48 gray scale
def normalize_images(images):

    logging.info("Normalizing images 48x48 grayscale")
    images_normalized = []

    # load the image, convert it to grayscale, and describe it
    for image in tqdm(images, desc="Normalizing", unit=" image"):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (48, 48))
        images_normalized.append(resized)

    return np.array(images_normalized)
