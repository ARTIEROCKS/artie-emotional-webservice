FROM python:3.9.7-slim-buster

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