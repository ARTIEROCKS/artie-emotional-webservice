FROM python:3.9.7-slim-buster

# Install necessary libraries for OpenGL
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

ADD model model
ADD service service
ADD repository repository
ADD config config
COPY app.py app.py

EXPOSE 5000

CMD [ "python3", "app.py", "--host=0.0.0.0", "--port=5000"]