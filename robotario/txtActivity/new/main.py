"""
Generador de Rutas para Robots

TC2008B
Grupo: 303
Equipo: 1
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation

# Dimensiones del robot (m)
ANCHO_ROBOT = 0.18
ALTO_ROBOT = 0.20
# Dimensiones del espacio (m)
ANCHO_ESPACIO = 6.5
ALTO_ESPACIO = 4.5
# Margen de error (m)
MARGEN = 0.035
# Dimensiones efectivas incluyendo el margen
ANCHO_ROBOT_EFECTIVO = ANCHO_ROBOT + 2 * MARGEN
ALTO_ROBOT_EFECTIVO = ALTO_ROBOT + 2 * MARGEN
# Agrega estas variables globales después de las dimensiones existentes
VELOCIDAD_ROBOT = 0.02  # metros por cuadro
ALFA_RUTA = 0.3   # transparencia de las líneas de la ruta


def parse_initial_positions(file_path):
    """
    Analiza las posiciones iniciales de los robots desde un archivo.

    Args:
        file_path (str): La ruta al archivo que contiene las posiciones iniciales.

    Returns:
        tuple: Una tupla que contiene tuplas, cada una representando las coordenadas (x, y) de las posiciones iniciales.
            Por ejemplo: ((x1, y1), (x2, y2), ...)
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()
        # Elimina los espacios en blanco, divide por comas, convierte a flotantes y convierte el iterador en lista
        x_positions = list(map(float, lines[0].strip().split(',')))
        y_positions = list(map(float, lines[1].strip().split(',')))
    return tuple(zip(x_positions, y_positions))


def parse_target_positions(file_path):
    """
    Analiza las posiciones objetivo de los robots desde un archivo.
    
    Args:
        file_path (str): La ruta al archivo que contiene las posiciones objetivo.
    
    Returns:
        list: Una lista de tuplas, cada una representando las coordenadas (x, y) de las posiciones objetivo.
            Por ejemplo: [(x1, y1), (x2, y2), ...]
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()
        x_positions = list(map(float, lines[0].strip().split(',')))
        y_positions = list(map(float, lines[1].strip().split(',')))
    return list(zip(x_positions, y_positions))


def parse_obstacles(directory_path):
    """
    Analiza las definiciones de coordenadas de los obstáculos desde múltiples archivos.
    
    Args:
        directory_path (str): La ruta al directorio que contiene cero o más archivos que contienen los vértices del obstáculo. Cada archivo sigue la convención de nomenclatura: Obstacle_<número>.txt.
        
    Returns:
        list: Una lista de listas, cada una representando un obstáculo. Cada obstáculo es una lista de tuplas, donde cada tupla contiene las coordenadas (x, y) de un vértice.
               Por ejemplo: [[(x1, y1), (x2, y2), (x3, y3), (x4, y4)], ...]
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


# TODO: Función `is_in_robot` para verificar no solo si estamos colisionando con un obstáculo, sino también si estamos colisionando con otro robot. También, podría revisar este enlace: https://www.metanetsoftware.com/technique/tutorialA.html, para la detección de colisiones.


# Clase Nodo que representa un estado en el espacio
class Nodo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.padre = None
        self.costo = 0

# Clase del algoritmo RRT*
class RRTStar:
    def __init__(self, inicio, objetivo, obstaculos, tamano_mapa, tamano_paso=0.05, max_iter=2000, objetivo_bias=0.1, umbral_mejora=0.01, max_iter_sin_mejora=100):
        self.inicio = Nodo(inicio[0], inicio[1])
        self.objetivo = Nodo(objetivo[0], objetivo[1])
        self.obstaculos = obstaculos
        self.tamano_mapa = tamano_mapa
        self.tamano_paso = tamano_paso
        self.max_iter = max_iter
        self.lista_nodos = [self.inicio]
        self.radio_region_objetivo = 0.1  # Según consideraciones
        self.radio_busqueda = 0.3       # Según consideraciones
        self.ruta = None
        self.objetivo_alcanzado = False
        self.objetivo_bias = objetivo_bias
        self.umbral_mejora = umbral_mejora
        self.max_iter_sin_mejora = max_iter_sin_mejora
        # Convierte los obstáculos a Polígonos de shapely y agrega el margen
        self.poligonos_obstaculos = [Polygon(obstaculo).buffer(MARGEN) for obstaculo in self.obstaculos]

    # Métodos de utilidad general
    def calcular_distancia(self, nodo1, nodo2):
        return math.hypot(nodo2.x - nodo1.x, nodo2.y - nodo1.y)

    def calcular_distancia_y_angulo(self, desde_nodo, hacia_nodo):
        dx = hacia_nodo.x - desde_nodo.x
        dy = hacia_nodo.y - desde_nodo.y
        distancia = math.hypot(dx, dy)
        theta = math.atan2(dy, dx)
        return distancia, theta

    # Método actualizado para usar shapely para la detección de colisiones
    def esta_en_obstaculo(self, nodo):
        """
        Verifica si el robot en la posición del nodo dado y orientación interseca algún obstáculo.
        """
        # Determina la orientación (theta) del robot
        if nodo.padre:
            dx = nodo.x - nodo.padre.x
            dy = nodo.y - nodo.padre.y
            theta = math.degrees(math.atan2(dy, dx))
        else:
            theta = 0  # Orientación predeterminada si no hay padre
        
        # Crea un rectángulo que representa las dimensiones del robot en la posición del nodo
        rectangulo_robot = box(
            nodo.x - ANCHO_ROBOT_EFECTIVO / 2,
            nodo.y - ALTO_ROBOT_EFECTIVO / 2,
            nodo.x + ANCHO_ROBOT_EFECTIVO / 2,
            nodo.y + ALTO_ROBOT_EFECTIVO / 2
        )
        # Rota el rectángulo para representar la dirección de frente del robot
        poligono_robot = rotate(rectangulo_robot, angle=theta, origin=(nodo.x, nodo.y))
        
        # Verifica la colisión con cualquier obstáculo
        for poligono in self.poligonos_obstaculos:
            if poligono_robot.intersects(poligono):
                return True
        return False

    # Actualizado para verificar colisión a lo largo del borde entre nodos
    def es_camino_libre_de_colision(self, nodo1, nodo2):
        """
        Verifica si el camino entre nodo1 y nodo2 está libre de colisiones,
        considerando las dimensiones y orientación del robot en cada punto muestreado.
        """
        distancia = self.calcular_distancia(nodo1, nodo2)
        if distancia == 0:
            # Los nodos están en la misma posición, verifica la colisión en este punto
            nodo_temporal = Nodo(nodo1.x, nodo1.y)
            nodo_temporal.padre = nodo1.padre
            return not self.esta_en_obstaculo(nodo_temporal)
        num_muestras = max(int(distancia / self.tamano_paso), 1)
        for i in range(num_muestras + 1):
            t = i / num_muestras
            x = nodo1.x + t * (nodo2.x - nodo1.x)
            y = nodo1.y + t * (nodo2.y - nodo1.y)
            # Crea un nodo temporal para verificar la colisión
            nodo_temporal = Nodo(x, y)
            nodo_temporal.padre = nodo1
            if self.esta_en_obstaculo(nodo_temporal):
                return False
        return True

    # Actualizado para usar es_camino_libre_de_colision para la detección de colisiones en el borde
    def es_libre_de_colision(self, nodo):
        if self.esta_en_obstaculo(nodo):
            return False
        if not (-self.tamano_mapa[0]/2 <= nodo.x <= self.tamano_mapa[0]/2 and
                -self.tamano_mapa[1]/2 <= nodo.y <= self.tamano_mapa[1]/2):
            return False
        # Verifica la colisión a lo largo del camino desde el padre hasta el nodo actual
        if nodo.padre and not self.es_camino_libre_de_colision(nodo.padre, nodo):
            return False
        return True

    # Métodos en el orden en que se llaman en plan()
    def obtener_nodo_aleatorio(self):
        if random.random() < self.objetivo_bias:
            return Nodo(self.objetivo.x, self.objetivo.y)
        else:
            return Nodo(
                random.uniform(-self.tamano_mapa[0]/2, self.tamano_mapa[0]/2),
                random.uniform(-self.tamano_mapa[1]/2, self.tamano_mapa[1]/2)
            )

    def obtener_nodo_mas_cercano(self, nodo_aleatorio):
        distancias = [self.calcular_distancia(nodo, nodo_aleatorio) for nodo in self.lista_nodos]
        indice_minimo = distancias.index(min(distancias))
        return self.lista_nodos[indice_minimo]

    def dirigir(self, desde_nodo, hacia_nodo):
        distancia, theta = self.calcular_distancia_y_angulo(desde_nodo, hacia_nodo)
        distancia = min(self.tamano_paso, distancia)
        nuevo_nodo = Nodo(
            desde_nodo.x + distancia * math.cos(theta),
            desde_nodo.y + distancia * math.sin(theta)
        )
        nuevo_nodo.costo = desde_nodo.costo + distancia
        nuevo_nodo.padre = desde_nodo
        return nuevo_nodo

    def encontrar_vecinos(self, nuevo_nodo):
        vecinos = []
        for nodo in self.lista_nodos:
            if self.calcular_distancia(nodo, nuevo_nodo) <= self.radio_busqueda:
                vecinos.append(nodo)
        return vecinos

    def elegir_padre(self, vecinos, nodo_mas_cercano, nuevo_nodo):
        mejor_costo = nodo_mas_cercano.costo + self.calcular_distancia(nodo_mas_cercano, nuevo_nodo)ons and addile_polygonleIleleGeneralty methodseeeeeeee_andlefrome, toetoefrometoefromeeeethod updated to usefor collision detectionis_inleeCheck if theat the given nodetion andtiots anyaclee thetioof theerenteerenteerentDefault orientation ifrentte aangling the robot'ss at the node'stion_recteEFFECTIVEWIDTHeEFFECTIVEHEIGHTeEFFECTIVEWIDTHeEFFECTIVEHEIGHTte theangle to the robot's facing directionrobot_y_recteeCheck forlwith anyacleyle_polygonrobot_yyUpdated to checklon along the edge betweeneis_collision_free_patheeCheck if the path betweene1 ande2 isl-freeconsidering the robot'ss and facing at each sampled pointeeeeeNodes are at the sametiochecklon at this pointtemp_nodeeeetemp_noderenterentis_inle(temp_nodesamplesestep_sizesamplessampleseeeeeete aary node forlon checkingtemp_nodeetemp_noderenteis_inle(temp_node    # Updated to use is_collision_free_path for edgel detectionisl_freeeis_inlee_sizee_size_sizee_sizeChecklon along the path fromrent to currenteerentis_collision_free_patherenteethods in ther they are called inget_random_nodegoalegoalgoalemap_sizemap_sizemap_sizemap_size    def get_nearest_node(self, rand_node):
        mejor_nodo = nodo_mas_cercano
        for nodo in vecinos:
            costo = nodo.costo + self.calcular_distancia(nodo, nuevo_nodo)
            if costo < mejor_costo and self.es_camino_libre_de_colision(nodo, nuevo_nodo):
                mejor_costo = costo
                mejor_nodo = nodo
        nuevo_nodo.costo = mejor_costo
        nuevo_nodo.padre = mejor_nodo
        return nuevo_nodo

    def reorganizar(self, nuevo_nodo, vecinos):
        for nodo in vecinos:
            costo_a_traves_de_nuevo = nuevo_nodo.costo + self.calcular_distancia(nuevo_nodo, nodo)
            if costo_a_traves_de_nuevo < nodo.costo and self.es_camino_libre_de_colision(nuevo_nodo, nodo):
                nodo.padre = nuevo_nodo
                nodo.costo = costo_a_traves_de_nuevo

    def alcanzo_objetivo(self, nodo):
        distancia = self.calcular_distancia(nodo, self.objetivo)
        return distancia <= self.radio_region_objetivo

    def generar_ruta_final(self, nodo_objetivo):
        ruta = []
        nodo = nodo_objetivo
        while nodo is not None:
            ruta.append((nodo.x, nodo.y))
            nodo = nodo.padre
        return ruta[::-1]  # Invierte la ruta
    
    # Coloca plan() como el último método
    def planificar(self):
        mejor_costo = float('inf')
        contador_sin_mejora = 0

        for _ in range(self.max_iter):
            nodo_aleatorio = self.obtener_nodo_aleatorio()
            nodo_mas_cercano = self.obtener_nodo_mas_cercano(nodo_aleatorio)
            nuevo_nodo = self.dirigir(nodo_mas_cercano, nodo_aleatorio)

            if self.es_libre_de_colision(nuevo_nodo):
                vecinos = self.encontrar_vecinos(nuevo_nodo)
                nuevo_nodo = self.elegir_padre(vecinos, nodo_mas_cercano, nuevo_nodo)
                self.lista_nodos.append(nuevo_nodo)
                self.reorganizar(nuevo_nodo, vecinos)

                if self.alcanzo_objetivo(nuevo_nodo):
                    costo_actual = nuevo_nodo.costo
                    if costo_actual < mejor_costo:
                        mejor_costo = costo_actual
                        self.ruta = self.generar_ruta_final(nuevo_nodo)
                        self.objetivo_alcanzado = True
                        contador_sin_mejora = 0
                    else:
                        contador_sin_mejora += 1

                    if contador_sin_mejora >= self.max_iter_sin_mejora:
                        break

def asegurar_directorio_salida():
    """Crea el directorio de salida si no existe."""
    os.makedirs('output', exist_ok=True)


            if self.is_collision_free(new_node):
                neighbors = self.find_neighbors(new_node)
                new_node = self.choose_parent(neighbors, nearest_node, new_node)
                self.node_list.append(new_node)
                self.rewire(new_node, neighbors)

                if self.reached_goal(new_node):
                    current_cost = new_node.cost
                    if current_cost < best_cost:
                        best_cost = current_cost
                        self.path = self.generate_final_path(new_node)
                        self.goal_reached = True
                        no_improvement_count = 0
                    else:
                        no_improvement_count += 1

                    if no_improvement_count >= self.max_no_improvement_iter:
                        break

def ensure_output_directory():
    """Crea el directorio de salida si no existe."""
    os.makedirs('output', exist_ok=True)

def visualize_space(initial_positions, target_positions, obstacles, paths=None):
    """
    Visualiza el espacio con las posiciones iniciales, posiciones objetivo, obstáculos, caminos,
    y anima a los robots moviéndose a lo largo de sus caminos.
    """
    fig, ax = plt.subplots()
    ax.set_xlim(-SPACE_WIDTH/2, SPACE_WIDTH/2)
    ax.set_ylim(-SPACE_HEIGHT/2, SPACE_HEIGHT/2)
    ax.set_aspect('equal')
    
    # Dibujar puntos de la cuadrícula
    for x in range(int(-SPACE_WIDTH), int(SPACE_WIDTH + 1)):
        for y in range(int(-SPACE_HEIGHT), int(SPACE_HEIGHT + 1)):
            ax.plot(x * 0.5, y * 0.5, 'ko', markersize=2)
    
    # Dibujar posiciones iniciales
    for pos in initial_positions:
        circle = patches.Circle(pos, 0.1, edgecolor='black', facecolor='none')
        ax.add_patch(circle)
    
    # Dibujar posiciones objetivo
    for pos in target_positions:
        circle = patches.Circle(pos, 0.1, edgecolor='none', facecolor='blue')
        ax.add_patch(circle)
    
    # Dibujar obstáculos
    for obstacle in obstacles:
        polygon = patches.Polygon(obstacle, edgecolor='none', facecolor='red')
        ax.add_patch(polygon)
    
    if paths:
        # Dibujar caminos con alpha reducido
        for i, path in enumerate(paths):
            path_x, path_y = zip(*path)
            color = 'blue' if i == 0 else 'green'
            ax.plot(path_x, path_y, color=color, linewidth=2, alpha=PATH_ALPHA, label=f'Camino Robot {i+1}')
        
        # Crear parches de robots
        robots = []
        robot_colors = ['blue', 'green']
        for i, pos in enumerate(initial_positions):
            robot = patches.Rectangle(
                (pos[0] - ROBOT_WIDTH/2, pos[1] - ROBOT_HEIGHT/2),
                ROBOT_WIDTH,
                ROBOT_HEIGHT,
                edgecolor='none',
                facecolor=robot_colors[i]
            )
            ax.add_patch(robot)
            robots.append(robot)
        
        # Calcular distancia total para cada camino
        path_distances = []
        for path in paths:
            total_dist = 0
            for i in range(len(path)-1):
                dx = path[i+1][0] - path[i][0]
                dy = path[i+1][1] - path[i][1]
                total_dist += math.sqrt(dx*dx + dy*dy)
            path_distances.append(total_dist)
        
        # Calcular número de cuadros necesarios
        max_distance = max(path_distances)
        num_frames = int(max_distance / ROBOT_SPEED) + 1
        
        def update(frame):
            # Calcular distancia recorrida
            distance = frame * ROBOT_SPEED
            
            # Actualizar posición de cada robot
            for robot_idx, (robot, path) in enumerate(zip(robots, paths)):
                # Encontrar posición a lo largo del camino en la distancia actual
                current_dist = 0
                current_pos = path[0]
                
                for i in range(len(path)-1):
                    dx = path[i+1][0] - path[i][0]
                    dy = path[i+1][1] - path[i][1]
                    segment_dist = math.sqrt(dx*dx + dy*dy)
                    
                    if current_dist + segment_dist >= distance:
                        # Interpolar posición
                        t = (distance - current_dist) / segment_dist
                        current_pos = (
                            path[i][0] + t * dx,
                            path[i][1] + t * dy
                        )
                        break
                    current_dist += segment_dist
                    if i == len(path)-2:  # Si está al final del camino
                        current_pos = path[-1]
                
                # Actualizar posición del robot
                robot.set_xy((current_pos[0] - ROBOT_WIDTH/2, current_pos[1] - ROBOT_HEIGHT/2))
            
            return robots
        
        # Crear y guardar animación
        ensure_output_directory()  # Agregar esta línea
        anim = FuncAnimation(
            fig, update, frames=num_frames,
            interval=20, blit=True
        )
        anim.save('output/simulation.gif', writer='pillow')
    
    plt.legend()
    plt.gca().set_facecolor('white')
    plt.show()

def write_trajectory_to_file(path, file_name, group, team, robot):
    ensure_output_directory()  # Agregar esta línea
    with open(file_name, 'w') as file:
        for i, (x, y) in enumerate(path):
            if i < 3:
                file.write(f"{x},{y},{group if i == 0 else team if i == 1 else robot}\n")
            else:
                file.write(f"{x},{y},0\n")


def load_paths_from_directory(directory):
    """
    Carga los caminos para los robots desde un directorio especificado.

    Args:
        directory (str): La ruta al directorio que contiene los archivos de camino.

    Returns:
        list: Una lista de caminos, donde cada camino es una lista de coordenadas (x, y).
    """
    paths = []
    for robot_number in [1, 2]:
        file_path = os.path.join(directory, f"XY_303_1_{robot_number}.txt")
        path = []
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                x, y, _ = line.strip().split(',')
                path.append((float(x), float(y)))
        paths.append(path)
    return paths

def generate_paths():
    initial_positions = parse_initial_positions('input/InitialPositions.txt')
    target_positions = parse_target_positions('input/TargetPositions.txt')
    obstacles = parse_obstacles('input')
    
    # Definir el orden para cada robot
    robot_1_order = [1, 2, 4, 5, 3, 7, 6]
    robot_2_order = [7, 3, 6, 1, 2, 4, 5]
    
    # Reordenar posiciones objetivo para cada robot
    robot_1_targets = [target_positions[i - 1] for i in robot_1_order]
    robot_2_targets = [target_positions[i - 1] for i in robot_2_order]
    
    paths = []
    for i, (initial_position, targets) in enumerate(zip(initial_positions, [robot_1_targets, robot_2_targets])):
        path = []
        current_position = initial_position
        robot_number = i + 1
        all_positions = [current_position] + targets
        for j in range(len(targets)):
            start_point = all_positions[j]
            end_point = all_positions[j + 1]
            print(f"Calculando desde el punto {j} al punto {j+1} para el Robot {robot_number}...")
            start_time = time.time()
            rrt_star = RRTStar(
                start=start_point,
                goal=end_point,
                obstacles=obstacles,
                map_size=(SPACE_WIDTH, SPACE_HEIGHT),
                step_size=0.5,
                max_iter=30000,
                goal_bias=0.2,
                improvement_threshold=0.01,
                max_no_improvement_iter=1000
            )
            rrt_star.plan()
            end_time = time.time()
            if rrt_star.path:
                segment_path = rrt_star.path
                if j > 0:
                    # Evitar puntos duplicados entre segmentos
                    segment_path = segment_path[1:]
                path.extend(segment_path)
                print(f"Camino obtenido en {end_time - start_time:.2f} segundos.")
            else:
                print(f"No se encontró camino desde el punto {j} al punto {j+1} para el Robot {robot_number}.")
                break
        if path:
            paths.append(path)
            write_trajectory_to_file(
                path,
                f"output/XY_303_1_{robot_number}.txt",
                303,
                1,
                robot_number
            )
        else:
            print(f"No se pudo generar el camino para el Robot {robot_number}.")

    # Visualizar el espacio con los caminos para cada robot
    visualize_space(initial_positions, target_positions, obstacles, paths)

def main():
    print("Reto: Sistema Multiagentes en Robotario")
    print("1. Generar caminos")
    print("2. Cargar caminos")
    print("3. Salir")
    
    choice = input("Ingrese su elección (1-3): ")
    
    if choice == '1':
        generate_paths()
    elif choice == '2':
        directory_number = input("Ingrese el número de directorio para cargar los caminos: ")
        directory = f"./best/{directory_number}/"
        paths = load_paths_from_directory(directory)
        initial_positions = parse_initial_positions('input/InitialPositions.txt')
        target_positions = parse_target_positions('input/TargetPositions.txt')
        obstacles = parse_obstacles('input')
        visualize_space(initial_positions, target_positions, obstacles, paths)
    elif choice == '3':
        sys.exit()
    else:
        print("Elección inválida. Por favor ingrese 1, 2 o 3.")

if __name__ == "__main__":
    main()