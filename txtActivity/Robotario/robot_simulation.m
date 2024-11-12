% Read the data from the text files
initial_positions = load('InitialPositions.txt');
obstacle1 = load('Obstacle1.txt');
obstacle2 = load('Obstacle2.txt');
obstacle3 = load('Obstacle3.txt');
obstacle4 = load('Obstacle4.txt');
targets_robot1 = load('XY_104_2_1.txt'); % Path coordinates for Robot 1
targets_robot2 = load('XY_104_2_2.txt'); % Path coordinates for Robot 2
target_positions = load('TargetPositions.txt'); % Target positions

% Combine all obstacle data into one cell array
obstacles = {obstacle1, obstacle2, obstacle3, obstacle4};

% Define the size of robots
robot_width = 0.16; % 0.16 meters (width of the robot)
robot_length = 0.20; % 0.20 meters (length of the robot)

% Set up the figure
figure;
hold on;
axis equal;
grid on;

% Plot each obstacle as a polygon using its vertices
for obs = 1:length(obstacles)
    for i = 1:size(obstacles{obs}, 2)
        % Extract x and y coordinates of the obstacle vertices
        x_coords = obstacles{obs}(1, :);
        y_coords = obstacles{obs}(2, :);
        
        % Draw the polygon
        fill(x_coords, y_coords, 'r');
    end
end

% Plot the initial positions of the robots as magenta rectangles
hRobot1 = rectangle('Position', [initial_positions(1, 1)-robot_width/2, initial_positions(1, 2)-robot_length/2, robot_width, robot_length], 'Curvature', [1 1], 'FaceColor', 'm');
hRobot2 = rectangle('Position', [initial_positions(2, 1)-robot_width/2, initial_positions(2, 2)-robot_length/2, robot_width, robot_length], 'Curvature', [1 1], 'FaceColor', 'm');

% Plot the target positions as blue circles
for i = 1:size(target_positions, 2)/2
    plot(target_positions(1, 2*i-1:2*i), target_positions(2, 2*i-1:2*i), 'bo', 'MarkerFaceColor', 'b');
end

% Configure axis to match 4 m x 6 m field
xlim([-3 3]); % Set x-axis limits from -3 m to 3 m (total 6 m)
ylim([-2 2]); % Set y-axis limits from -3 m to 3 m (total 6 m)
xlabel('X [m]');
ylabel('Y [m]');

% Initialize arrays to store the path for plotting
robot1_path_x = [];
robot1_path_y = [];
robot2_path_x = [];
robot2_path_y = [];

% Find the maximum number of steps between the two robots
max_steps = max(size(targets_robot1, 1), size(targets_robot2, 1));

% Animate the movement of both robots simultaneously
for i = 1:max_steps
    % Update Robot 1 position if it has more steps
    if i <= size(targets_robot1, 1)
        set(hRobot1, 'Position', [targets_robot1(i, 1)-robot_width/2, targets_robot1(i, 2)-robot_length/2, robot_width, robot_length]);
        % Update the path for Robot 1
        robot1_path_x = [robot1_path_x; targets_robot1(i, 1)];
        robot1_path_y = [robot1_path_y; targets_robot1(i, 2)];
        % Plot the updated path for Robot 1
        plot(robot1_path_x, robot1_path_y, 'k-', 'LineWidth', 2);
    end
    
    % Update Robot 2 position if it has more steps
    if i <= size(targets_robot2, 1)
        set(hRobot2, 'Position', [targets_robot2(i, 1)-robot_width/2, targets_robot2(i, 2)-robot_length/2, robot_width, robot_length]);
        % Update the path for Robot 2
        robot2_path_x = [robot2_path_x; targets_robot2(i, 1)];
        robot2_path_y = [robot2_path_y; targets_robot2(i, 2)];
        % Plot the updated path for Robot 2
        plot(robot2_path_x, robot2_path_y, 'r-', 'LineWidth', 2);
    end
    
    pause(0.1); 
end

hold off;
