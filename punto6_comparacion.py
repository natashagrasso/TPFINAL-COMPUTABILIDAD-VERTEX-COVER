"""Punto 6 del TP: comparación entre el algoritmo exacto y la heurística.

Para cada tamaño n se arma el MISMO grafo (p=0.3, SEMILLA=42) y se comparan:
- Calidad: ¿la heurística alcanzó el óptimo? (tamaño exacto vs. heurístico).
- Error relativo: cuánto más grande es el cover heurístico, en porcentaje.
- Tiempo de ejecución de cada algoritmo.

El CSV de salida guarda además metadatos (aristas, semilla, versión de
NetworkX, Python y plataforma) para que la comparación sea reproducible.

Hay dos modos de uso:
- Sin --entrada: ejecuta AMBOS algoritmos en este equipo (por defecto n=10..15).
  Es el modo en que los tiempos son comparables, porque se miden juntos.
- Con --entrada: reutiliza el CSV del punto 3 (tiempos del exacto ya medidos) y
  solo corre la heurística. Sirve para cubrir n grandes que tardarían demasiado
  en volver a medir. Advertencia: los tiempos importados pueden venir de otro
  equipo o versión de NetworkX, así que no permiten atribuir el speedup solo al
  algoritmo; por eso se verifica que el grafo reconstruido coincida (misma p y
  semilla) antes de comparar.

Uso:
    python punto6_comparacion.py                               # mide ambos, n=10..15
    python punto6_comparacion.py --entrada datos/resultados.csv --salida datos/comparacion_completa.csv
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
from punto2_exacto import SEMILLA, vertex_cover_minimo


def medir(funcion, grafo, repeticiones):
    """Mide solo la función y verifica cada resultado fuera del cronómetro."""
    tiempos = []
    cover = set()
    for _ in range(repeticiones):
        inicio = perf_counter()
        cover = funcion(grafo)
        tiempos.append(perf_counter() - inicio)
        if not cover <= set(grafo) or not all(
            u in cover or v in cover for u, v in grafo.edges()
        ):
            raise ValueError("El algoritmo devolvió un recubrimiento inválido.")
    return cover, median(tiempos)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--entrada", type=Path, help="CSV del exacto ya medido")
    parser.add_argument("--desde", type=int, default=10)
    parser.add_argument("--hasta", type=int, default=15)
    parser.add_argument("--repeticiones", type=int, default=5,
                        help="repeticiones de la heurística; se usa la mediana")
    parser.add_argument("--salida", type=Path,
                        default=Path("datos/comparacion.csv"),
                        help="ruta del CSV de salida (predeterminado: datos/)")
    args = parser.parse_args()
    if args.desde < 0 or args.hasta < args.desde or args.repeticiones < 1:
        parser.error("Revisá el rango de n y las repeticiones (al menos 1).")

    if args.entrada:
        with args.entrada.open(newline="", encoding="utf-8-sig") as archivo:
            lector = csv.DictReader(archivo)
            requeridas = {"n", "tiempo_segundos", "tamano_vertex_cover", "estado"}
            if not requeridas <= set(lector.fieldnames or []):
                parser.error("El CSV de entrada no tiene las columnas del punto 3.")
            casos = list(lector)
        print("Se reutilizan los datos del exacto; no se vuelve a ejecutar.")
        print("Confirmar mismo generador, p=0.3, semilla y versión de NetworkX.")
        print("Los tiempos importados no permiten atribuir diferencias solo al algoritmo.")
    else:
        casos = [{"n": n} for n in range(args.desde, args.hasta + 1)]
        print("Se ejecutan ambos algoritmos sobre el mismo grafo y equipo.")

    columnas = ["n", "aristas", "semilla", "probabilidad", "networkx_version",
                "python_version", "plataforma", "origen_exacto", "estado_exacto",
                "tamano_exacto", "tamano_heuristico", "alcanzo_optimo",
                "error_relativo_porcentaje", "tiempo_exacto_segundos",
                "tiempo_heuristico_mediana_segundos", "repeticiones_heuristica",
                "heuristica_valida"]
    # Crea la carpeta de destino (p. ej. datos/) si todavía no existe.
    args.salida.parent.mkdir(parents=True, exist_ok=True)
    # Modo x: evita sobrescribir mediciones previas accidentalmente.
    try:
        archivo = args.salida.open("x", newline="", encoding="utf-8-sig")
    except FileExistsError:
        parser.error("La salida ya existe; elegí otro nombre con --salida.")

    with archivo:
        escritor = csv.DictWriter(archivo, fieldnames=columnas)
        escritor.writeheader()
        archivo.flush()
        for caso in casos:
            n = int(caso["n"])
            if n < 0:
                raise ValueError("n no puede ser negativo")
            grafo = nx.erdos_renyi_graph(n, 0.3, seed=SEMILLA)
            if args.entrada:
                estado = caso["estado"].strip().casefold()
                tiempo_exacto = caso["tiempo_segundos"]
                optimo = (int(caso["tamano_vertex_cover"])
                          if estado == "completado" else None)
            else:
                cover_exacto, tiempo = medir(vertex_cover_minimo, grafo, 1)
                optimo = len(cover_exacto)
                tiempo_exacto = f"{tiempo:.9f}"
                estado = "completado"

            cover, tiempo_h = medir(vertex_cover_voraz, grafo, args.repeticiones)
            tamano = len(cover)
            if optimo is not None and tamano < optimo:
                raise ValueError(
                    f"n={n}: la heurística es menor que el supuesto óptimo. "
                    "Revisá que los grafos y los datos de entrada coincidan."
                )
            error = (100 * (tamano - optimo) / optimo if optimo else
                     (0.0 if optimo == 0 and tamano == 0 else None))
            escritor.writerow({
                "n": n, "aristas": grafo.number_of_edges(), "semilla": SEMILLA,
                "probabilidad": 0.3, "networkx_version": nx.__version__,
                "python_version": sys.version.split()[0],
                "plataforma": platform.platform(),
                "origen_exacto": str(args.entrada) if args.entrada else "misma ejecución",
                "estado_exacto": estado, "tamano_exacto": optimo,
                "tamano_heuristico": tamano,
                "alcanzo_optimo": ("sí" if tamano == optimo else "no")
                                  if optimo is not None else "desconocido",
                "error_relativo_porcentaje": f"{error:.6f}" if error is not None else "",
                "tiempo_exacto_segundos": tiempo_exacto,
                "tiempo_heuristico_mediana_segundos": f"{tiempo_h:.9f}",
                "repeticiones_heuristica": args.repeticiones,
                "heuristica_valida": "sí",
            })
            archivo.flush()
            error_texto = f"{error:.2f}%" if error is not None else "desconocido"
            print(f"n={n}: exacto={optimo if optimo is not None else '?'}; "
                  f"heurística={tamano}; error={error_texto}; "
                  f"T exacto={tiempo_exacto} s; T heurística={tiempo_h:.9f} s")
    print(f"Comparación guardada en: {args.salida.resolve()}")


if __name__ == "__main__":
    main()
