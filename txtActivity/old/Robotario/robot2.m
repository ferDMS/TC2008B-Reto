initial_positions = load('InitialPositions.txt');
obstacle1 = load('Obstacle1.txt');
obstacle2 = load('Obstacle2.txt');
obstacle3 = load('Obstacle3.txt');
obstacle4 = load('Obstacle4.txt');
targets_robot1 = load('XY_104_2_1.txt'); % Path coordinates for Robot 1
targets_robot2 = load('XY_104_2_2.txt'); % Path coordinates for Robot 2
target_positions = load('TargetPositions.txt'); % Target positions

obstacles = {obstacle1, obstacle2, obstacle3, obstacle4};

% tamaño
robot_width = 0.16; % 0.16 m
robot_length = 0.20; % 0.20 m

% Configurar figura
figure;
hold on;
axis equal;
grid on;

% Plot de obstaculo
for obs = 1:length(obstacles)
    for i = 1:size(obstacles{obs}, 2)
        % Extract x and y coordinates of the obstacle vertices
        x_coords = obstacles{obs}(1, :);
        y_coords = obstacles{obs}(2, :);
        
        % Draw the polygon
        fill(x_coords, y_coords, 'r');
    end
end

% Posicion inicial
hRobot1 = rectangle('Position', [initial_positions(1, 1)-robot_width/2, initial_positions(1, 2)-robot_length/2, robot_width, robot_length], 'Curvature', [1 1], 'FaceColor', 'm');
hRobot2 = rectangle('Position', [initial_positions(2, 1)-robot_width/2, initial_positions(2, 2)-robot_length/2, robot_width, robot_length], 'Curvature', [1 1], 'FaceColor', 'm');

% Plot de destinos
for i = 1:size(target_positions, 2)/2
    plot(target_positions(1, 2*i-1:2*i), target_positions(2, 2*i-1:2*i), 'bo', 'MarkerFaceColor', 'b');
end

% Configure axis 4 m x 6 m 
xlim([-3 3]);
ylim([-2 2]);
xlabel('X [m]');
ylabel('Y [m]');

robot1_path_x = [];
robot1_path_y = [];
robot2_path_x = [];
robot2_path_y = [];

% Find the maximum number of steps between the two robots
max_steps = max(size(targets_robot1, 1), size(targets_robot2, 1));

% Definir el tamaño del paso para la interpolación
step_size = 0.01; % Ajustar el tamaño del paso para un movimiento más suave o más rápido

% Encontrar el número máximo de pasos entre los dos robots
max_steps = max(size(targets_robot1, 1), size(targets_robot2, 1));

% Inicializar las posiciones actuales para ambos robots
current_pos1 = [initial_positions(1, 1), initial_positions(1, 2)];
current_pos2 = [initial_positions(2, 1), initial_positions(2, 2)];

% Inicializar los gráficos de las trayectorias
robot1_path = plot(current_pos1(1), current_pos1(2), 'k-', 'LineWidth', 2);
robot2_path = plot(current_pos2(1), current_pos2(2), 'r-', 'LineWidth', 2);

% Animar el movimiento de ambos robots simultáneamente
for i = 1:max_steps
    % Interpolar y mover Robot 1
    if i <= size(targets_robot1, 1)
        target_pos1 = [targets_robot1(i, 1), targets_robot1(i, 2)];
    else
        target_pos1 = current_pos1;
    end
    
    % Interpolar y mover Robot 2
    if i <= size(targets_robot2, 1)
        target_pos2 = [targets_robot2(i, 1), targets_robot2(i, 2)];
    else
        target_pos2 = current_pos2;
    end

    % Determinar el número de pasos de interpolación en función de la distancia más larga
    dist1 = norm(target_pos1 - current_pos1);
    dist2 = norm(target_pos2 - current_pos2);
    max_dist = max(dist1, dist2);
    num_interp_steps = ceil(max_dist / step_size);

    % Interpolar y actualizar las posiciones de ambos robots en paralelo
    for j = 1:num_interp_steps
        t = j / num_interp_steps;
        
        % Posiciones interpoladas
        interp_pos1 = current_pos1 + t * (target_pos1 - current_pos1);
        interp_pos2 = current_pos2 + t * (target_pos2 - current_pos2);
        
        % Actualizar posiciones de los robots
        set(hRobot1, 'Position', [interp_pos1(1)-robot_width/2, interp_pos1(2)-robot_length/2, robot_width, robot_length]);
        set(hRobot2, 'Position', [interp_pos2(1)-robot_width/2, interp_pos2(2)-robot_length/2, robot_width, robot_length]);

        % Actualizar y graficar la trayectoria de los robots
        robot1_path_x = get(robot1_path, 'XData');
        robot1_path_y = get(robot1_path, 'YData');
        robot1_path_x = [robot1_path_x, interp_pos1(1)];
        robot1_path_y = [robot1_path_y, interp_pos1(2)];
        set(robot1_path, 'XData', robot1_path_x, 'YData', robot1_path_y);

        robot2_path_x = get(robot2_path, 'XData');
        robot2_path_y = get(robot2_path, 'YData');
        robot2_path_x = [robot2_path_x, interp_pos2(1)];
        robot2_path_y = [robot2_path_y, interp_pos2(2)];
        set(robot2_path, 'XData', robot2_path_x, 'YData', robot2_path_y);

        % Pausar para simular el movimiento
        pause(0.01); % Ajustar la pausa para la velocidad
    end
    
    % Actualizar posiciones actuales para la siguiente iteración
    current_pos1 = target_pos1;
    current_pos2 = target_pos2;
end

hold off;;