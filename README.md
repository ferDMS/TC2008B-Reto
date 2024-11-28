# TC2008B - Reto Final: Simulación Multiagente de Tractores y Camiones en un Entorno Agrícola

## Integrantes del Equipo
- **Regina Cavazos Valdés**
- **Lorna Jaqueline García De León**
- **Pablo Andrés García Martínez**
- **Fernando Daniel Monroy Sánchez**
- **Diego Fernando Sabillon Chinchilla**
- **Brenda Sofía Sandoval**

---

## Introducción

Este proyecto consiste en el desarrollo de una simulación multiagente que modela el comportamiento de tractores cosechadores (**Harvesters**) y camiones contenedores (**Containers**) en un entorno agrícola. Los agentes interactúan de forma autónoma en tareas de cosecha, almacenamiento y transporte. La simulación también incluye elementos adicionales como:

- **Plots** (áreas de cultivo)
- **Silo** (almacenamiento central)
- Puntos de abastecimiento de combustible

La implementación se realizó utilizando **Python**, **Unity 3D** y un sistema de comunicación mediante una **REST API**.

---

## Requisitos Previos

### Software Requerido
- **Python** (Versión 3.8 o superior)  
  [Descargar Python](https://www.python.org/downloads/)
- **Pip** (Administrador de paquetes de Python, incluido con Python)
- **Unity 3D** (Versión recomendada: 2021.3 o superior)

### Librerías Python
Ejecuta el siguiente comando para instalar las dependencias:
```bash
pip install flask agentpy numpy pygame
```
# Instalación y Configuración

## Paso 1: Clonar el Repositorio
Clona este repositorio en tu máquina local:
```bash
git clone https://github.com/ferDMS/TC2008B-Reto/.git
```
## Paso 2: Configurar Parámetros de Simulación

Puedes personalizar los parámetros de la simulación enviando una solicitud POST al endpoint `/initialize`. Los parámetros configurables incluyen:

- `plant_grid_size`: Tamaño del área de cultivo.
- `path_width`: Ancho de los caminos alrededor de los cultivos.
- `num_tractors`: Número de tractores.
- `water_capacity`: Capacidad de agua de los tractores.
- `fuel_capacity`: Capacidad de combustible.
- `steps`: Número de pasos de simulación.

---

## Ejecución

### Paso 1: Iniciar el Servidor Flask

Ejecuta el servidor Flask con:
```bash
python api/<nombre_del_archivo>.py
```

El servidor estará disponible en: http://127.0.0.1:5000.

### Paso 2: Inicializar la Simulación
Envía una solicitud POST para inicializar la simulación. Por ejemplo:

```bash
curl -X POST http://127.0.0.1:5000/initialize \
-H "Content-Type: application/json" \
-d '{
  "plant_grid_size": 5,
  "path_width": 2,
  "num_tractors": 3,
  "water_capacity": 10,
  "fuel_capacity": 20,
  "steps": 50
}'
```

## Paso 3: Ejecutar la Simulación en Unity

1. Abre el proyecto Unity en `unity/My project`.
2. Ejecuta la escena principal para visualizar la simulación.

---

## Estructura del Proyecto

### Directorios Principales
- **api/**: Código del servidor Flask para la simulación y control de agentes.
- **unity/My project/**: Escena de Unity con los modelos y movimientos.
- **tractor_statuses.json**: Archivo generado con el estado de los tractores en cada paso.
- **README.md**: Documentación del proyecto.

---

## Características Clave

### Protocolos de Interacción
1. **Cosecha**: Los Harvesters solo avanzan a Plots con madurez > 0 y cosechan hasta completar su capacidad.
2. **Almacenamiento**: Los Containers almacenan cosecha y la transportan al Silo cuando están llenos.
3. **Evitar Colisiones**: Ningún agente puede ocupar el mismo espacio al mismo tiempo.
4. **Recarga de Combustible**: Ambos agentes priorizan reabastecimiento cuando el nivel de combustible es bajo.
5. **Sincronización**: Solo un Container puede descargar en el Silo simultáneamente.

### Simulación Gráfica en Unity
- Modelado rápido con figuras primitivas y Prefabs reutilizables.
- Iluminación dinámica para condiciones diurnas y nocturnas.
- Texturas realistas y movimientos naturales usando **Lerp** y **splines**.

### REST API
- Comunicación entre Python y Unity para la toma de decisiones en tiempo real.
- Generación de un archivo JSON para exportar trayectorias de los agentes.

---

## Resultados

### Salida
La simulación genera un archivo `tractor_statuses.json`, con datos como:
- **Posición**.
- **Tarea actual**.
- **Niveles de agua y combustible**.
- **Capacidad de trigo almacenado**.
- **Flexibilidad**: El modelo puede adaptarse a diferentes configuraciones sin requerir cambios extensivos en la implementación.
- **Escalabilidad**: Es posible agregar más agentes o modificar las reglas existentes para abarcar nuevas dinámicas.
- **Visualización**: La representación gráfica interactiva facilita el análisis del sistema y su comunicación a audiencias no técnicas.

### Desventajas
- **Complejidad**: La implementación requiere conocimientos avanzados en modelado multiagente, programación y simulación gráfica.
- **Costos Computacionales**: La simulación puede ser intensiva en recursos, limitando su ejecución en sistemas con hardware modesto.

---

## Reflexión

Este proyecto permitió aplicar conocimientos teóricos y prácticos en el diseño y ejecución de sistemas multiagente. Destacamos la importancia de las interacciones dentro de sistemas complejos, donde cada agente tiene un rol crucial en el funcionamiento del entorno agrícola.  

La integración de **Unity** para la simulación gráfica y **Python** con una **REST API** para la lógica del modelo multiagente fortaleció el enfoque colaborativo y práctico del equipo. El uso de datos en tiempo real y la generación de resultados exportables también amplió las aplicaciones futuras de este modelo.

Comparado con las expectativas iniciales, este proyecto ayudó al equipo a consolidar habilidades en programación, simulación y comunicación técnica, destacando la utilidad de las herramientas seleccionadas.

---

## Contribuciones

Cada miembro del equipo contribuyó de manera significativa al éxito del proyecto, colaborando en diferentes áreas clave:

- **Desarrollo del modelo multiagente**: Definición de reglas y comportamiento autónomo para los agentes.
- **Diseño gráfico y simulación en Unity**: Implementación de la visualización gráfica y dinámica de la simulación.
- **Integración REST API**: Comunicación fluida entre la simulación y la lógica del modelo en Python.
- **Documentación y análisis de resultados**: Creación de informes claros y útiles para la comprensión y presentación del proyecto.

