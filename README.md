# TP Final: Recubrimiento de Vértices

Este trabajo práctico implementa en Python una solución exacta al problema del **recubrimiento mínimo de vértices** (*Minimum Vertex Cover*).

Un grafo está formado por vértices (puntos) y aristas (conexiones). Un recubrimiento de vértices es un conjunto de puntos que toca todas las conexiones: cada arista debe tener al menos uno de sus extremos seleccionado. El programa genera un grafo aleatorio y encuentra el recubrimiento válido de menor tamaño mediante fuerza bruta.

## Requisitos

- Python 3.10 o superior.
- `networkx`, que se instala desde `requirements.txt`.

## Instalación y ejecución

Desde una terminal abierta en la carpeta del proyecto, crear y activar un entorno virtual e instalar la dependencia:

```bash
python -m venv .venv
```

En MSYS2 UCRT64, activar el entorno e instalar NetworkX:

```bash
source .venv/Scripts/activate
python -m pip install -r requirements.txt
```

Ejecutar el programa indicando la cantidad de vértices deseada:

```bash
python vertex_cover.py 10
```

El número `10` es la cantidad de vértices del grafo. También se puede reemplazar por otros valores, por ejemplo `12` o `15`.

El programa informa el tamaño del recubrimiento mínimo, los vértices seleccionados y el tiempo empleado en la búsqueda. Se usa una semilla fija (`42`), por lo que para un mismo valor de `n` se genera el mismo grafo y se obtiene el mismo recubrimiento en cada ejecución.

Para instrucciones más detalladas, consultar el [manual de ejecución](MANUAL.md).

## Método y limitaciones

La búsqueda de fuerza bruta prueba los subconjuntos posibles de vértices, representados mediante máscaras de bits, y verifica cuáles cubren todas las aristas. Al revisar todas las posibilidades, garantiza encontrar una solución mínima. Sin embargo, para `n` vértices hay hasta `2^n` subconjuntos, por lo que el método está destinado a grafos pequeños.
