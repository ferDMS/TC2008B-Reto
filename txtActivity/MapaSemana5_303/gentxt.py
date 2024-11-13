import numpy as np
from shapely.geometry import Polygon, LineString, Point
import networkx as nx
import matplotlib.pyplot as plt

# Define plane boundaries (origin at the center)
PLANE_WIDTH = 6  # meters
PLANE_HEIGHT = 4  # meters

# NSTEPS constraint
NSTEPS = 100

# Define the obstacles
obstacles = [
    Polygon([
        (-0.218391135768374, 0.225864543073497),
        (-0.746320221915368, -0.0789354569265029),
        (-0.441520221915368, -0.606864543073497),
        (0.0864088642316258, -0.302064543073497)
    ]),
    Polygon([
        (0.441520221915368, 0.606864543073497),
        (-0.0864088642316257, 0.302064543073497),
        (0.218391135768374, -0.225864543073497),
        (0.746320221915368, 0.0789354569265031)
    ]),
    Polygon([
        (-0.6952, 1.3048),
        (-1.3048, 1.3048),
        (-1.3048, 0.6952),
        (-0.6952, 0.6952)
    ]),
    Polygon([
        (1.3048, -0.6952),
        (0.6952, -0.6952),
        (0.6952, -1.3048),
        (1.3048, -1.3048)
    ]),
    Polygon([
        (0.873302236800156, 1.43552614690566),
        (0.28447385309434, 1.59330223680016),
        (0.126697763199844, 1.00447385309434),
        (0.71552614690566, 0.846697763199844)
    ]),
    Polygon([
        (-0.568947706188681, -1),
        (-1, -0.568947706188681),
        (-1.43105229381132, -1),
        (-1, -1.43105229381132)
    ]),
]

# Define the targets
targets = [
    (-0.86717069892473, -0.356552419354838),
    (-0.277318548387096, 0.550235215053764),
    (0.286122311827957, -0.497412634408602),
    (-1.01683467741935, 1.52745295698925),
    (0.673487903225808, 0.629469086021506),
    (-1.37778897849462, -1.36898521505376),
    (1.54506048387097, -0.999227150537633),
]

# Define GRID_RES
GRID_RES = 0.05  # meters

# Function to check if any targets are inside obstacles
def check_targets_in_obstacles(targets, obstacles):
    for idx, target in enumerate(targets):
        point = Point(target)
        for obs in obstacles:
            if obs.contains(point) or obs.touches(point):
                print(f"Target {idx} at {target} is inside or touching an obstacle.")
                break

# Function to plot the environment
def plot_environment(obstacles, targets):
    fig, ax = plt.subplots()
    # Plot obstacles
    for obs in obstacles:
        x, y = obs.exterior.xy
        ax.fill(x, y, color='gray', alpha=0.5, edgecolor='black')
    # Plot targets
    tx, ty = zip(*targets)
    ax.plot(tx, ty, 'ro', label='Targets')
    ax.set_aspect('equal')
    ax.set_xlim(-PLANE_WIDTH / 2 - 0.5, PLANE_WIDTH / 2 + 0.5)
    ax.set_ylim(-PLANE_HEIGHT / 2 - 0.5, PLANE_HEIGHT / 2 + 0.5)
    ax.legend()
    plt.title('Environment with Obstacles and Targets')
    plt.xlabel('X-axis (meters)')
    plt.ylabel('Y-axis (meters)')
    plt.grid(True)
    plt.show()

# Function to create the grid for A* algorithm
def create_grid(obstacles, grid_res):
    x_min = -PLANE_WIDTH / 2 - grid_res
    x_max = PLANE_WIDTH / 2 + grid_res
    y_min = -PLANE_HEIGHT / 2 - grid_res
    y_max = PLANE_HEIGHT / 2 + grid_res
    x_coords = np.arange(x_min, x_max + grid_res, grid_res)
    y_coords = np.arange(y_min, y_max + grid_res, grid_res)
    grid = {}
    for x in x_coords:
        for y in y_coords:
            point = Point(x, y)
            if any(obs.contains(point) or obs.touches(point) for obs in obstacles):
                grid[(x, y)] = 1  # Occupied
            else:
                grid[(x, y)] = 0  # Free
    return grid

# A* algorithm implementation
def astar(grid, start, goal):
    from heapq import heappush, heappop

    def heuristic(a, b):
        return np.linalg.norm(np.array(a) - np.array(b))

    open_set = []
    heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    while open_set:
        _, current = heappop(open_set)
        if current == goal:
            # Reconstruct path
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1]
        x, y = current
        # Define neighbors (including diagonals)
        neighbors = [
            (x + GRID_RES, y),
            (x - GRID_RES, y),
            (x, y + GRID_RES),
            (x, y - GRID_RES),
            (x + GRID_RES, y + GRID_RES),
            (x - GRID_RES, y - GRID_RES),
            (x + GRID_RES, y - GRID_RES),
            (x - GRID_RES, y + GRID_RES),
        ]
        for neighbor in neighbors:
            if neighbor not in grid or grid[neighbor] == 1:
                continue  # Skip occupied cells
            tentative_g_score = g_score[current] + heuristic(current, neighbor)
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heappush(open_set, (f_score[neighbor], neighbor))
    return None  # No path found

# Function to create the complete graph with A* paths
def create_complete_graph_with_astar(points, obstacles, grid):
    G = nx.Graph()
    num_points = len(points)
    for i in range(num_points):
        G.add_node(i, pos=points[i])
    for i in range(num_points):
        for j in range(num_points):
            if i == j:
                continue
            # Use A* to find a path
            start_cell = (round(points[i][0] / GRID_RES) * GRID_RES, round(points[i][1] / GRID_RES) * GRID_RES)
            goal_cell = (round(points[j][0] / GRID_RES) * GRID_RES, round(points[j][1] / GRID_RES) * GRID_RES)
            path = astar(grid, start_cell, goal_cell)
            if path is not None:
                # Compute the length of the path
                path_length = sum(np.linalg.norm(np.array(path[k+1]) - np.array(path[k])) for k in range(len(path)-1))
                G.add_edge(i, j, weight=path_length, path=path)
            else:
                print(f"No path found between target {i} and target {j}.")
    return G

# Solve TSP using NetworkX's approximate solver
def solve_tsp(G):
    from networkx.algorithms.approximation import traveling_salesman_problem
    path = traveling_salesman_problem(G, weight='weight')
    return path

# Extract full path from TSP path
def extract_full_path_from_tsp(tsp_path, G):
    full_path = []
    for i in range(len(tsp_path) - 1):
        u = tsp_path[i]
        v = tsp_path[i + 1]
        edge_data = G.get_edge_data(u, v)
        path = edge_data['path']
        if len(full_path) > 0:
            # Avoid duplicate points
            if full_path[-1] == path[0]:
                full_path.extend(path[1:])
            else:
                full_path.extend(path)
        else:
            full_path.extend(path)
    return full_path

# Discretize the full path to meet NSTEPS constraint
def discretize_full_path(full_path, NSTEPS):
    # Compute the total length of the path
    total_length = sum(np.linalg.norm(np.array(full_path[i + 1]) - np.array(full_path[i])) for i in range(len(full_path) - 1))
    # Determine the distance between steps
    step_distance = total_length / NSTEPS
    # Generate waypoints along the path
    waypoints = [full_path[0]]
    accumulated_distance = 0
    last_point = np.array(full_path[0])
    for i in range(1, len(full_path)):
        current_point = np.array(full_path[i])
        segment = current_point - last_point
        segment_length = np.linalg.norm(segment)
        while accumulated_distance + segment_length >= step_distance:
            remaining_distance = step_distance - accumulated_distance
            ratio = remaining_distance / segment_length
            waypoint = last_point + ratio * segment
            waypoints.append(tuple(waypoint))
            last_point = waypoint
            segment = current_point - last_point
            segment_length = np.linalg.norm(segment)
            accumulated_distance = 0
        accumulated_distance += segment_length
        last_point = current_point
    if waypoints[-1] != full_path[-1]:
        waypoints.append(full_path[-1])
    return waypoints

# Function to plot the full path
def plot_full_path(obstacles, points, full_path):
    fig, ax = plt.subplots()
    # Plot obstacles
    for obs in obstacles:
        x, y = obs.exterior.xy
        ax.fill(x, y, color='gray', alpha=0.5, edgecolor='black')
    # Plot points
    px, py = zip(*points)
    ax.plot(px, py, 'ro', label='Targets')
    # Plot full path
    fx, fy = zip(*full_path)
    ax.plot(fx, fy, 'b-', label='Full Path')
    ax.set_aspect('equal')
    ax.legend()
    plt.title('Robot Path')
    plt.xlabel('X-axis (meters)')
    plt.ylabel('Y-axis (meters)')
    plt.grid(True)
    plt.show()

# Main execution
if __name__ == "__main__":
    # Check targets against obstacles
    check_targets_in_obstacles(targets, obstacles)

    # Visualize the environment
    plot_environment(obstacles, targets)

    # Create the grid
    grid = create_grid(obstacles, GRID_RES)

    # Create the complete graph with A* paths
    all_points = targets
    G = create_complete_graph_with_astar(all_points, obstacles, grid)

    # Check if the graph is fully connected
    if not nx.is_connected(G):
        print("The complete graph is not fully connected.")
        # Handle disconnected components if necessary
    else:
        # Solve TSP
        tsp_path = solve_tsp(G)

        # Extract full path from TSP
        full_path = extract_full_path_from_tsp(tsp_path, G)

        # Discretize the path
        waypoints = discretize_full_path(full_path, NSTEPS)

        # Output the waypoints
        print("Robot path coordinates:")
        for coord in waypoints:
            print(coord)

        # Visualize the full path
        plot_full_path(obstacles, all_points, full_path)
