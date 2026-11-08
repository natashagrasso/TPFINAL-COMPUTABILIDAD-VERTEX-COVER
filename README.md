# TP Final: Recubrimiento de Vértices (Minimum Vertex Cover)

Trabajo final de **Teoría de la Computabilidad** (UADER – FCyT). Implementa y
compara una solución **exacta** (fuerza bruta) y una **heurística** (voraz de
máximo grado) para el problema del recubrimiento mínimo de vértices, analizando
su tiempo de ejecución y escalabilidad.

Un grafo está formado por vértices (puntos) y aristas (conexiones). Un
*recubrimiento de vértices* es un conjunto de puntos que toca todas las
conexiones: cada arista debe tener al menos uno de sus extremos en el conjunto.
El problema consiste en hallar el recubrimiento de menor tamaño posible, y es
**NP-difícil**: no se conoce un algoritmo eficiente que lo resuelva de forma
exacta para grafos grandes.

## Estructura del proyecto

```
.
├── punto2_exacto.py         # Punto 2: algoritmo exacto (fuerza bruta)
├── punto3_experimento.py    # Punto 3: mide tiempos del exacto para n creciente
├── punto4_grafico.py        # Punto 4: genera los gráficos de tiempo
├── punto5_heuristica.py     # Punto 5: heurística voraz de máximo grado
├── punto6_comparacion.py    # Punto 6: compara exacto vs. heurística
├── punto7_escalabilidad.py  # Punto 7: mide la heurística para n grandes (>=1000)
├── datos/                   # CSV generados (resultados y comparaciones)
├── graficos/                # Imágenes generadas (gráficos de tiempo)
├── requirements.txt         # Dependencias de Python
├── README.md                # Este archivo
└── MANUAL.md                # Manual de ejecución detallado
```

## Correspondencia con la consigna

| Punto | Tema | Archivo(s) |
|-------|------|------------|
| 2 | Algoritmo exacto | `punto2_exacto.py` |
| 3 | Experimentación del exacto | `punto3_experimento.py` → `datos/resultados.csv` |
| 4 | Análisis gráfico | `punto4_grafico.py` → `graficos/*.png` |
| 5 | Heurística | `punto5_heuristica.py` |
| 6 | Comparación exacto vs. heurística | `punto6_comparacion.py` → `datos/comparacion*.csv` |
| 7 | Escalabilidad de la heurística (n≥1000) | `punto7_escalabilidad.py` → `datos/escalabilidad_final.csv`, `graficos/escalabilidad_tiempo.png` |

La corrida del punto 7 midió `n = 1000, 2000, 3000, 4000 y 5000`, con tres
repeticiones por tamaño. Los tiempos medianos fueron de 0,351 a 13,714 segundos.
Los resultados completos y el análisis están en [MANUAL.md](MANUAL.md).

## Requisitos

- Python 3.10 o superior.
- Las dependencias de `requirements.txt` (`networkx`, `pandas`, `matplotlib`).

## Instalación

Desde una terminal abierta en la carpeta del proyecto, crear el entorno virtual:

```bash
python -m venv .venv
```

Activarlo (la ruta depende de la terminal):

```bash
source .venv/bin/activate        # Linux, macOS y MSYS2 UCRT64
# .venv\Scripts\activate         # Windows nativo (cmd o PowerShell)
```

Instalar las dependencias:

```bash
python -m pip install -r requirements.txt
```

## Ejecución rápida

```bash
# Punto 2 — resolver un grafo de 10 vértices con el algoritmo exacto
python punto2_exacto.py 10

# Punto 5 — resolver el mismo grafo con la heurística
python punto5_heuristica.py 10

# Punto 3 — experimentación de tiempos del exacto (tarda; ver MANUAL.md)
python punto3_experimento.py --desde 10 --hasta 12 --salida datos/prueba.csv

# Punto 4 — gráficos a partir del CSV de resultados
python punto4_grafico.py

# Punto 6 — comparar los mismos casos medidos en el punto 3
python punto6_comparacion.py --entrada datos/resultados.csv --salida datos/comparacion_nueva.csv

# Punto 7 — escalabilidad de la heurística para n grandes
python punto7_escalabilidad.py
```

Las instrucciones detalladas (experimentación larga, opciones de cada script,
reproducibilidad) están en el [manual de ejecución](MANUAL.md).

## Reproducibilidad

Todos los programas generan el grafo con el modelo **Erdős–Rényi**: `n` vértices
y cada arista posible incluida con probabilidad `0.3`. La **semilla se fija en
42** (constante `SEMILLA` en `punto2_exacto.py`, reutilizada por los demás
scripts), de modo que un mismo `n` produce siempre el mismo grafo. Así el
exacto y la heurística se comparan sobre exactamente los mismos casos.

## Método y limitaciones

La fuerza bruta prueba los subconjuntos posibles de vértices, representados con
máscaras de bits, y se queda con el más chico que cubra todas las aristas. Al
revisarlos todos garantiza el óptimo, pero para `n` vértices hay hasta `2^n`
subconjuntos: el tiempo crece exponencialmente y solo es viable para grafos
pequeños. La heurística renuncia a esa garantía a cambio de ser polinomial y
escalar a grafos grandes.
