import numpy as np
import os
import heapq

def heuristic(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))

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
            new_cost = cost_so_far[current] + heuristic(current, next)
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
    path.append(start)
    path.reverse()
    return path

class Grid:
    def __init__(self, width, height, obstacles, clearance=0.2):
        self.width = width
        self.height = height
        self.obstacles = self.expand_obstacles(obstacles, clearance)

    def expand_obstacles(self, obstacles, clearance):
        expanded_obstacles = set()
        for (ox, oy) in obstacles:
            for dx in np.arange(-clearance, clearance + 0.05, 0.05):
                for dy in np.arange(-clearance, clearance + 0.05, 0.05):
                    expanded_obstacles.add((ox + dx, oy + dy))
        return expanded_obstacles

    def in_bounds(self, id):
        (x, y) = id
        return -3 <= x <= 3 and -2 <= y <= 2  # Adjusted bounds to fit 6m width and 4m height centered at (0,0)

    def passable(self, id):
        return id not in self.obstacles

    def neighbors(self, id):
        (x, y) = id
        step_size = 0.2  # Smaller step size for finer control
        results = [(x + step_size, y), (x, y - step_size), (x - step_size, y), (x, y + step_size)]
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

def write_path(robot, path):
    """Writes the calculated path to a file in the script directory."""
    filename = f"Robot_{robot}_Path.txt"
    full_path = os.path.join(get_script_dir(), filename)
    with open(full_path, 'w') as f:
        for position in path:
            f.write(f"{position[0]},{position[1]}\n")

def calculate_path(initial_pos, target_positions, grid, other_robot_paths):
    path = [initial_pos]
    current_pos = initial_pos
    for target in target_positions:
        path_segment = a_star_search(current_pos, target, grid)
        path.extend(path_segment[1:])  # Exclude the start position to avoid duplicates
        current_pos = target

    # Limit the number of points and smooth the trajectory
    path = simplify_path(path, max_points=100)
    smoothed_path = smooth_path(path)

    return smoothed_path

def simplify_path(path, max_points=100):
    """Reduces the number of points in the path to a maximum of max_points."""
    if len(path) <= max_points:
        return path
    indices = np.round(np.linspace(0, len(path) - 1, max_points)).astype(int)
    return [path[i] for i in indices]

def smooth_path(path, window_size=5):
    """Smooths the path using a moving average."""
    if len(path) < 3:
        return path
    x, y = zip(*path)
    x_smooth = moving_average(x, window_size)
    y_smooth = moving_average(y, window_size)
    return list(zip(x_smooth, y_smooth))

def moving_average(data, window_size):
    """Calculates the moving average for smoothing."""
    if len(data) < window_size:
        window_size = len(data)
    return np.convolve(data, np.ones(window_size) / window_size, mode='valid').tolist()

def calculate_centered_target_path(initial_pos, target_positions, grid):
    path = [initial_pos]
    current_pos = initial_pos
    for target in target_positions:
        # Prioritize moving towards the center of target positions
        target_center = (target[0], target[1])
        path_segment = a_star_search(current_pos, target_center, grid)
        path.extend(path_segment[1:])  # Exclude the start position to avoid duplicates
        current_pos = target_center

    # Limit the number of points and smooth the trajectory
    path = simplify_path(path, max_points=100)
    smoothed_path = smooth_path(path)

    return smoothed_path

# Example usage
script_directory = get_script_dir()  # Get the directory of the script
initial_positions = read_positions(os.path.join(script_directory, "InitialPositions.txt"))
target_positions = read_positions(os.path.join(script_directory, "TargetPositions.txt"))

# Assuming obstacles are read and transformed correctly
obstacles = []
for obs_file in os.listdir(script_directory):
    if obs_file.startswith("Obstacle_"):
        obstacles.extend(read_positions(os.path.join(script_directory, obs_file)))

# Create grid
grid = Grid(6, 4, obstacles, clearance=0.2)  # Define grid size (6m x 4m) and pass obstacles

robot_paths = []
for robot_id, initial_pos in enumerate(initial_positions, start=1):
    path = calculate_centered_target_path(initial_pos, target_positions, grid)
    write_path(robot_id, path)
    robot_paths.append(path)  # Add calculated path to ensure other robots can avoid it
