# Manual de ejecución

## Requisitos

- Python 3.10 o superior.
- Una terminal abierta en el directorio que contiene `vertex_cover.py` y `requirements.txt`.

## Instalación en MSYS2 UCRT64

La primera vez, ejecutar estos comandos uno por uno:

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install -r requirements.txt
```

El indicador `(.venv)` en el prompt significa que el entorno virtual está activo. Este entorno permite instalar `networkx` sin modificar la instalación de Python administrada por MSYS2.

## Ejecución

Con el entorno virtual activo, indicar como argumento la cantidad de vértices:

```bash
python vertex_cover.py 10
```

También se puede usar, por ejemplo:

```bash
python vertex_cover.py 12
python vertex_cover.py 15
```

El programa genera un grafo aleatorio no dirigido con una probabilidad de `0.3` para cada arista posible y busca un recubrimiento mínimo de vértices. La semilla fija `42` hace que se genere siempre el mismo grafo para un mismo valor de `n`.

La salida contiene:

- **Tamaño del recubrimiento mínimo:** cantidad de vértices seleccionados.
- **Vértices del recubrimiento:** identificadores de los vértices seleccionados.
- **Tiempo de ejecución:** duración de la búsqueda, en segundos.

Para un mismo valor de `n`, el grafo y el recubrimiento se repiten en cada ejecución. Si se cambia `n`, se genera otro grafo. El tiempo puede variar ligeramente entre ejecuciones y corresponde a la búsqueda; no incluye la generación del grafo.

## Activar o salir del entorno virtual

Si se cierra la terminal, volver al directorio del proyecto y activar el entorno:

```bash
source .venv/Scripts/activate
```

Al finalizar, se puede salir del entorno virtual con:

```bash
deactivate
```

## Consideración sobre el algoritmo

La fuerza bruta examina hasta `2^n` subconjuntos. Encuentra una solución óptima, pero el tiempo de ejecución aumenta rápidamente a medida que crece la cantidad de vértices. Se recomienda usarlo con grafos pequeños.
