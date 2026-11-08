"""Punto 7 del TP: escalabilidad de la heurística.

Ejecuta la heurística voraz (punto5_heuristica.py) sobre grafos grandes (n >= 1000),
tamaños que el algoritmo exacto nunca podría resolver, y mide su tiempo de
ejecución para analizar cómo escala y si es viable para casos reales.

Para cada tamaño n:
- Se genera el grafo Erdős–Rényi (misma probabilidad y semilla que el resto del
  trabajo, por defecto p=0.3 y SEMILLA=42) para mantener la configuración.
- Se mide solo la heurística (no la generación del grafo), repitiéndola varias
  veces y quedándose con la mediana, que es robusta frente a variaciones.
- Se registran n, cantidad de aristas, tamaño del cover y tiempo mediano.

Los resultados se guardan en un CSV dentro de datos/ y, si matplotlib está
instalado, se genera además un gráfico de tiempo vs. n en graficos/.

Advertencia: con p=0.3 la cantidad de aristas crece como ~n²/2, así que los
grafos grandes consumen mucha memoria y tiempo de GENERACIÓN. Conviene subir n
de a poco y vigilar el uso de RAM.

Uso:
    python punto7_escalabilidad.py
    python punto7_escalabilidad.py --tamanos 1000 2000 5000 --repeticiones 3
"""

import argparse
import csv
import platform
import sys
from pathlib import Path
from statistics import median
from time import perf_counter

import networkx as nx

from punto5_heuristica import vertex_cover_voraz
from punto2_exacto import SEMILLA

# Carpetas de salida, coherentes con el resto del proyecto.
CARPETA_DATOS = Path("datos")
CARPETA_GRAFICOS = Path("graficos")


def medir_heuristica(grafo: nx.Graph, repeticiones: int) -> tuple[int, float]:
    """Corre la heurística varias veces y devuelve (tamaño del cover, mediana).

    La validez del resultado se comprueba FUERA del cronómetro para no
    contaminar la medición de tiempo.

    :param grafo: grafo sobre el que se mide.
    :param repeticiones: cantidad de corridas; se reporta la mediana de tiempos.
    :return: tamaño del recubrimiento y tiempo mediano en segundos.
    """
    tiempos = []
    cover: set[int] = set()
    for _ in range(repeticiones):
        inicio = perf_counter()
        cover = vertex_cover_voraz(grafo)
        tiempos.append(perf_counter() - inicio)

    # Verificación de correctitud (no se cronometra): el cover debe tocar
    # todas las aristas del grafo.
    if not all(u in cover or v in cover for u, v in grafo.edges()):
        raise ValueError("La heurística devolvió un recubrimiento inválido.")

    return len(cover), median(tiempos)


def graficar(filas: list[dict], salida: Path) -> None:
    """Dibuja el tiempo de la heurística en función de n.

    matplotlib se importa acá adentro para que la MEDICIÓN funcione aunque la
    librería no esté instalada; solo el gráfico la necesita.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib no está instalado: se omite el gráfico "
              "(instalalo con 'pip install -r requirements.txt').")
        return

    tamanos = [fila["n"] for fila in filas]
    tiempos = [fila["tiempo_mediana_segundos"] for fila in filas]

    figura, eje = plt.subplots(figsize=(10, 6))
    eje.plot(tamanos, tiempos, marker="o", label="Heurística (mediana)")
    eje.set_xlabel("Tamano de entrada n (vertices)")
    eje.set_ylabel("Tiempo de ejecucion (segundos)")
    eje.set_title("Escalabilidad de la heuristica de Vertex Cover")
    eje.grid(True, linestyle=":", alpha=0.7)
    eje.legend()
    figura.tight_layout()

    CARPETA_GRAFICOS.mkdir(parents=True, exist_ok=True)
    figura.savefig(salida, dpi=150)
    plt.close(figura)
    print(f"Grafico guardado en {salida}")


def main() -> None:
    """Mide la heurística para cada tamaño, guarda el CSV y genera el gráfico."""
    parser = argparse.ArgumentParser(description="Escalabilidad de la heurística.")
    parser.add_argument(
        "--tamanos",
        type=int,
        nargs="+",
        default=[1000, 2000, 3000, 4000, 5000],
        help="tamaños de n a medir (predeterminado: 1000 2000 3000 4000 5000)",
    )
    parser.add_argument(
        "--repeticiones",
        type=int,
        default=3,
        help="repeticiones por tamaño; se reporta la mediana (predeterminado: 3)",
    )
    parser.add_argument(
        "--probabilidad",
        type=float,
        default=0.3,
        help="probabilidad de arista del grafo (predeterminado: 0.3)",
    )
    parser.add_argument(
        "--salida",
        type=Path,
        default=CARPETA_DATOS / "escalabilidad.csv",
        help="ruta del CSV de resultados (predeterminado: datos/escalabilidad.csv)",
    )
    args = parser.parse_args()

    if args.repeticiones < 1:
        parser.error("--repeticiones debe ser al menos 1")
    if any(n < 0 for n in args.tamanos):
        parser.error("los tamaños de n no pueden ser negativos")
    if not 0 <= args.probabilidad <= 1:
        parser.error("--probabilidad debe estar entre 0 y 1")

    # Crea la carpeta de destino y evita sobrescribir mediciones previas.
    args.salida.parent.mkdir(parents=True, exist_ok=True)
    if args.salida.exists():
        parser.error(
            f"el archivo {args.salida} ya existe; elegí otra ruta con --salida"
        )

    columnas = [
        "n", "aristas", "semilla", "probabilidad", "tamano_cover",
        "tiempo_mediana_segundos", "repeticiones", "networkx_version",
        "python_version", "plataforma",
    ]
    filas: list[dict] = []

    with args.salida.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=columnas)
        escritor.writeheader()
        archivo.flush()

        for n in sorted(args.tamanos):
            # La generación del grafo queda fuera de la medición de la heurística.
            grafo = nx.erdos_renyi_graph(n, args.probabilidad, seed=SEMILLA)
            tamano, tiempo = medir_heuristica(grafo, args.repeticiones)

            fila = {
                "n": n,
                "aristas": grafo.number_of_edges(),
                "semilla": SEMILLA,
                "probabilidad": args.probabilidad,
                "tamano_cover": tamano,
                "tiempo_mediana_segundos": tiempo,
                "repeticiones": args.repeticiones,
                "networkx_version": nx.__version__,
                "python_version": sys.version.split()[0],
                "plataforma": platform.platform(),
            }
            # El CSV se actualiza después de cada tamaño: si se interrumpe la
            # corrida, lo ya medido queda guardado.
            escritor.writerow({**fila, "tiempo_mediana_segundos": f"{tiempo:.6f}"})
            archivo.flush()
            filas.append(fila)

            print(f"n={n}: aristas={grafo.number_of_edges()}; "
                  f"cover={tamano}; tiempo={tiempo:.6f} s")

    print(f"Resultados guardados en: {args.salida.resolve()}")
    graficar(filas, CARPETA_GRAFICOS / "escalabilidad_tiempo.png")


if __name__ == "__main__":
    main()
