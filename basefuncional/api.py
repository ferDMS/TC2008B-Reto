from flask import Flask, jsonify, request
from basemodel import FarmModel  # Cambia esta línea al archivo correcto

app = Flask(__name__)
model = None

@app.route('/initialize', methods=['POST'])
def initialize_model():
    global model
    parameters = {
        'num_tractors': request.form.get('num_tractors', type=int),
        'water_capacity': request.form.get('water_capacity', type=int),
        'fuel_capacity': request.form.get('fuel_capacity', type=int)
    }
    model = FarmModel(parameters)
    return jsonify({"message": "Model initialized successfully"}), 200

@app.route('/step', methods=['POST'])
def step_model():
    global model
    if model is None:
        return jsonify({"error": "Model not initialized"}), 400
    
    steps = request.form.get('steps', 1, type=int)
    model.step(steps)
    return jsonify({"message": f"{steps} steps executed"}), 200

@app.route('/state', methods=['GET'])
def get_model_state():
    global model
    if model is None:
        return jsonify({"error": "Model not initialized"}), 400
    
    state = {
        "plants": model.get_plant_states(),
        "tractors": model.get_tractor_states(),
        "grid": model.get_grid_state()
    }
    return jsonify(state), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)