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

