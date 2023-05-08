from flask import Flask, request, jsonify
from flask_cors import CORS
from service import queue_service
from service.emotional_state_service import EmotionalStateService
from threading import Thread

app = Flask(__name__)
CORS(app)

def run_flask_app():
    app.run(debug=False, host="0.0.0.0", port="5000")

@app.route('/api/v1/emotional-model/predict', methods=['GET'])
def predict_emotional_model():

    external_id = request.args.get('externalId')
    emotional_state_service = EmotionalStateService()
    document = emotional_state_service.find_by_external_id(external_id)

    return jsonify(document)


if __name__ == "__main__":
    t = Thread(target=queue_service.start_consuming)
    t.start()
    run_flask_app()
