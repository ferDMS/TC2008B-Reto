from flask import Flask, jsonify, request
from lorna import FarmModel

app = Flask(__name__)
model = None

@app.route('/initialize', methods=['POST'])
def initialize_model():
    global model
    parameters = request.json or {
        'num_tractors': 3,
        'water_capacity': 20,
        'fuel_capacity': 100,
        'steps': 200
    }
    model = FarmModel(parameters)
    success = model.initialize()
    return jsonify({"message": "Model initialized" if success else "Failed to initialize model"}), 200 if success else 500

@app.route('/step', methods=['POST'])
def step_model():
    global model
    if model is None:
        return jsonify({"error": "Model not initialized"}), 400
    model.step()
    return jsonify({"message": "Step executed"}), 200

@app.route('/state', methods=['GET'])
def get_state():
    global model
    if model is None:
        return jsonify({"error": "Model not initialized"}), 400
    state = model.get_state()
    return jsonify(state), 200

if __name__ == '__main__':
    app.run(debug=True)
