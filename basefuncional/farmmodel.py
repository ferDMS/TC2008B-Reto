from flask import Flask, jsonify, request
import agentpy as ap
import numpy as np
import pygame
import sys
from collections import deque
import json  # Import json module for handling JSON operations

app = Flask(__name__)

# Initialize pygame
#pygame.init()
PLANT_GRID_SIZE = 5  
PATH_WIDTH = 2
GRID_SIZE = PLANT_GRID_SIZE + (PATH_WIDTH * 2)
WIDTH, HEIGHT = 600, 600  
CELL_SIZE = WIDTH // GRID_SIZE
FPS = 2


parameters = {}


# agentes
class Plant(ap.Agent):
    def setup(self):
        self.maturity = 0
        self.watered = False
        self.harvested = False
        self.position = None

    def needs_water(self):
        return not self.watered and not self.harvested and self.maturity < 5

    def is_ready_for_harvest(self):
        return self.maturity >= 5 and not self.harvested

    def grow(self):
        if self.watered and not self.harvested and self.maturity < 5:
            self.maturity += 1

class Silo(ap.Agent):
    def setup(self):
        self.position = (GRID_SIZE - 1, 0)

class Tractor(ap.Agent):
    def setup(self):
        self.water_capacity = self.p['water_capacity']
        self.fuel_capacity = self.p['fuel_capacity']
        self.wheat_capacity = self.p['wheat_capacity']
        self.water_level = self.water_capacity
        self.fuel_level = self.fuel_capacity
        self.wheat_level = 0
        self.task = "idle"
        self.position = None
        self.current_path = deque()

    def move_to(self, target_pos):
        if self.fuel_level > 0:
            self.position = target_pos
            self.fuel_level = max(0, self.fuel_level - 1)
            return True
        return False

    def perform_task(self, plant):
        if self.task == "watering" and plant.needs_water() and self.water_level > 0:
            plant.watered = True
            self.water_level = max(0, self.water_level - 1)
            return True
        elif self.task == "harvesting" and plant.is_ready_for_harvest() and self.wheat_level < self.wheat_capacity:
            plant.harvested = True
            self.wheat_level += 1
            return True
        return False

    def deposit_wheat(self):
        self.wheat_level = 0

class FarmModel(ap.Model):
    def initialize(self):
        self.grid = ap.Grid(self, [GRID_SIZE, GRID_SIZE])
    
        self.plants = []
        positions = []
    
        for y in range(PATH_WIDTH, GRID_SIZE - PATH_WIDTH):
            for x in range(PATH_WIDTH, GRID_SIZE - PATH_WIDTH):
                plant = Plant(self)
                plant.setup()
                plant.position = (x, y)
                self.plants.append(plant)
                positions.append((x, y))
        
        # Convert plants to AgentList and add them to the grid
        self.plants = ap.AgentList(self, self.plants)
        self.grid.add_agents(self.plants, positions)
        
        # Initialize tractors
        self.tractors = []
        tractor_positions = []
        
        # Define possible paths
        path_positions = []
        
        # Logic to create tractors
        for x in range(GRID_SIZE):
            for y in range(PATH_WIDTH):
                path_positions.append((x, y))
            for y in range(GRID_SIZE - PATH_WIDTH, GRID_SIZE):  
                path_positions.append((x, y))
                
        for y in range(PATH_WIDTH, GRID_SIZE - PATH_WIDTH):
            for x in range(PATH_WIDTH):  
                path_positions.append((x, y))
            for x in range(GRID_SIZE - PATH_WIDTH, GRID_SIZE):
                path_positions.append((x, y))
        
        for i in range(self.p['num_tractors']):
            while True:
                pos = path_positions[np.random.randint(len(path_positions))]
                if pos not in tractor_positions:
                    tractor = Tractor(self)
                    tractor.setup()
                    tractor.position = pos
                    self.tractors.append(tractor)
                    tractor_positions.append(pos)
                    break
        
        self.tractors = ap.AgentList(self, self.tractors)
        self.grid.add_agents(self.tractors, tractor_positions)
        
        # Initialize silo
        self.silo = Silo(self)
        self.silo.setup()
        self.grid.add_agents([self.silo], [self.silo.position])
        
        print(f"Setup complete: {len(self.plants)} plants, {len(self.tractors)} tractors, 1 silo")
        return True

    def find_path(self, start, end):
        if start == end:
            return [start]
            
        def h(pos):
            return abs(pos[0] - end[0]) + abs(pos[1] - end[1])
        
        def get_neighbors(pos):
            x, y = pos
            neighbors = []
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
                    is_path = (new_x < PATH_WIDTH or 
                             new_x >= GRID_SIZE - PATH_WIDTH or 
                             new_y < PATH_WIDTH or 
                             new_y >= GRID_SIZE - PATH_WIDTH)
                    is_target = (new_x, new_y) == end
                    if not any(t.position == (new_x, new_y) 
                        for t in self.tractors if t.position != start):
                            neighbors.append((new_x, new_y))
            return neighbors
        
        frontier = [(h(start), start)]
        came_from = {start: None}
        cost_so_far = {start: 0}
        
        while frontier:
            _, current = frontier.pop(0)
            if current == end:
                break
                
            for next_pos in get_neighbors(current):
                new_cost = cost_so_far[current] + 1
                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    priority = new_cost + h(next_pos)
                    frontier.append((priority, next_pos))
                    frontier.sort()
                    came_from[next_pos] = current
        
        if end not in came_from:
            return None
        
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = came_from[current]
        return path[::-1]

    def find_nearest_target(self, tractor):
        if tractor.task == "watering":
            targets = [p for p in self.plants if p.needs_water()]
        elif tractor.task == "harvesting":
            targets = [p for p in self.plants if p.is_ready_for_harvest()]
        else:  # Heading to silo
            targets = [self.silo]
        
        if not targets:
            return None
            
        return min(targets, 
                  key=lambda p: abs(p.position[0] - tractor.position[0]) + 
                               abs(p.position[1] - tractor.position[1]))

    def step(self):
        for plant in self.plants:
            plant.grow()
        
        for tractor in self.tractors:
            if tractor.fuel_level <= 0:
                continue
            
            # Prioritize watering first, then harvesting, then depositing wheat
            if tractor.wheat_level >= tractor.wheat_capacity:
                tractor.task = "depositing"
            elif any(plant.needs_water() for plant in self.plants):
                tractor.task = "watering"
            elif any(plant.is_ready_for_harvest() for plant in self.plants):
                tractor.task = "harvesting"
            else:
                tractor.task = "idle"
            
            if not tractor.current_path:
                if tractor.task == "depositing":
                    target = self.silo
                else:
                    target = self.find_nearest_target(tractor)
                if target:
                    path = self.find_path(tractor.position, target.position)
                    if path:
                        tractor.current_path = deque(path)
            
            if tractor.current_path:
                next_pos = tractor.current_path.popleft()
                if next_pos not in [t.position for t in self.tractors if t != tractor]:
                    if tractor.move_to(next_pos):
                        if tractor.task == "depositing" and tractor.position == self.silo.position:
                            tractor.deposit_wheat()
                        else:
                            target_plant = next(
                                (p for p in self.plants if p.position == next_pos), None)
                            if target_plant:
                                tractor.perform_task(target_plant)



@app.route('/initialize', methods=['POST']) 
def initialize_values():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Invalid JSON data"}), 400
    
        print("Recieved data: ", data)
        required_keys = ['plant_grid_size', 'path_width', 'num_tractors', 'water_capacity', 'fuel_capacity', 'steps']
        missing_keys = [key for key in required_keys if key not in data]
        if missing_keys:
            return jsonify({"error": f"Missing required keys: {', '.join(missing_keys)}"}), 400
    
        global PLANT_GRID_SIZE, PATH_WIDTH
        PLANT_GRID_SIZE = data['plant_grid_size']
        PATH_WIDTH = data['path_width']

        global parameters
        parameters = {
            'num_tractors': data['num_tractors'],
        'water_capacity': data['water_capacity'],
        'fuel_capacity': data['fuel_capacity'],
        'wheat_capacity': PLANT_GRID_SIZE,
            'steps': data['steps']
        }

        GRID_SIZE = PLANT_GRID_SIZE + (PATH_WIDTH * 2)
        CELL_SIZE = WIDTH // GRID_SIZE

        result = initialize_simulation()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Hello, World!"})



def initialize_simulation():
    # Create and initialize the model
    model = FarmModel(parameters)
    if not model.initialize():
        print("Failed to initialize model")
        # pygame.quit()
        sys.exit(1)

    # Initialize a list to store tractor statuses over time
    tractor_status_over_time = []

    # Main simulation loop
    running = True
    step_count = 0
    # clock = pygame.time.Clock()

    while running and step_count < parameters['steps']:
        try:
            model.step()
            # Collect status of tractors
            current_step = {"step": step_count}
            for idx, tractor in enumerate(model.tractors):
                tractor_id = f"tractor_{idx}"
                current_step[tractor_id] = list(tractor.position)  # [x, y]
                current_step[f"{tractor_id}_task"] = tractor.task
                current_step[f"{tractor_id}_water_level"] = tractor.water_level
                current_step[f"{tractor_id}_fuel_level"] = tractor.fuel_level
                # If you want to include wheat_level, uncomment the next line
                # current_step[f"{tractor_id}_wheat_level"] = tractor.wheat_level
            tractor_status_over_time.append(current_step)
            
            step_count += 1
            # clock.tick(FPS)
        except Exception as e:
            print(f"Error during simulation: {e}")
            running = False

    #pygame.quit()

    # After the simulation loop, save the statuses to a JSON file
    try:
        with open('tractor_statuses.json', 'w') as f:
            json.dump(tractor_status_over_time, f, indent=4)
        print("Tractor statuses saved to tractor_statuses.json")
    except Exception as e:
        print(f"Failed to save tractor statuses: {e}")
    
    return tractor_status_over_time



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)