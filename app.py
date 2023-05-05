from flask import Flask
from flask_cors import CORS
from service import queue_service

app = Flask(__name__)
CORS(app)

if __name__ == "__main__":
    queue_service.start_consuming()
    app.run(debug=False, host="0.0.0.0", port="5000")
