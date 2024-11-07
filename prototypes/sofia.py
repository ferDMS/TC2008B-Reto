import agentpy as ap
import numpy as np
import pygame
import sys
from collections import deque

#inicializaciones pygame
pygame.init()
PLANT_GRID_SIZE = 5  
PATH_WIDTH = 1  
GRID_SIZE = PLANT_GRID_SIZE + (PATH_WIDTH * 2) 
WIDTH, HEIGHT = 400, 400  
CELL_SIZE = WIDTH // GRID_SIZE
FPS = 2

# colores
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
        
        # convertir las plantas en AgentList y agregarlas a la grid
        self.plants = ap.AgentList(self, self.plants)
        self.grid.add_agents(self.plants, positions)
        
        # inicializar tractores
        self.tractors = []
        tractor_positions = []
        
        # definir posibles caminos
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
        for _ in range(self.p['num_tractors']):
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
                    # Check if position is either on a path or the target position
                    is_path = (new_x < PATH_WIDTH or 
                             new_x >= GRID_SIZE - PATH_WIDTH or 
                             new_y < PATH_WIDTH or 
                             new_y >= GRID_SIZE - PATH_WIDTH)
                    is_target = (new_x, new_y) == end
                    if is_path or is_target:
                        # Check if position is not occupied by another tractor
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
        else:
            targets = [p for p in self.plants if p.is_ready_for_harvest()]
        
        if not targets:
            return None
            
        return min(targets, 
                  key=lambda p: abs(p.position[0] - tractor.position[0]) + 
                               abs(p.position[1] - tractor.position[1]))

    def step(self):
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
                if tractor.move_to(next_pos):
                    target_plant = next(
                        (p for p in self.plants if p.position == next_pos), None)
                    if target_plant:
                        tractor.perform_task(target_plant)

def draw_grid(model):
    screen.fill(WHITE)
    
    # Draw grid lines
    for x in range(GRID_SIZE + 1):
        pygame.draw.line(screen, BLACK, (x * CELL_SIZE, 0), (x * CELL_SIZE, HEIGHT))
    for y in range(GRID_SIZE + 1):
        pygame.draw.line(screen, BLACK, (0, y * CELL_SIZE), (WIDTH, y * CELL_SIZE))
    
    # Draw path areas with light gray background
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if (x < PATH_WIDTH or x >= GRID_SIZE - PATH_WIDTH or 
                y < PATH_WIDTH or y >= GRID_SIZE - PATH_WIDTH):
                pygame.draw.rect(screen, PATH_COLOR,
                               (x * CELL_SIZE + 1, y * CELL_SIZE + 1,
                                CELL_SIZE - 2, CELL_SIZE - 2))
    
    # Draw plants
    for plant in model.plants:
        x, y = plant.position
        if plant.harvested:
            color = GRAY
        elif plant.watered:
            color = BLUE
        elif plant.maturity == 0:
            color = RED
        else:
            green_value = int(155 + (plant.maturity * 20))
            color = (0, green_value, 0)
        
        pygame.draw.rect(screen, color,
                       (x * CELL_SIZE + 1, y * CELL_SIZE + 1,
                        CELL_SIZE - 2, CELL_SIZE - 2))
        
        text = font.render(str(plant.maturity), True, BLACK)
        text_rect = text.get_rect(center=(x * CELL_SIZE + CELL_SIZE//2,
                                        y * CELL_SIZE + CELL_SIZE//2))
        screen.blit(text, text_rect)
    
    # Draw tractors
    for tractor in model.tractors:
        x, y = tractor.position
        color = ORANGE if tractor.task == "watering" else YELLOW
        
        tractor_size = int(CELL_SIZE * 0.6)
        margin = (CELL_SIZE - tractor_size) // 2
        
        pygame.draw.rect(screen, color,
                       (x * CELL_SIZE + margin,
                        y * CELL_SIZE + margin,
                        tractor_size, tractor_size))
        
        pygame.draw.rect(screen, BLACK,
                       (x * CELL_SIZE + margin,
                        y * CELL_SIZE + margin,
                        tractor_size, tractor_size), 2)
        
        water_text = font.render(f"W:{tractor.water_level}", True, BLACK)
        fuel_text = font.render(f"F:{tractor.fuel_level}", True, BLACK)
        
        water_rect = water_text.get_rect(centerx=x * CELL_SIZE + CELL_SIZE//2,
                                       bottom=y * CELL_SIZE - 2)
        fuel_rect = fuel_text.get_rect(centerx=x * CELL_SIZE + CELL_SIZE//2,
                                     bottom=water_rect.top - 2)
        
        screen.blit(water_text, water_rect)
        screen.blit(fuel_text, fuel_rect)
    
    pygame.display.flip()

# parametros de inicio
parameters = {
    'num_tractors': 4,
    'water_capacity': 20,
    'fuel_capacity': 100,
    'steps': 200,
}

# crear e inicializar el modelo
model = FarmModel(parameters)
if not model.initialize():
    print("Failed to initialize model")
    pygame.quit()
    sys.exit(1)

# main loop del juego
running = True
step_count = 0
clock = pygame.time.Clock()

while running and step_count < parameters['steps']:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    try:
        model.step()
        draw_grid(model)
        step_count += 1
        clock.tick(FPS)
    except Exception as e:
        print(f"Error during simulation: {e}")
        running = False

pygame.quit()