from flask import Flask, request, jsonify
from flask_cors import CORS
from service import queue_service
from service.sensor_data_service import SensorDataService

app = Flask(__name__)
CORS(app)


@app.route('/api/v1/emotional-model/predict', methods=['GET'])
def predict_emotional_model():

    external_id = request.args.get('externalId')
    sensor_data_service = SensorDataService()
    document = sensor_data_service.find_by_external_id(external_id)
    return jsonify(document)


if __name__ == "__main__":
    queue_service.start_consuming()
    app.run(debug=False, host="0.0.0.0", port="5000")
