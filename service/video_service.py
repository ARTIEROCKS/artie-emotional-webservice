from base64 import b64decode
import cv2
from tqdm import tqdm
import ffmpeg
import numpy as np
import tempfile
import os
from base64 import b64decode
import logging

def transform_video_to_images(data):
    logging.info("Getting frames from video file")
    frames = []
    if data != 'data:':
        try:
            first_comma = data.find(",")
            second_comma = data.find(",", first_comma + 1)

            if second_comma == -1:
                logging.error("Could not find second comma in the input data.")
                return frames

            encoded = data[second_comma + 1:]
            if not encoded:
                logging.error("Encoded video data is empty.")
                return frames

            try:
                video_data = b64decode(encoded)
            except Exception as decode_error:
                logging.error(f"Error decoding Base64 data: {decode_error}")
                return frames

            # Create a temporary file to store the video
            with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as temp_file:
                temp_file.write(video_data)
                temp_file_path = temp_file.name

            # Use FFmpeg to extract frames
            try:

                probe = ffmpeg.probe(temp_file_path)
                video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
                if not video_stream:
                    logging.error("No video stream found in the input file.")
                    return frames

                width = int(video_stream['width'])
                height = int(video_stream['height'])

                out, _ = (
                    ffmpeg
                    .input(temp_file_path)
                    .output('pipe:', format='rawvideo', pix_fmt='rgb24')
                    .run(capture_stdout=True)
                )

                frames = np.frombuffer(out, np.uint8).reshape([-1, height, width, 3])

            except ffmpeg.Error as e:
                logging.error(f"ffprobe error: {e.stderr.decode()}")
            except Exception as e:
                logging.error(f"Error processing video: {e}")
            finally:
                os.unlink(temp_file_path)

        except Exception as e:
            logging.error(f"Unexpected error during video processing: {e}")
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
