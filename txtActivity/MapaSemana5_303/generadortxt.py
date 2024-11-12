import numpy as np
import os
import heapq

def heuristic(a, b):
    return abs(b[0] - a[0]) + abs(b[1] - a[1])

def a_star_search(start, goal, grid):
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while frontier:
        current = heapq.heappop(frontier)[1]

        if current == goal:
            break

        for next in grid.neighbors(current):
            new_cost = cost_so_far[current] + 1  # Assuming all edges have the same cost
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                heapq.heappush(frontier, (priority, next))
                came_from[next] = current

    # Reconstruct path
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)  # optional
    path.reverse()  # optional
    return path

class Grid:
    def __init__(self, width, height, obstacles):
        self.width = width
        self.height = height
        self.obstacles = set(obstacles)  # Use a set for faster look-up

    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id):
        return id not in self.obstacles

    def neighbors(self, id):
        (x, y) = id
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return list(results)  # Convert filter object to list

def get_script_dir():
    """Returns the directory where the script is located."""
    return os.path.dirname(os.path.realpath(__file__))

def read_positions(file_path):
    """Reads two-line CSV files for positions. Ensures file exists."""
    if not os.path.exists(file_path):
        print(f"Error: {file_path} does not exist.")
        return []
    with open(file_path, 'r') as file:
        x_values = list(map(float, file.readline().strip().split(',')))
        y_values = list(map(float, file.readline().strip().split(',')))
    return list(zip(x_values, y_values))

def write_path(group, team, robot, path):
    """Writes the calculated path to a file in the script directory."""
    filename = f"XY_{group}_{team}_{robot}.txt"
    full_path = os.path.join(get_script_dir(), filename)
    with open(full_path, 'w') as f:
        for position in path:
            f.write(f"{position[0]},{position[1]}\n")

def calculate_path(initial_pos, target_positions, grid):
    path = [initial_pos]
    current_pos = initial_pos
    for target in target_positions:
        path_segment = a_star_search(current_pos, target, grid)
        path.extend(path_segment[1:])  # Exclude the start position to avoid duplicates
        current_pos = target
    return path

# Example usage
group = 1
team = 1
robots = [1, 2]  # Assuming two robots for simplicity
script_directory = get_script_dir()  # Get the directory of the script

initial_positions = read_positions(os.path.join(script_directory, "InitialPositions.txt"))
target_positions = read_positions(os.path.join(script_directory, "TargetPositions.txt"))

# Assuming obstacles are read and transformed correctly
obstacles = []
for obs_file in os.listdir(script_directory):
    if obs_file.startswith("Obstacle_"):
        obstacles.extend(read_positions(os.path.join(script_directory, obs_file)))

# Create grid
grid = Grid(10, 10, obstacles)  # Define grid size and pass obstacles

for robot, initial_pos in zip(robots, initial_positions):
    path = calculate_path(initial_pos, target_positions, grid)
    write_path(group, team, robot, path)
