import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import matplotlib.animation as animation
import os

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load data using paths relative to the script directory
initial_positions = np.loadtxt(os.path.join(script_dir, 'InitialPositions.txt'))
obstacle1 = np.loadtxt(os.path.join(script_dir, 'Obstacle1.txt'))
obstacle2 = np.loadtxt(os.path.join(script_dir, 'Obstacle2.txt'))
obstacle3 = np.loadtxt(os.path.join(script_dir, 'Obstacle3.txt'))
obstacle4 = np.loadtxt(os.path.join(script_dir, 'Obstacle4.txt'))
targets_robot1 = np.loadtxt(os.path.join(script_dir, 'XY_104_2_1.txt'))  # Path coordinates for Robot 1
targets_robot2 = np.loadtxt(os.path.join(script_dir, 'XY_104_2_2.txt'))  # Path coordinates for Robot 2
target_positions = np.loadtxt(os.path.join(script_dir, 'TargetPositions.txt'))  # Target positions

obstacles = [obstacle1, obstacle2, obstacle3, obstacle4]

# Robot dimensions
robot_width = 0.16  # 0.16 m
robot_length = 0.20  # 0.20 m

# Configure figure
fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.grid(True)

# Plot obstacles
for obs in obstacles:
    x_coords = obs[0, :]
    y_coords = obs[1, :]
    ax.fill(x_coords, y_coords, 'r')

# Initial positions
hRobot1 = FancyBboxPatch(
    (initial_positions[0, 0] - robot_width / 2, initial_positions[0, 1] - robot_length / 2),
    robot_width,
    robot_length,
    boxstyle="round,pad=0.0",
    facecolor='m'
)
ax.add_patch(hRobot1)

hRobot2 = FancyBboxPatch(
    (initial_positions[1, 0] - robot_width / 2, initial_positions[1, 1] - robot_length / 2),
    robot_width,
    robot_length,
    boxstyle="round,pad=0.0",
    facecolor='m'
)
ax.add_patch(hRobot2)

# Plot target positions
# Assuming target_positions are in pairs of x and y
ax.plot(target_positions[0, :], target_positions[1, :], 'bo', markerfacecolor='b')

# Configure axes limits
ax.set_xlim([-3, 3])
ax.set_ylim([-2, 2])
ax.set_xlabel('X [m]')
ax.set_ylabel('Y [m]')

# Initialize robot paths
robot1_path_line, = ax.plot([], [], 'k-', linewidth=2)
robot2_path_line, = ax.plot([], [], 'r-', linewidth=2)

# Step size for interpolation
step_size = 0.01  # Adjust for smoother or faster movement

# Initialize current positions
current_pos1 = initial_positions[0, :]
current_pos2 = initial_positions[1, :]

# Prepare full paths for both robots
robot1_full_path = [current_pos1]
robot2_full_path = [current_pos2]

# Find the maximum number of steps between the two robots
max_steps = max(len(targets_robot1), len(targets_robot2))

# Generate interpolated positions for both robots
for i in range(max_steps):
    # Target positions
    target_pos1 = targets_robot1[i, :] if i < len(targets_robot1) else current_pos1
    target_pos2 = targets_robot2[i, :] if i < len(targets_robot2) else current_pos2

    # Compute distances and interpolation steps
    dist1 = np.linalg.norm(target_pos1 - current_pos1)
    dist2 = np.linalg.norm(target_pos2 - current_pos2)
    max_dist = max(dist1, dist2)
    num_interp_steps = int(np.ceil(max_dist / step_size))

    # Interpolate positions
    t_values = np.linspace(0, 1, num_interp_steps)
    for t in t_values:
        interp_pos1 = current_pos1 + t * (target_pos1 - current_pos1)
        interp_pos2 = current_pos2 + t * (target_pos2 - current_pos2)
        robot1_full_path.append(interp_pos1)
        robot2_full_path.append(interp_pos2)

    # Update current positions
    current_pos1 = target_pos1
    current_pos2 = target_pos2

# Convert paths to numpy arrays
robot1_full_path = np.array(robot1_full_path)
robot2_full_path = np.array(robot2_full_path)

# Animation functions
def init():
    hRobot1.set_xy((robot1_full_path[0, 0] - robot_width / 2, robot1_full_path[0, 1] - robot_length / 2))
    hRobot2.set_xy((robot2_full_path[0, 0] - robot_width / 2, robot2_full_path[0, 1] - robot_length / 2))
    robot1_path_line.set_data([], [])
    robot2_path_line.set_data([], [])
    return hRobot1, hRobot2, robot1_path_line, robot2_path_line

def animate(i):
    if i < len(robot1_full_path):
        pos1 = robot1_full_path[i]
        hRobot1.set_xy((pos1[0] - robot_width / 2, pos1[1] - robot_length / 2))
        robot1_path_line.set_data(robot1_full_path[:i + 1, 0], robot1_full_path[:i + 1, 1])
    if i < len(robot2_full_path):
        pos2 = robot2_full_path[i]
        hRobot2.set_xy((pos2[0] - robot_width / 2, pos2[1] - robot_length / 2))
        robot2_path_line.set_data(robot2_full_path[:i + 1, 0], robot2_full_path[:i + 1, 1])
    return hRobot1, hRobot2, robot1_path_line, robot2_path_line

# Create animation
num_frames = max(len(robot1_full_path), len(robot2_full_path))
ani = animation.FuncAnimation(
    fig,
    animate,
    frames=num_frames,
    init_func=init,
    blit=True,
    interval=10,
    repeat=False
)

plt.show()
