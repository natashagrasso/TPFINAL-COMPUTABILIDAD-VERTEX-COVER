"""Resuelve Minimum Vertex Cover mediante fuerza bruta."""

import argparse
from time import perf_counter

import networkx as nx


def vertex_cover_minimo(grafo: nx.Graph) -> set[int]:
    """Devuelve un vertex cover de tamaño mínimo probando subconjuntos."""
    vertices = list(grafo.nodes())
    posicion = {vertice: indice for indice, vertice in enumerate(vertices)}
    aristas = [
        (posicion[origen], posicion[destino])
        for origen, destino in grafo.edges()
    ]

    mejor_mascara = (1 << len(vertices)) - 1
    mejor_tamano = len(vertices)

    # Recorre las 2^n combinaciones posibles.
    for mascara in range(1 << len(vertices)):
        tamano = mascara.bit_count()
        if tamano >= mejor_tamano:
            continue

        # Comprueba que cada arista tenga un extremo seleccionado
        if all(
            (mascara & (1 << origen)) or (mascara & (1 << destino))
            for origen, destino in aristas
        ):
            mejor_mascara = mascara
            mejor_tamano = tamano

    return {
        vertice
        for indice, vertice in enumerate(vertices)
        if mejor_mascara & (1 << indice)
    }


def main() -> None:
    """Lee el tamaño del grafo, lo genera y muestra el resultado."""
    parser = argparse.ArgumentParser(
        description="Encuentra un vertex cover mínimo con fuerza bruta."
    )
    parser.add_argument(
        "n",
        type=int,
        help="cantidad de vértices del grafo aleatorio",
    )
    args = parser.parse_args()

    if args.n < 0:
        parser.error("n debe ser un entero no negativo")

    # se fija la semilla para repetir el mismo grafo en cada prueba.
    grafo = nx.erdos_renyi_graph(args.n, 0.3, seed=42)

    inicio = perf_counter()
    cover = vertex_cover_minimo(grafo)
    duracion = perf_counter() - inicio

    print(f"Tamaño del vertex cover mínimo: {len(cover)}")
    print(f"Vértices del vertex cover: {sorted(cover)}")
    print(f"Tiempo de ejecución: {duracion:.6f} segundos")


if __name__ == "__main__":
    main()


# Ejemplos de uso desde la terminal:
#   python vertex_cover.py 10
#   python vertex_cover.py 12
#   python vertex_cover.py 15
