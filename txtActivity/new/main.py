import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

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

def visualize_space(initial_positions, target_positions, obstacles):
    fig, ax = plt.subplots()
    ax.set_xlim(-2.25, 2.25)
    ax.set_ylim(-2.25, 2.25)
    ax.set_aspect('equal')
    
    # Draw grid points
    for x in range(-5, 6):
        for y in range(-5, 6):
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
    
    plt.gca().set_facecolor('white')
    plt.show()

# Example usage
initial_positions = parse_initial_positions('input/InitialPositions.txt')
target_positions = parse_target_positions('input/TargetPositions.txt')
obstacles = parse_obstacles('input')

visualize_space(initial_positions, target_positions, obstacles)

# Print in pretty format
print('Initial positions:', initial_positions)
print('Target positions:', target_positions)
print('Obstacles:')
for i, obstacle in enumerate(obstacles):
    print(f'Obstacle {i + 1}:', obstacle)


