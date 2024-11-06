# Prototipo

## Introducción

Crear un sistema multiagente de pares de tractores cosechadores (cosechador) y camiones en donde se almacena aquello que se está cosechando (contenedor). Cada par de agentes funciona de la misma manera: el tractor avanza a través del campo de cultivos cosechándolos mientras el camión de almacenamiento avanza a la par. Mientras ambos van avanzando, el cosechador agarra la cosecha y va llenando el contenedor. El cosechador puede almacenar una cantidad menor que el contenedor por su cuenta, pero lo más óptimo es que el cosechador siempre almacene la cosecha en el contenedor mientras esté a su lado. Cuando el contenedor se llena, este se deacopla del cosechador y va a guardar al silo. Mientras tanto el cosechador sigue avanzando, almacenando la cosecha en su propio almacenaje interno pequeño.

Tenemos que generar algo con agent.py similar al de [Flocking Behaviour](https://agentpy.readthedocs.io/en/latest/agentpy_flocking.html). Debemos de generar las reglas de cada agente. Tendremos tres agentes principales: `Silo` (que almacena cosecha), `Plot` (que es donde se puede plantar una semilla), `Harvester` y `Container` (donde ambos son vehículos independientes que se mueven según las reglas de la simulación).

## Simulación

Para cada step, un tractor avanza una posición. Es decir, la velocidad de cada tractor a cada step es moverse hacia otra posición, o no moverse.

Primero plantear las variables que se buscarán optimizar (maximizar y minimizar).

Ejemplos de cosas que podríamos minimizar:

- Gasolina total gastada
- Distancia recorrida por cosechador
- Distancia recorrida por contenedor
    - También incluiría número de 
- Tiempo total para cosechar todo

Ejemplo de cosas que podríamos maximizar:

- Cosecha total

Qué debería de generar nuestro código?

- Archivos de puntos (coordenadas) hacia donde deberían de moverse los tractores

## FarmModel (ag.Model)

El tamaño del plano también determina la cantidad total de cosecha que puede estar almacenada

### Propiedades

- Tamaño del plano alrededor del origen (0,0)
    - Longitud (x) : `int`
    - Altitud (y) : `int`
- Steps : `int`
- Harvesters : `[Harvester]`
- Containers `[Containers]`
- Plots `[Plots]`
- Silos `[Silos]`

### Reglas

## HarvesterModel (ag.Agent)

### Propiedades

- Location (plot sobre el que ses encuentra) : `Plot`
- Max. gasolina : `int`
- Nivel gasolina : `int`
- Max. almacenaje : `int`
- Nivel de cosecha : `int`
- Distancia recorrida : `int`

### Reglas

1. No chocar con otro harvester o containers
2. Avanza solamente en cierta orientación según ubicación `Plot`: 
    - Si `Plot` tiene madurez > 0, solo puede avanzar en orientación del `Plot`
    - Si `Plot` tiene madurez == 0, puede avanzar en cualquier orientación. 
3. La ruta que toma maximiza la madurez de los `Plot` en su ruta mientras minimiza la distancia
4. Si en un step un `Harvester` está cosechando un `Plot`, para el siguiente step el `Plot` cambia de madurez a 0 (sin cosecha).

## ContainerModel (ag.Agent)

### Propiedades

- Location (plot sobre el que ses encuentra) : `Plot`
- Max. gasolina : `int`
- Nivel gasolina : `int`
- Max. almacenaje : `int`
- Nivel de cosecha : `int`
- Distancia recorrida : `int`

- Tiempo de descarga (de cosecha) : `int` (en steps)
- Silo más cercano : `Silo` (referencia)
- Harvester pair : `Harvester` (referencia)

### Reglas

1. No chocar con otros harvester o containers
2. Avanza solamente en cierta orientación según ubicación `Plot`: 
    - Si `Plot` tiene madurez > 0, solo puede avanzar en orientación del `Plot`
    - Si `Plot` tiene madurez == 0, puede avanzar en cualquier orientación.
3. Cuando su cosecha se llena, ir a silo más cercano

## PlotModel (ag.Agent)

Es la parcela donde crece una cosecha. La cosecha puede tener diferentes niveles de madurez. Debido a que las cosechas se plantan en zurcos con cierta orientación, esta será una limitante para los tractores que pasen, pues un tractor solo podrá avanzar en paralelo a la orientación de la parcela (si intentara avanzar en perpendicular, aplastaría la cosecha).

### Propiedades

- Location (x,y) : (`int`, `int`)
- Madurez de cosecha : `int`
    - Sin semilla / Ya cosechado : 0
    - En crecimiento : 1 - 9
    - Máximo estado de cosecha : 10
    - Cosecha caduca : >= 11
- Ángulo de dirección : `float`

### Reglas

## SiloModel (ag.Agent)

### Propiedades

- Location (x,y) : (`int`, `int`)
- Max. almacenaje : `int`
- Nivel de cosecha : `int`

### Reglas

1. Solamente un container puede descargar a la vez (podemos quitar esta regla para hacerlo más sencillo)


## IGNORAR ESTO:
```
## Crop (object)

- Madurez
```