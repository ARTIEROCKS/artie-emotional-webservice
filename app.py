from flask import Flask, request, jsonify
from flask_cors import CORS
from service import queue_service
from service.emotional_state_service import EmotionalStateService

app = Flask(__name__)
CORS(app)


@app.route('/api/v1/emotional-model/predict', methods=['GET'])
def predict_emotional_model():

    external_id = request.args.get('externalId')
    emotional_state_service = EmotionalStateService()
    document = emotional_state_service.find_by_external_id(external_id)

    if document is None:
        document = {"externalId": external_id, "emotionalState": None}

    return jsonify(document)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port="5000")
    queue_service.start_consuming()
