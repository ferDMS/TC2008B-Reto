"""
Robot Path Generator

TC2008B
Grupo: 303
Equipo: 1
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
import math

# Dimensions of robot (m)
ROBOT_WIDTH = 0.18
ROBOT_HEIGHT = 0.20
# Dimensions of space (m)
SPACE_WIDTH = 6.5
SPACE_HEIGHT = 6.5


def parse_initial_positions(file_path):
    """
    Parses the initial positions of the robots from a file.

    Args:
        file_path (str): The path to the file containing the initial positions.

    Returns:
        tuple: A tuple containing tuples, each representing the (x, y) coordinates of the initial positions.
            For example: ((x1, y1), (x2, y2), ...)
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()
        # Strip whitespaces, split by commas, cast as floats and turn iterator to list
        x_positions = list(map(float, lines[0].strip().split(',')))
        y_positions = list(map(float, lines[1].strip().split(',')))
    return tuple(zip(x_positions, y_positions))


def parse_target_positions(file_path):
    """
    Parses the target positions of the robots from a file.
    
    Args:
        file_path (str): The path to the file containing the target positions.
    
    Returns:
        list: A list of tuples, each representing the (x, y) coordinates of the target positions.
            For example: [(x1, y1), (x2, y2), ...]
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()
        x_positions = list(map(float, lines[0].strip().split(',')))
        y_positions = list(map(float, lines[1].strip().split(',')))
    return list(zip(x_positions, y_positions))


def parse_obstacles(directory_path):
    """
    Parses the obstacle coordinates definitions from multiple files.
    
    Args:
        directory_path (str): The path to the directory containing zero or more files containing the vertices of the obstacle. Each file follows the naming convention: Obstacle_<number>.txt.
        
    Returns:
        list: A list of lists, each representing an obstacle. Each obstacle is a list of tuples, where each tuple contains the (x, y) coordinates of a vertex.
               For example: [[(x1, y1), (x2, y2), (x3, y3), (x4, y4)], ...]
    """
    obstacles = []
    for file_name in os.listdir(directory_path):
        if file_name.startswith('Obstacle_') and file_name.endswith('.txt'):
            with open(os.path.join(directory_path, file_name), 'r') as file:
                lines = file.readlines()
                x_positions = list(map(float, lines[0].strip().split(',')))
                y_positions = list(map(float, lines[1].strip().split(',')))
                obstacles.append(list(zip(x_positions, y_positions)))
    return obstacles


def is_in_obstacle(point, obstacles):
    """
    Used in the rrt_star function, this function checks if a point is inside any of the obstacles.
    
    Args:
        point (tuple): The (x, y) coordinates of the point.
        obstacles (list): A list of obstacles, where each obstacle is a list of tuples, each representing the (x, y) coordinates of a vertex.
        
    Returns:
        bool: True if the point is inside any of the obstacles, False otherwise.
    """
    
    # TODO: Add functionality so not only does the point not collide with the obstacle, but also the entire dimensions of the robot. This will not only have to consider the robot as a Polygon consisting of its defined dimensions, but also the facing of said Polygon.
    
    for obstacle in obstacles:
        polygon = patches.Polygon(obstacle)
        if polygon.contains_point(point):
            return True
    return False


# TODO: Function `is_in_robot` to check not only whether we are colliding with an obstacle, but also whether we are colliding with another robot. Also, might check out this link: https://www.metanetsoftware.com/technique/tutorialA.html, for collision detection.


def distance(p1, p2):
    """
    Calculates the Euclidean distance between two points.
    """
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def nearest_vertex(tree, point):
    """
    Finds the vertex in the tree that is nearest to the given point. Remember, the tree is the set of paths that can be taken by the robot. The point is defined is given through a heuristic, in this case, generating it randomly.
    
    Args:
        tree (list): A list of vertices, where each vertex is a tuple representing the (x, y) coordinates.
        point (tuple): The (x, y) coordinates of the point.
        
    Returns:
        tuple: The (x, y) coordinates of the vertex in the tree that is nearest to the point.
    """
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
            random_point = (
                random.uniform(-SPACE_WIDTH/2, SPACE_WIDTH/2), 
                random.uniform(-SPACE_HEIGHT/2, SPACE_HEIGHT/2)
            )
        
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


def visualize_space(initial_positions, target_positions, obstacles, paths=None):
    """
    Once a simulation is run, this function can be used to visualize the space with the initial positions, target positions, obstacles, and the paths taken by the robots.
    
    Args:
        paths: List of paths, where each path is a list of (x,y) coordinates
    """
    fig, ax = plt.subplots()
    ax.set_xlim(-SPACE_WIDTH/2, SPACE_WIDTH/2)
    ax.set_ylim(-SPACE_HEIGHT/2, SPACE_HEIGHT/2)
    ax.set_aspect('equal')
    
    # Draw grid points
    for x in range(int(-SPACE_WIDTH), int(SPACE_WIDTH + 1)):
        for y in range(int(-SPACE_HEIGHT), int(SPACE_HEIGHT + 1)):
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
        rect = patches.Rectangle(
            (pos[0] - ROBOT_WIDTH/2, pos[1] - ROBOT_HEIGHT/2), 
            ROBOT_WIDTH, 
            ROBOT_HEIGHT, 
            edgecolor='none', 
            facecolor='lightgrey'
        )
        ax.add_patch(rect)
    
    # Draw paths
    if paths:
        for i, path in enumerate(paths):
            path_x, path_y = zip(*path)
            color = 'lightblue' if i == 0 else 'lightgreen'
            ax.plot(path_x, path_y, color=color)

    plt.gca().set_facecolor('white')
    plt.show()


def write_trajectory_to_file(path, file_name, group, team, robot):
    with open(file_name, 'w') as file:
        for i, (x, y) in enumerate(path):
            if i < 3:
                file.write(f"{x},{y},{group if i == 0 else team if i == 1 else robot}\n")
            else:
                file.write(f"{x},{y},0\n")


# Example usage
def main():
    initial_positions = parse_initial_positions('input/InitialPositions.txt')
    target_positions = parse_target_positions('input/TargetPositions.txt')
    obstacles = parse_obstacles('input')

    paths = []
    for i, initial_position in enumerate(initial_positions):
        tree, parent, target = rrt_star(initial_position, target_positions, obstacles)
        if target:
            path = extract_path(tree, parent, target)
            paths.append(path)
            write_trajectory_to_file(path, f"output/XY_303_1_{i+1}.txt", 303, 1, i+1)
        else:
            print(f"No path found for robot starting at {initial_position}.")

    # Visualize the space with paths for each robot
    visualize_space(initial_positions, target_positions, obstacles, paths)
    
    # Print in pretty format
    # print('Initial positions:', initial_positions)
    # print('Target positions:', target_positions)
    # print('Obstacles:')
    # for i, obstacle in enumerate(obstacles):
    #     print(f'Obstacle {i + 1}:', obstacle)
    

if __name__ == "__main__":    
    main()