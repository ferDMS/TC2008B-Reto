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
import numpy as np
from shapely.geometry import Point, LineString, Polygon, box
from shapely.affinity import rotate

# Dimensions of robot (m)
ROBOT_WIDTH = 0.18
ROBOT_HEIGHT = 0.20
# Dimensions of space (m)
SPACE_WIDTH = 6.5
SPACE_HEIGHT = 6.5
# Margin of error (m)
MARGIN = 0.05
# Effective dimensions including margin
EFFECTIVE_ROBOT_WIDTH = ROBOT_WIDTH + 2 * MARGIN
EFFECTIVE_ROBOT_HEIGHT = ROBOT_HEIGHT + 2 * MARGIN


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


# TODO: Function `is_in_robot` to check not only whether we are colliding with an obstacle, but also whether we are colliding with another robot. Also, might check out this link: https://www.metanetsoftware.com/technique/tutorialA.html, for collision detection.


# Node class representing a state in the space
class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None
        self.cost = 0

# RRT* algorithm class
class RRTStar:
    def __init__(self, start, goal, obstacles, map_size, step_size=0.05, max_iter=2000, goal_bias=0.1):
        self.start = Node(start[0], start[1])
        self.goal = Node(goal[0], goal[1])
        self.obstacles = obstacles
        self.map_size = map_size
        self.step_size = step_size
        self.max_iter = max_iter
        self.node_list = [self.start]
        self.goal_region_radius = 0.1  # As per considerations
        self.search_radius = 0.3       # As per considerations
        self.path = None
        self.goal_reached = False
        self.goal_bias = goal_bias
        # Convert obstacles to shapely Polygons and add margin
        self.obstacle_polygons = [Polygon(obstacle).buffer(MARGIN) for obstacle in self.obstacles]

    # General utility methods
    def calc_distance(self, node1, node2):
        return math.hypot(node2.x - node1.x, node2.y - node1.y)

    def calc_distance_and_angle(self, from_node, to_node):
        dx = to_node.x - from_node.x
        dy = to_node.y - from_node.y
        distance = math.hypot(dx, dy)
        theta = math.atan2(dy, dx)
        return distance, theta

    # Method updated to use shapely for collision detection
    def is_in_obstacle(self, node):
        """
        Check if the robot at the given node position and orientation intersects any obstacle.
        """
        # Determine the orientation (theta) of the robot
        if node.parent:
            dx = node.x - node.parent.x
            dy = node.y - node.parent.y
            theta = math.degrees(math.atan2(dy, dx))
        else:
            theta = 0  # Default orientation if no parent
        
        # Create a rectangle representing the robot's dimensions at the node's position
        robot_rect = box(
            node.x - EFFECTIVE_ROBOT_WIDTH / 2,
            node.y - EFFECTIVE_ROBOT_HEIGHT / 2,
            node.x + EFFECTIVE_ROBOT_WIDTH / 2,
            node.y + EFFECTIVE_ROBOT_HEIGHT / 2
        )
        # Rotate the rectangle to represent the robot's facing direction
        robot_polygon = rotate(robot_rect, angle=theta, origin=(node.x, node.y))
        
        # Check for collision with any obstacle
        for polygon in self.obstacle_polygons:
            if robot_polygon.intersects(polygon):
                return True
        return False

    # Updated to check collision along the edge between nodes
    def is_collision_free_path(self, node1, node2):
        """
        Check if the path between node1 and node2 is collision-free,
        considering the robot's dimensions and facing at each sampled point.
        """
        distance = self.calc_distance(node1, node2)
        if distance == 0:
            # Nodes are at the same position, check collision at this point
            temp_node = Node(node1.x, node1.y)
            temp_node.parent = node1.parent
            return not self.is_in_obstacle(temp_node)
        num_samples = max(int(distance / self.step_size), 1)
        for i in range(num_samples + 1):
            t = i / num_samples
            x = node1.x + t * (node2.x - node1.x)
            y = node1.y + t * (node2.y - node1.y)
            # Create a temporary node for collision checking
            temp_node = Node(x, y)
            temp_node.parent = node1
            if self.is_in_obstacle(temp_node):
                return False
        return True

    # Updated to use is_collision_free_path for edge collision detection
    def is_collision_free(self, node):
        if self.is_in_obstacle(node):
            return False
        if not (-self.map_size[0]/2 <= node.x <= self.map_size[0]/2 and
                -self.map_size[1]/2 <= node.y <= self.map_size[1]/2):
            return False
        # Check collision along the path from parent to current node
        if node.parent and not self.is_collision_free_path(node.parent, node):
            return False
        return True

    # Methods in the order they are called in plan()
    def get_random_node(self):
        if random.random() < self.goal_bias:
            return Node(self.goal.x, self.goal.y)
        else:
            return Node(
                random.uniform(-self.map_size[0]/2, self.map_size[0]/2),
                random.uniform(-self.map_size[1]/2, self.map_size[1]/2)
            )

    def get_nearest_node(self, rand_node):
        distances = [self.calc_distance(node, rand_node) for node in self.node_list]
        min_index = distances.index(min(distances))
        return self.node_list[min_index]

    def steer(self, from_node, to_node):
        distance, theta = self.calc_distance_and_angle(from_node, to_node)
        distance = min(self.step_size, distance)
        new_node = Node(
            from_node.x + distance * math.cos(theta),
            from_node.y + distance * math.sin(theta)
        )
        new_node.cost = from_node.cost + distance
        new_node.parent = from_node
        return new_node

    def find_neighbors(self, new_node):
        neighbors = []
        for node in self.node_list:
            if self.calc_distance(node, new_node) <= self.search_radius:
                neighbors.append(node)
        return neighbors

    def choose_parent(self, neighbors, nearest_node, new_node):
        best_cost = nearest_node.cost + self.calc_distance(nearest_node, new_node)
        best_node = nearest_node
        for node in neighbors:
            cost = node.cost + self.calc_distance(node, new_node)
            if cost < best_cost and self.is_collision_free_path(node, new_node):
                best_cost = cost
                best_node = node
        new_node.cost = best_cost
        new_node.parent = best_node
        return new_node

    def rewire(self, new_node, neighbors):
        for node in neighbors:
            cost_through_new = new_node.cost + self.calc_distance(new_node, node)
            if cost_through_new < node.cost and self.is_collision_free_path(new_node, node):
                node.parent = new_node
                node.cost = cost_through_new

    def reached_goal(self, node):
        distance = self.calc_distance(node, self.goal)
        return distance <= self.goal_region_radius

    def generate_final_path(self, goal_node):
        path = []
        node = goal_node
        while node is not None:
            path.append((node.x, node.y))
            node = node.parent
        return path[::-1]  # Reverse the path
    
    # Place plan() as the last method
    def plan(self):
        for _ in range(self.max_iter):
            rand_node = self.get_random_node()
            nearest_node = self.get_nearest_node(rand_node)
            new_node = self.steer(nearest_node, rand_node)

            if self.is_collision_free(new_node):
                neighbors = self.find_neighbors(new_node)
                new_node = self.choose_parent(neighbors, nearest_node, new_node)
                self.node_list.append(new_node)
                self.rewire(new_node, neighbors)

                if self.reached_goal(new_node):
                    self.path = self.generate_final_path(new_node)
                    self.goal_reached = True
                    return

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
        rrt_star = RRTStar(
            start=initial_position,
            goal=target_positions[2],
            obstacles=obstacles,
            map_size=(SPACE_WIDTH, SPACE_HEIGHT),
            step_size=0.1,
            max_iter=20000,
            goal_bias=0.3
        )
        rrt_star.plan()
        if rrt_star.path:
            path = rrt_star.path
            paths.append(path)
            write_trajectory_to_file(
                path,
                f"output/XY_303_1_{i+1}.txt",
                303,
                1,
                i+1
            )
        else:
            print(f"No path found for robot starting at {initial_position}.")

    # Visualize the space with paths for each robot
    visualize_space(initial_positions, target_positions, obstacles, paths)

if __name__ == "__main__":    
    main()