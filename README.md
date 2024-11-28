# TC2008B - Reto Final: Simulación Multiagente de Tractores y Camiones en un Entorno Agrícola

## Integrantes del Equipo
- **Regina Cavazos Valdés**
- **Lorna Jaqueline García De León**
- **Pablo Andrés García Martínez**
- **Fernando Daniel Monroy Sánchez**
- **Diego Fernando Sabillon Chinchilla**
- **Brenda Sofía Sandoval**

---

## Requisitos Previos para clonar el repositorio

### Software Requerido
- **Python** (Versión 3.8 o superior)  
  [Descargar Python](https://www.python.org/downloads/)
- **Pip** (Administrador de paquetes de Python, incluido con Python)
- **Unity 3D** (Versión recomendada: 2022.3.51f1

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

## Ejecución

### Paso 1: Iniciar el Servidor Flask

Ejecuta el servidor Flask con:
```bash
python api/api.py
```

El servidor estará disponible en: http://127.0.0.1:5000 para probarlo utilizando herramientas externas como Postman o CURL.
Ejemplo POST por medio de CURL:

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

## Paso 2: Ejecutar la Simulación en Unity

1. Abre el proyecto Unity en `unity/My project`.
2. Abre la escena "Main Scene" que se encuentra dentro del directorio Assets > Scenes > Main Scene.
3. Haz click en el botón de play para visualizar la simulación.

---

## Estructura del Proyecto

### Directorios Principales
- **api/**: Código del servidor Flask para la simulación y control de agentes.
- **unity/My project/**: Escena de Unity con los modelos y movimientos.
- **tractor_statuses.json**: Archivo generado con el estado de los tractores en cada paso en la ejecución de la simulación mas reciente.
- **README.md**: Documentación del proyecto.




