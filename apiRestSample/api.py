from flask import Flask, jsonify, request
from lorna import FarmModel

app = Flask(__name__)
model = None

@app.route('/configure', methods=['POST'])
def configure_model():
    global model
    parameters = request.json
    model = FarmModel(parameters)
    return jsonify({"message": "Model configured successfully"}), 200

@app.route('/update', methods=['POST'])
def update_model():
    global model
    if model is None:
        return jsonify({"error": "Model not configured"}), 400
    
    steps = request.json.get('steps', 1)
    for _ in range(steps):
        model.step()
    return jsonify({"message": f"{steps} steps executed"}), 200

@app.route('/plants', methods=['GET'])
def get_plants():
    global model
    if model is None:
        return jsonify({"error": "Model not configured"}), 400
    plants = model.get_plant_states()
    return jsonify(plants), 200

@app.route('/tractors', methods=['GET'])
def get_tractors():
    global model
    if model is None:
        return jsonify({"error": "Model not configured"}), 400
    tractors = model.get_tractor_states()
    return jsonify(tractors), 200

@app.route('/grid', methods=['GET'])
def get_grid():
    global model
    if model is None:
        return jsonify({"error": "Model not configured"}), 400
    grid = model.get_grid_state()
    return jsonify(grid), 200

if __name__ == '__main__':
    app.run(debug=True)