# Manual de ejecución

Guía paso a paso para instalar el entorno y correr cada programa del trabajo.
Para una visión general del proyecto, ver el [README](README.md).

## Requisitos

- Python 3.10 o superior.
- Una terminal abierta en la carpeta que contiene los scripts `.py` y
  `requirements.txt`.

## Instalación del entorno

La primera vez, crear el entorno virtual:

```bash
python -m venv .venv
```

Activarlo según la terminal que se use:

```bash
source .venv/bin/activate        # Linux, macOS y MSYS2 UCRT64
# .venv\Scripts\activate         # Windows nativo (cmd o PowerShell)
```

> En MSYS2 UCRT64 (entorno tipo Unix sobre Windows) el entorno virtual se crea
> con la carpeta `bin/`, igual que en Linux/macOS. Solo el Python nativo de
> Windows usa `Scripts/`.

El indicador `(.venv)` en el prompt significa que el entorno está activo.
Con el entorno activo, instalar las dependencias:

```bash
python -m pip install -r requirements.txt
```

Para salir del entorno virtual, usar `deactivate`.

## Punto 2 — Algoritmo exacto

Resuelve el recubrimiento mínimo por fuerza bruta. Recibe como argumento la
cantidad de vértices:

```bash
python punto2_exacto.py 10
python punto2_exacto.py 15
```

El programa genera un grafo aleatorio no dirigido (probabilidad `0.3` por
arista, semilla fija `42`) y busca el recubrimiento mínimo. La salida muestra:

- **Vértices** y **aristas** del grafo generado (para poder verificar el
  resultado a mano: cada arista debe tocar al menos un vértice del cover).
- **Tamaño del recubrimiento mínimo** y los **vértices** que lo forman.
- **Tiempo de ejecución** de la búsqueda (no incluye la generación del grafo).

## Punto 5 — Heurística

Resuelve el mismo problema con la heurística voraz de máximo grado. Mismo uso:

```bash
python punto5_heuristica.py 10
```

La salida agrega la línea **Recubrimiento válido: sí/no**, que confirma que el
resultado cubre todas las aristas. Como usa la misma semilla, trabaja sobre el
mismo grafo que el algoritmo exacto para cada `n`.

## Punto 3 — Experimentación con el algoritmo exacto

`punto3_experimento.py` aumenta `n` desde 10 de a uno y registra los tiempos hasta que
un caso supere el límite (una hora por defecto). Cada caso se corre en un
proceso aparte para poder cortarlo por tiempo. Los resultados se guardan en un
CSV dentro de `datos/`, y el archivo se actualiza después de cada tamaño, así
que si se interrumpe la corrida no se pierde lo ya medido.

Prueba acotada (rápida, recomendada antes de la corrida larga):

```bash
python punto3_experimento.py --desde 10 --hasta 12 --salida datos/prueba.csv
```

Serie completa solicitada por la consigna (puede durar **horas**):

```bash
python punto3_experimento.py --salida datos/resultados.csv
```

Si un caso supera los 3600 segundos, la ejecución se detiene y el CSV registra
`>3600` en la columna de tiempo. El programa **no sobrescribe** un CSV que ya
exista: para repetir el experimento, elegir otro nombre con `--salida`.

Opciones: `--desde`, `--hasta`, `--limite-segundos`, `--salida`.

> **Condiciones de prueba.** Las mediciones dependen del equipo y de la carga
> del sistema. Conviene cerrar otros programas, anotar el hardware usado y no
> ejecutar procesos pesados durante la corrida.

## Punto 4 — Gráficos

`punto4_grafico.py` lee el CSV del punto 3 y genera dos gráficos (escala lineal y
logarítmica) en la carpeta `graficos/`, además de imprimir una tabla con los
cocientes `tiempo(n)/tiempo(n-1)`:

```bash
python punto4_grafico.py                              # lee datos/resultados.csv
python punto4_grafico.py --entrada datos/prueba.csv   # otro CSV
```

Genera `graficos/grafico_tiempo_lineal.png` y `graficos/grafico_tiempo_log.png`.

## Punto 6 — Comparación exacto vs. heurística

`punto6_comparacion.py` compara calidad (¿la heurística alcanzó el óptimo?), error
relativo y tiempos. Tiene dos modos:

```bash
# Mide ambos algoritmos en este equipo (n=10..15 por defecto)
python punto6_comparacion.py --salida datos/comparacion.csv

# Reutiliza los tiempos del exacto ya medidos (punto 3) y solo corre la
# heurística; sirve para cubrir n grandes sin volver a medir el exacto
python punto6_comparacion.py --entrada datos/resultados.csv --salida datos/comparacion_completa.csv
```

El CSV de salida incluye metadatos (aristas, semilla, versiones de NetworkX y
Python, plataforma) para que la comparación sea reproducible. Igual que el
experimento, **no sobrescribe** un archivo existente.

Opciones: `--entrada`, `--desde`, `--hasta`, `--repeticiones`, `--salida`.

## Punto 7 — Escalabilidad de la heurística

`punto7_escalabilidad.py` corre la heurística sobre grafos grandes (`n ≥ 1000`),
tamaños que el algoritmo exacto nunca podría resolver, para analizar cómo crece
su tiempo y si es viable en casos reales. Mide solo la heurística (no la
generación del grafo), repite cada tamaño y reporta la mediana.

```bash
python punto7_escalabilidad.py                           # n = 1000..5000
python punto7_escalabilidad.py --tamanos 1000 2000 5000 --repeticiones 3
```

Guarda `datos/escalabilidad.csv` (n, aristas, tamaño del cover, tiempo mediano y
metadatos) y, si matplotlib está instalado, `graficos/escalabilidad_tiempo.png`.
Igual que los otros scripts, **no sobrescribe** un CSV existente.

Opciones: `--tamanos`, `--repeticiones`, `--probabilidad`, `--salida`.

> **Memoria.** Con `p = 0.3` la cantidad de aristas crece como ~n²/2: por
> ejemplo, `n = 5000` genera ~3,75 millones de aristas. Conviene subir `n` de a
> poco y vigilar el uso de RAM; si falta memoria, reducir los tamaños.

## Nota sobre la complejidad

La fuerza bruta examina hasta `2^n` subconjuntos: encuentra siempre el óptimo,
pero su tiempo crece exponencialmente, por lo que solo es práctica con grafos
pequeños. La heurística es polinomial (`O(n² + m)`): es mucho más rápida y
escala a grafos grandes, pero no garantiza el tamaño mínimo.
