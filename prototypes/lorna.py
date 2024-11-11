import agentpy as ap
import numpy as np
import pygame
import sys
from collections import deque

# Initialize Pygame
pygame.init()
PLANT_GRID_SIZE = 4  # Size of the inner grid for plants
PATH_WIDTH = 1  # Width of the path around plants
GRID_SIZE = PLANT_GRID_SIZE + (PATH_WIDTH * 2)  # Total grid size including paths
WIDTH, HEIGHT = 400, 400  # Make window slightly larger
CELL_SIZE = WIDTH // GRID_SIZE
FPS = 2

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (169, 169, 169)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)
PATH_COLOR = (240, 240, 240)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Farm Simulation")
font = pygame.font.SysFont(None, 20)

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
            self.watered = False

class Tractor(ap.Agent):
    def setup(self):
        self.water_capacity = self.p['water_capacity']
        self.fuel_capacity = self.p['fuel_capacity']
        self.water_level = self.water_capacity
        self.fuel_level = self.fuel_capacity
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
        elif self.task == "harvesting" and plant.is_ready_for_harvest():
            plant.harvested = True
            return True
        return False

class FarmModel(ap.Model):
    def initialize(self, parameters):
        """Custom initialization method with paths"""
        # Create grid
        self.grid = ap.Grid(self, [GRID_SIZE, GRID_SIZE])
        
        # Initialize plants as a list first
        self.plants = []
        positions = []
        
        # Create plants only in inner grid
        for y in range(PATH_WIDTH, GRID_SIZE - PATH_WIDTH):
            for x in range(PATH_WIDTH, GRID_SIZE - PATH_WIDTH):
                plant = Plant(self)
                plant.setup()
                plant.position = (x, y)
                self.plants.append(plant)
                positions.append((x, y))
        
        # Convert plants to AgentList and add to grid
        self.plants = ap.AgentList(self, self.plants)
        self.grid.add_agents(self.plants, positions)
        
        # Initialize tractors only on paths
        self.tractors = []
        tractor_positions = []
        
        # Define possible path positions
        path_positions = []
        
        # Add top and bottom paths
        for x in range(GRID_SIZE):
            for y in range(PATH_WIDTH):  # Top path
                path_positions.append((x, y))
            for y in range(GRID_SIZE - PATH_WIDTH, GRID_SIZE):  # Bottom path
                path_positions.append((x, y))
                
        # Add left and right paths (excluding corners to avoid duplicates)
        for y in range(PATH_WIDTH, GRID_SIZE - PATH_WIDTH):
            for x in range(PATH_WIDTH):  # Left path
                path_positions.append((x, y))
            for x in range(GRID_SIZE - PATH_WIDTH, GRID_SIZE):  # Right path
                path_positions.append((x, y))
        
        # Create tractors only on paths
        for _ in range(parameters['num_tractors']):
            while True:
                pos = path_positions[np.random.randint(len(path_positions))]
                if pos not in tractor_positions:
                    tractor = Tractor(self)
                    tractor.setup()
                    tractor.position = pos
                    self.tractors.append(tractor)
                    tractor_positions.append(pos)
                    break
        
        # Convert tractors to AgentList and add to grid
        self.tractors = ap.AgentList(self, self.tractors)
        self.grid.add_agents(self.tractors, tractor_positions)
        
        print(f"Setup complete: {len(self.plants)} plants, {len(self.tractors)} tractors")
        return True

    def is_position_occupied(self, pos, ignore_tractor=None):
        for tractor in self.tractors:
            if tractor.position == pos and tractor != ignore_tractor:
                return True
        return False

    def find_path(self, start, end):
        # ... (código existente)

    def find_nearest_target(self, tractor):
        # ... (código existente)

    def step(self, steps=1):
        for _ in range(steps):
            # Update plants
            for plant in self.plants:
                plant.grow()

            # Update tractors
            for tractor in self.tractors:
                if tractor.fuel_level <= 0:
                    continue

                tractor.task = "watering" if tractor.water_level > 0 else "harvesting"

                if not tractor.current_path:
                    target = self.find_nearest_target(tractor)
                    if target:
                        path = self.find_path(tractor.position, target.position)
                        if path:
                            tractor.current_path = deque(path)

                if tractor.current_path:
                    next_pos = tractor.current_path.popleft()
                    if self.is_position_occupied(next_pos, ignore_tractor=tractor):
                        print(f"Tractor en {tractor.position} encuentra a otro tractor en {next_pos}. Intentando ruta alternativa.")
                        if tractor.current_path:
                            target = self.find_nearest_target(tractor)
                            if target:
                                new_path = self.find_path(tractor.position, target.position)
                                if new_path:
                                    tractor.current_path = deque(new_path)
                        continue

                    if tractor.move_to(next_pos):
                        target_plant = next((p for p in self.plants if p.position == next_pos), None)
                        if target_plant:
                            tractor.perform_task(target_plant)

    def get_plant_states(self):
        return [{"position": plant.position, "maturity": plant.maturity, "watered": plant.watered, "harvested": plant.harvested} for plant in self.plants]

    def get_tractor_states(self):
        return [{"position": tractor.position, "task": tractor.task, "water_level": tractor.water_level, "fuel_level": tractor.fuel_level} for tractor in self.tractors]

    def get_grid_state(self):
        grid_state = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        for plant in self.plants:
            x, y = plant.position
            grid_state[y][x] = plant.maturity
        return grid_state