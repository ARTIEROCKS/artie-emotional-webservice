from base64 import b64decode
import cv2
import logging
from tqdm import tqdm
import numpy as np


# Function to transform a video into frames
def transform_video_to_images(data):

    logging.info("Getting frames from video file")
    images = []
    if data != 'data:':
        try:
            header, encoded = data.split(",", 1)
            video = b64decode(encoded)

            # Convert the video to frames
            cap = cv2.VideoCapture(video)
            while True:
                ret, frame = cap.read()

                if not ret:
                    break

                images.append(frame)

            cap.release()

        except Exception as e:
            logging.error(f"Error during video processing: {str(e)}")

    return images


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
