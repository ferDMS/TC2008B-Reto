# Reto: Sistema Multiagentes en Robotario

## Introducción

### Overview

El objetivo del reto es generar 2 archivos de texto, donde cada uno definirá una serie de coordenadas (X, Y) que representan una trayectoria o camino. Son 2 archivos de texto, uno para cada robot que existirá en el ambiente. El robot 1 es un robot físico, construido previamente por el Robotario. El robot 2 es un robot simulado, proyectado en el piso del Robotario. Independientemente de ser físico o proyectado, el objetivo es que ambos robots puedan avanzar a través de puntos objetivo determinados al inicio. Para pasar por estos puntos objetivo, el robot deberá atravesar los puntos trayectoria generados. Además, la trayectoria de ambos robots se deberá generar según condiciones iniciales del ambiente donde existen los robots y de manera que ambos nunca colisionen con ningún obstáculo en el ambiente (incluyendo los robots entre sí). Las condiciones iniciales son:

### Condiciones Iniciales

| Descripción                     | Archivo                | Formato                         |
| ------------------------------- | ---------------------- | ------------------------------- |
| Posición inicial de Robot 1 y 2 | `InitialPositions.txt` | x1,x2<br/>y1,y2                 |
| Posiciones objetivo             | `TargetPositions.txt`  | x1,x2,x3,x4<br/>y1,y2,y3,y4     |
| Esquinas de obstáculo           | `Obstacle_{i}.txt`     | x1,x2,x3,x4,…<br/>y1,y2,y3,y4,… |

Como se puede ver arriba, podrán existir múltiples archivos de obstáculos según el número de obstáculo $1, 2, 3, \ldots$. Un obstáculo siempre será una figura con 4 lados, como un cuadrado o rectángulo, que tendrá aristas entre los 4 vértices definidos en cada uno de los archivos. Es decir, el archivo `Obstacle_{i}.txt` siempre tendrá 4 puntos $X$ y 4 puntos $Y$, sin excepción.

Respecto a las posiciones iniciales y objetivo, el archivo `InitialPositions.txt` siempre tendrá exactamente 2 pares de coordenadas (x1, y1) y (x2, y2) para cada uno de los robots respectivamente. Además, el archivo `TargetPositions.txt` siempre tendrá minimamente 1 par de coordenadas (x1, y1) y no tiene cota superior en cantidad de posiciones objetivo. Recordar que estas posiciones objetivo son coordenadas por las cuales AMBOS robots tendrán que pasar durante la simulación.

Cada archivo tiene el siguiente formato:

- Fila 1: Posiciones en $X$ separadas por comas
- Fila 2: Posiciones en $Y$ separadas por comas

### Archivos a generar

Los archivos a generar, las coordenadas de la trayectoria de los robots, son los siguientes:

| Descripción             | Archivo          | Formato                                                                  |
| ----------------------- | ---------------- | ------------------------------------------------------------------------ |
| Trayectoria de Robot 1  | `XY_303_1_1.txt` | x1,y1,grupo<br/>x2,y2,equipo<br/>x3,y3,1<br/>x4,y4,0<br/>x5,y5,0<br/>... |
| Trayectoria del Robot 2 | `XY_303_1_2.txt` | x1,y1,grupo<br/>x2,y2,equipo<br/>x3,y3,2<br/>x4,y4,0<br/>x5,y5,0<br/>... |

El contenido de ambos archivos representa los puntos por los cuales los robots deberán de moverse, considerando que estos puntos esquivan los obstáculos en el plano y buscan pasar por cada posición objetivo.

Siendo la trayectoria generada un conjunto de puntos $T$ (trayectoria) y cada punto objetivo un conjunto de puntos $O$ (objetivo), podemos decir que $O \subseteq T$. Es decir, cada uno de los puntos objetivo deberá encontrarse en la serie de puntos trayectoria generados.

El nombre del archivo se determina en base a:

- Número de grupo de nuestra clase TC2008B
- Número de nuestro equipo en la clase
- Número de robot al que le queremos asignar la trayectoria

Considerando que somos el grupo **303** y el equipo **1**, los nombres de nuestros archivos deberán de ser:

- **XY_303_1_1.txt**
- **XY_303_1_2.txt**

El formato interior a ambos archivos generados es diferente a la de los archivos iniciales. El formato consistirá en un documento separado por comas que contiene exactamente 3 columnas: Posición en $X$, Posición en $Y$, Datos complementarios. Con datos complementarios nos referimos a los datos de grupo, equipo y robot que también se detallan en el nombre del archivo. Es decir, estos datos también deberán encontrarse en el contenido del archivo, en esta 3ra columna. Una vez que se hayan detallado los 3 datos complementarios (grupo, equipo, robot), las filas siguientes (de la fila 4 hacia adelante) únicamente tomarán en valor de $0$ en su lugar, como se puede ver en el ejemplo del formato.

La trayectoria de ambos robots se debe generar considerando la ejecución esperada de todo el sistema:

1. Primero, ambos robots estarán correctamente ubicados en sus posiciones iniciales, tal como se describen en `InitialPositions.txt`.
2. Al ejecutar la simulación del sistema, ambos robots avanzarán a través de cada punto trayectoria de manera simultánea a exactamente la misma velocidad.
3. Durante la ejecución ningún robot deberá colisionar con ninguno de los obstáculos en el ambiente ni entre sí.
4. Durante la ejecución cada robot deberá atravesar cada punto objetivo.
5. La ejecución finaliza cuando cada robot haya pasado por cada uno de los puntos trayectoria generados.

Tal como se menciona arriba, un punto de alta importancia a considerar son las colisiones de los robots con un obstáculo o robot.

### Colisiones entre objetos

Al generar los puntos trayectoria no solamente se deben de considerar las aristas de cada uno de los obstáculos (vértices definidos ya conectados), sino las dimensiones del robot y un pequeño margen de error. Es decir, se debe considerar:

- **Dimensiones del robot**: Ambos robots tienen las mismas dimensiones. A pesar de que el robot no tiene dimensiones cuadradas, deberemos considerar un espacio de colisión posible que sea cuadrado (como un square collider). Las dimensiones de este collider son de $0.18\ m$ de longitud y $0.20\ m$ de altura. Considerando que el robot siempre es colocado inicialmente "viendo" en un ángulo de 90 grados (hacia el norte), las dimensiones iniciales son $(0.18\ m\ X,\ 0.20\ m\ Y)$.

- **Margen de Error**: Debido a que es una prioridad muy alta es no colisionar con ningún robot ni obstáculo, para cada objeto que exista en el ambiente queremos agregar un margen de error de $0.05\ m$. Es decir, siempre se mantendrá esta distancia segura del "square collider" de cada robot a cualquier otro objeto en el ambiente, incluyendo aristas de obstáculos u otros "square collider" de otros robots.

### Visualizando la simulación

Con el objetivo de analizar de manera visual la generación de las trayectorias de los robots, también crearemos figuras en un espacio 2D que simulen la ejecución de los puntos iniciales, los puntos objetivo, los puntos trayectoria, los obstáculos y los robots.

En primer lugar es necesario describir el escenario 2D.

El espacio tiene una altura de $4.5\ m$ y longitud de $6.5\ m$. El fondo del mismo es blanco. Sobre el fondo, existen marcas, puntos negros, a lo largo del plano con el objetivo de tener una mejor perspectiva de las dimensiones del plano. Por ello, los puntos negros están colocados todos en una formación tipo "grid", a $0.5\ m$ de distancia entre cada uno. Existe un punto negro sobre el origen $(0,0)$, desde el cual se designan las posiciones de los demás puntos negros.

Aparte del fondo descrito, también se deben de visualizar los robots y los puntos que existen en el plano:

- Puntos iniciales: Círculos de radio $0.1\ m$, con outline negro y sin fill.
- Puntos objetivo: Círculos de radio $0.1\ m$, sin outline y con fill azul.
- Puntos trayectoria: Círculos de radio $0.025\ m$, con outline negro y sin fill.
- Obstáculos: Polígono formado conectando todos los vértices del mismo, sin outline y con fill rojo.
- Robots: Rectángulo de dimensiones $0.18\ m\times 0.20\ m$, sin outline y con fill gris claro.

Una configuración ejemplo se puede observar en la siguiente imagen:

![](assets/image.png)

## Algoritmo

Como referencia, se utilizó la implementación que se encuentra en el siguiente artículo de Medium: https://medium.com/@aggorjefferson/exploring-path-planning-with-rrt-and-visualization-in-python-cf5bd80a6cd6

En el mismo se detalla el algoritmo de exploración de caminos para robots *Rapidly-exploring Random Tree* (RRT). Este algoritmo se utiliza para resolver los desafíos que enfrentan los robots autónomos al intentar encontrar un ruta de un punto inicial a uno objetivo a la vez que se evitan obstáculos en el camino. La versión optimizada del algoritmo, RRT\*, intenta encontrar no solamente un camino, sino uno óptimo, el más corto posible.

El algoritmo se ve de la siguiente manera:

![](assets/rrt_example.gif)

El código del algoritmo utiliza dos clases: `Node`, un punto en el plano perteneciente al grafo dirigido que representa posibles rutas del robot, y `RRTStar`, el objeto que orquestra la ejecución del algoritmo y contiene los parámetros iniciales del sistema.

Dadas estas condiciones iniciales del ambiente, la secuencia de alto nivel del algoritmo es la siguiente:

1. Generar un nuevo punto de manera aleatoria en el plano como referencia.
2. Obtener el nodo en nuestros caminos posibles (grafo) más cercano al nuevo punto.
3. Crear un nuevo nodo desde el nodo más cercano en dirección hacia el punto generado. El nuevo nodo estará a una distancia exacta del nodo más cercano y puede no equivaler al punto aleatorio generado.
4. Checar colisiones del nuevo nodo. En caso de ser un punto válido, optimizar las rutas hacia el nuevo nodo y rutas hacia nodos vecinos.
5. Si el nuevo nodo es exactamente el nodo objetivo, encontramos un camino posible.
6. De no ser el nodo objetivo, continuar la ejecución hasta llegar al objetivo.

Ahora, la ejecución del algoritmo a fondo:

1. Generar un nuevo punto de manera aleatoria en el plano, `rand_node`. Este punto será un nuevo punto de referencia para guiarnos. Es decir, lo utilizaremos como guía hacia el objetivo. Debido a que queremos que sea una guía, asignaremos una probabilidad `prob_goal_node = 0.2` de que nuestra guía nos lleve hacia el nodo objetivo. Esta heurística nos ayuda a explorar de manera diversa el espacio pero también a dirigir nuestros esfuerzos hacia el nodo objetivo.

2. Obtener el nodo trayectoria más cercano al nuevo `rand_node`. Es decir, de entre la lista de todos los puntos anteriormente calculados como posibles rutas (nuestro árbol dirigido), encontraremos el nodo más cercano al nodo de referencia generado. Para hacer esto calculamos la distancia euclediana de cada nodo `node_list[i]` hacia el generado `rand_node` como `dist_list[i]`. El nodo que más cercano, de menor distancia, será el elegido, como `nearest_node`.

3. Dirigir el árbol desde `nearest_node` en dirección hacia `rand_node`. Crearemos un nuevo nodo `new_node` a cierta distancia `step_size` del nodo más cercano `nearest_node` en dirección hacia `rand_node`. Es decir, obtenemos el ángulo de `nearest_node` hacia `rand_node`, y avanzamos en esa dirección unicamente una distancia `step_size`.
   
   - Una cosa a considerar es que si `rand_node` equivale a nuestro nodo objetivo `goal_node` y además la distancia euclediana entre ambos nodos `nearest_node` y `rand_node` es menor al `step_size`, vamos a querer crear nuestro `new_node` en exactamente la posición del nodo objetivo. Es decir, en este caso la conexión entre `nearest_node` y `new_node` sería menor a `step_size` de manera que podamos conectar directamente con la ubicación del `goal_node`.

4. Checar que el nodo generado no colisione con un obstáculo. Para checar esto se pueden utilizar librerías para detectar colisión de puntos dentro de polígonos así como métodos para evitar colisiones de aristas (edges) dentro de obstáculos, por ejemplo, con `shapely.geometry import Point, LineString, Polygon`. En caso de colisionar, el nodo nunca se agrega a nuestras rutas posibles y empezaremos una nueva generación aleatoria. En caso de librar la colisión, se buscan todos los nodos vecinos a `new_node` dentro de un radio `search_radius` utilizando la distancia euclediana para empezar a optimizar las conexiones entre nodos. Esta es la principal diferencia entre RRT y RRT\*.
   
   - Sabemos que a través de nuestras ejecuciones, empezaremos a tener muchos muchos nodos. Debido a esto, nos gustaría siempre mantener sus conexiones lo más cortas posibles. Con el objetivo de hacer esto, intentaremos determinar un el mejor nodo padre `best_node` para nuestro nuevo nodo `new_node` según la distancia más corta para llegar a ese nuevo nodo `new_node`. Para hacer esto, iteramos cada nodo vecino `neighbors[i]` y calculamos la distancia euclediana hacia el `new_node` como `dist[i]`. Considerando la distancia total acumulada hasta cada `neighbors[i]`, el nodo vecino que proporcione la distancia más corta acumulada hacia `new_node` (definida como `neighbors[i].cost` + `dist[i]`) será elegido como padre. La elección de padre debe ser libre de colisiones.
   
   - Una vez que se confirma una ruta óptima hacia `new_node` desde un `best_node`, se agrega el `new_node` a la lista nodos en nuestro árbol `node_list[i]`.
   
   - Después de escoger de manera óptima el padre de `new_node`, también queremos optimizar las rutas hacia estos mismos nodos `neighbors[i]` en caso de que una ruta que atraviece `new_node` sea más eficiente que cualquiera anterior hacia estos `neighbors`. Para hacerlo usamos nuevamente la distancia euclediana entre `new_node` y cada `neighbors[i]` y las guardamos como `dist[i]`. Si una ruta que pase por el `new_node` hacia cada nodo vecino es más óptima que una anterior (`new_node.cost + dist[i] < neighbors[i].cost`) entonces hacemos "rewiring" de la ruta del vecino. La elección de ruta optimizada debe ser libre de colisiones.

5. En caso de que la ubicación de `new_node` sea exactamente igual a `goal_node` significa que hemos logrado llegar al punto objetivo y hemos optimizado las rutas para llegar al mismo con una distancia tan corta como fuera posible. Para regresar la ruta completa, se realiza reconstruye la ruta a través de cada nodo padre desde `new_node` hasta el nodo origen inicial con padre `None`.

6. En caso de no haber completado la ejecución hacia el `goal_node`, continuar las generaciones nuevos puntos aleatorios.