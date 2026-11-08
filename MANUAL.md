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

El programa genera un grafo aleatorio no dirigido con una probabilidad de `0.3` para cada arista posible y busca un recubrimiento mínimo de vértices.

La salida contiene:

- **Tamaño del recubrimiento mínimo:** cantidad de vértices seleccionados.
- **Vértices del recubrimiento:** identificadores de los vértices seleccionados.
- **Tiempo de ejecución:** duración de la búsqueda, en segundos.

### Fijar semilla para repetir experimentos

La semilla se fija en `42` para que, al ejecutar el programa con el mismo valor de `n`, se genere el mismo grafo y se obtenga el mismo recubrimiento. El tiempo puede variar ligeramente y corresponde a la búsqueda; no incluye la generación del grafo.

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

## Experimentación con el algoritmo exacto

El punto 3 del trabajo pide aumentar `n` desde 10 y registrar los tiempos hasta que una ejecución supere una hora. El programa `experimento.py` automatiza las pruebas y guarda cada resultado en `resultados_experimento.csv`. Cada caso usa la misma semilla fija que el algoritmo exacto. Si un caso supera el límite de 3600 segundos, la ejecución se detiene y el CSV registra `>3600`.

Antes de iniciar la experimentación larga, se puede hacer una prueba acotada:

```bash
python experimento.py --desde 10 --hasta 12 --salida prueba.csv
```

Para realizar la serie solicitada, cerrar programas que no sean necesarios y ejecutar:

```bash
python experimento.py
```

El proceso puede durar mucho tiempo: la fuerza bruta crece exponencialmente. El CSV se actualiza después de cada tamaño probado, así que los resultados parciales quedan guardados si se interrumpe la corrida. Si se repite el experimento, indicar otro nombre con `--salida`, porque el programa no sobrescribe resultados existentes. Las mediciones dependen del equipo y de la carga del sistema; anotar el hardware y procurar no ejecutar otros procesos pesados durante la prueba.
