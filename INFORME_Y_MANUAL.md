# Informe técnico y manual de ejecución

## Resolución del problema Minimum Vertex Cover mediante fuerza bruta

## 1. Introducción

Este proyecto implementa en Python una solución exacta al problema del **recubrimiento mínimo de vértices** (*Minimum Vertex Cover*). El programa genera un grafo aleatorio y determina el conjunto de menor tamaño que cubre todas sus aristas. Para hallar la solución, utiliza un algoritmo de fuerza bruta y la biblioteca NetworkX para la representación y generación de grafos.

En un grafo, un **vértice** representa un punto y una **arista** representa una conexión entre dos puntos. Un recubrimiento de vértices es un conjunto de vértices tal que cada arista tiene al menos uno de sus extremos en el conjunto. Se denomina mínimo cuando, entre todos los recubrimientos válidos, contiene la menor cantidad de vértices.

Por ejemplo, si un grafo contiene las aristas `A-B` y `B-C`, el conjunto `{B}` cubre ambas. En este caso, es un recubrimiento mínimo de tamaño 1.

## 2. Estructura del proyecto

- `vertex_cover.py`: genera el grafo, calcula el recubrimiento mínimo e imprime los resultados.
- `requirements.txt`: contiene la dependencia externa necesaria para ejecutar el programa: `networkx`.

## 3. Diseño y funcionamiento

El programa recibe como argumento el número de vértices `n` y genera un grafo aleatorio no dirigido mediante el modelo Erdős-Rényi. Cada arista posible se incluye con probabilidad `0.3` (30 %). Los vértices se identifican con números desde `0` hasta `n - 1`.

La función `vertex_cover_minimo` busca una solución exacta mediante los siguientes pasos:

1. Obtiene los vértices y las aristas del grafo.
2. Representa cada subconjunto con una máscara de bits. Para `n` vértices existen `2^n` subconjuntos posibles; en cada máscara, un bit en `1` indica que el vértice correspondiente está incluido y un bit en `0` indica que no lo está.
3. Recorre las máscaras y calcula cuántos vértices selecciona cada una. Omite las que no pueden mejorar la solución mínima encontrada.
4. Verifica si cada arista tiene al menos uno de sus extremos seleccionado.
5. Conserva la máscara válida de menor tamaño y devuelve los vértices correspondientes.

La exploración exhaustiva garantiza que el resultado sea mínimo. Sin embargo, la cantidad de subconjuntos crece exponencialmente con `n`: el algoritmo puede considerar hasta `2^n` máscaras y verificar las aristas para cada candidata. Por este motivo, el método es adecuado principalmente para grafos pequeños.

El tiempo informado corresponde a la búsqueda del recubrimiento y no incluye la generación del grafo.

## 4. Requisitos de ejecución

- Python instalado.
- Una terminal abierta en el directorio del proyecto.
- La dependencia `networkx`, instalada en un entorno virtual según el procedimiento de la sección siguiente.

## 5. Instalación y ejecución en MSYS2 UCRT64

Los comandos deben ejecutarse desde el directorio que contiene `vertex_cover.py` y `requirements.txt`.

### 5.1. Crear el entorno virtual e instalar la dependencia

En la primera ejecución, ingresar los siguientes comandos, uno por uno:

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install -r requirements.txt
```

La indicación `(.venv)` en el prompt confirma que el entorno virtual está activo. El entorno virtual permite instalar `networkx` sin modificar la instalación de Python administrada por MSYS2.

### 5.2. Ejecutar el programa

Con el entorno virtual activo, ejecutar:

```bash
python vertex_cover.py 10
```

El argumento numérico indica `n`, la cantidad de vértices. Por ejemplo, para ejecutar el programa con 12 o 15 vértices:

```bash
python vertex_cover.py 12
python vertex_cover.py 15
```

Si el entorno virtual no está activo, puede activarse nuevamente desde el directorio del proyecto con:

```bash
source .venv/Scripts/activate
```

Los comandos deben ingresarse sin incluir el símbolo `$` que muestra el prompt.

### 5.3. Desactivar el entorno virtual

Para finalizar el uso del entorno virtual:

```bash
deactivate
```

## 6. Interpretación de los resultados

El programa imprime tres datos:

- **Tamaño del recubrimiento mínimo**: cantidad de vértices de la solución.
- **Vértices del recubrimiento**: identificadores de los vértices seleccionados.
- **Tiempo de ejecución**: duración de la búsqueda, expresada en segundos.

El grafo se genera aleatoriamente, por lo que los vértices seleccionados y el tamaño de la solución pueden variar entre ejecuciones, incluso si se utiliza el mismo valor de `n`.

## 7. Limitaciones del método

La fuerza bruta garantiza una solución óptima, pero su costo aumenta rápidamente a medida que crece el número de vértices: cada vértice adicional duplica la cantidad de subconjuntos posibles. Por ejemplo, para `n = 10` existen `1.024` subconjuntos y para `n = 15`, `32.768`. En consecuencia, este método no resulta práctico para grafos grandes.
