from flask import Flask, request, jsonify
from flask_cors import CORS
from service import queue_service

app = Flask(__name__)
CORS(app)

@app.route('/api/v1/emotional-model/predict', methods=['GET'])
def predict_emotional_model():
    external_id = request.args.get('externalId')
    # TODO: process external_id and predict emotional model
    response = {'message': 'Emotional model prediction for external ID {} is pending'.format(external_id)}
    return jsonify(response)

if __name__ == "__main__":
    queue_service.start_consuming()
    app.run(debug=False, host="0.0.0.0", port="5000")
