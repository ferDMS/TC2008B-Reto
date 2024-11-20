import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
import math

def parse_initial_positions(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        x_positions = list(map(float, lines[0].strip().split(',')))
        y_positions = list(map(float, lines[1].strip().split(',')))
    return (x_positions[0], y_positions[0]), (x_positions[1], y_positions[1])

def parse_target_positions(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        x_positions = list(map(float, lines[0].strip().split(',')))
        y_positions = list(map(float, lines[1].strip().split(',')))
    return list(zip(x_positions, y_positions))

def parse_obstacles(directory_path):
    obstacles = []
    for file_name in os.listdir(directory_path):
        if file_name.startswith('Obstacle_') and file_name.endswith('.txt'):
            with open(os.path.join(directory_path, file_name), 'r') as file:
                lines = file.readlines()
                x_positions = list(map(float, lines[0].strip().split(',')))
                y_positions = list(map(float, lines[1].strip().split(',')))
                obstacles.append(list(zip(x_positions, y_positions)))
    return obstacles

def visualize_space(initial_positions, target_positions, obstacles, path=None):
    fig, ax = plt.subplots()
    ax.set_xlim(-3.25, 3.25)
    ax.set_ylim(-3.25, 3.25)
    ax.set_aspect('equal')
    
    # Draw grid points
    for x in range(-7, 8):
        for y in range(-7, 8):
            ax.plot(x * 0.5, y * 0.5, 'ko', markersize=2)
    
    # Draw initial positions
    for pos in initial_positions:
        circle = patches.Circle(pos, 0.1, edgecolor='black', facecolor='none')
        ax.add_patch(circle)
    
    # Draw target positions
    for pos in target_positions:
        circle = patches.Circle(pos, 0.1, edgecolor='none', facecolor='blue')
        ax.add_patch(circle)
    
    # Draw obstacles
    for obstacle in obstacles:
        polygon = patches.Polygon(obstacle, edgecolor='none', facecolor='red')
        ax.add_patch(polygon)
    
    # Draw robots
    for pos in initial_positions:
        rect = patches.Rectangle((pos[0] - 0.09, pos[1] - 0.1), 0.18, 0.20, edgecolor='none', facecolor='lightgrey')
        ax.add_patch(rect)
    
    # Draw path
    if path:
        path_x, path_y = zip(*path)
        ax.plot(path_x, path_y, 'g-')
    
    plt.gca().set_facecolor('white')
    plt.show()

def is_in_obstacle(point, obstacles):
    for obstacle in obstacles:
        polygon = patches.Polygon(obstacle)
        if polygon.contains_point(point):
            return True
    return False

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def nearest_vertex(tree, point):
    nearest = tree[0]
    min_dist = distance(nearest, point)
    for vertex in tree:
        dist = distance(vertex, point)
        if dist < min_dist:
            nearest = vertex
            min_dist = dist
    return nearest

def rrt_star(initial_position, target_positions, obstacles, max_iterations=2000, step_size=0.05, radius=0.3, goal_bias=0.1):
    tree = [initial_position]
    parent = {initial_position: None}
    cost = {initial_position: 0}
    
    for _ in range(max_iterations):
        if random.random() < goal_bias:
            random_point = random.choice(target_positions)
        else:
            random_point = (random.uniform(-3.25, 3.25), random.uniform(-3.25, 3.25))
        
        if is_in_obstacle(random_point, obstacles):
            continue
        nearest = nearest_vertex(tree, random_point)
        direction = ((random_point[0] - nearest[0]) / distance(nearest, random_point),
                     (random_point[1] - nearest[1]) / distance(nearest, random_point))
        new_point = (nearest[0] + direction[0] * step_size, nearest[1] + direction[1] * step_size)
        if is_in_obstacle(new_point, obstacles):
            continue
        
        # Find neighbors within radius
        neighbors = [vertex for vertex in tree if distance(vertex, new_point) < radius]
        
        # Choose the best parent for the new point
        best_parent = nearest
        min_cost = cost[nearest] + distance(nearest, new_point)
        for neighbor in neighbors:
            new_cost = cost[neighbor] + distance(neighbor, new_point)
            if new_cost < min_cost:
                best_parent = neighbor
                min_cost = new_cost
        
        tree.append(new_point)
        parent[new_point] = best_parent
        cost[new_point] = min_cost
        
        # Rewire the tree
        for neighbor in neighbors:
            if neighbor == best_parent:
                continue
            new_cost = cost[new_point] + distance(new_point, neighbor)
            if new_cost < cost[neighbor]:
                parent[neighbor] = new_point
                cost[neighbor] = new_cost
        
        for target in target_positions:
            if distance(new_point, target) < 0.1:
                tree.append(target)
                parent[target] = new_point
                return tree, parent, target
    
    return tree, parent, None

def extract_path(tree, parent, target):
    if target not in parent:
        return []
    path = [target]
    while parent[target] is not None:
        target = parent[target]
        path.append(target)
    path.reverse()
    return path

# Example usage
initial_positions = parse_initial_positions('input/InitialPositions.txt')
target_positions = parse_target_positions('input/TargetPositions.txt')
obstacles = parse_obstacles('input')

paths = []
for initial_position in initial_positions:
    tree, parent, target = rrt_star(initial_position, target_positions, obstacles)
    if target:
        path = extract_path(tree, parent, target)
        paths.append(path)
    else:
        print(f"No path found for robot starting at {initial_position}.")

# Visualize the space with paths for each robot
fig, ax = plt.subplots()
ax.set_xlim(-3.25, 3.25)
ax.set_ylim(-3.25, 3.25)
ax.set_aspect('equal')

# Draw grid points
for x in range(-7, 8):
    for y in range(-7, 8):
        ax.plot(x * 0.5, y * 0.5, 'ko', markersize=2)

# Draw initial positions
for pos in initial_positions:
    circle = patches.Circle(pos, 0.1, edgecolor='black', facecolor='none')
    ax.add_patch(circle)

# Draw target positions
for pos in target_positions:
    circle = patches.Circle(pos, 0.1, edgecolor='none', facecolor='blue')
    ax.add_patch(circle)

# Draw obstacles
for obstacle in obstacles:
    polygon = patches.Polygon(obstacle, edgecolor='none', facecolor='red')
    ax.add_patch(polygon)

# Draw robots
for pos in initial_positions:
    rect = patches.Rectangle((pos[0] - 0.09, pos[1] - 0.1), 0.18, 0.20, edgecolor='none', facecolor='lightgrey')
    ax.add_patch(rect)

# Draw paths
for i, path in enumerate(paths):
    path_x, path_y = zip(*path)
    color = 'lightblue' if i == 0 else 'lightgreen'
    ax.plot(path_x, path_y, color=color)

plt.gca().set_facecolor('white')
plt.show()

# Print in pretty format
# print('Initial positions:', initial_positions)
# print('Target positions:', target_positions)
# print('Obstacles:')
# for i, obstacle in enumerate(obstacles):
#     print(f'Obstacle {i + 1}:', obstacle)