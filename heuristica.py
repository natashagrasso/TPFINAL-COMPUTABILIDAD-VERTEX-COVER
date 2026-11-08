"""Punto 5: recubrimiento de vértices mediante una heurística de máximo grado."""

import argparse
from time import perf_counter

import networkx as nx

from vertex_cover import SEMILLA


def vertex_cover_voraz(grafo: nx.Graph) -> set[int]:
    """Devuelve un cover válido, sin garantizar tamaño mínimo.

    Admite grafos simples no dirigidos sin lazos, con vértices enteros.
    Elige el máximo grado actual; los empates se resuelven por menor
    identificador. Trabaja sobre una copia para conservar el grafo original.
    Tiempo O(n² + m) y memoria adicional O(n + m), para esta implementación.
    """
    if grafo.is_directed() or grafo.is_multigraph():
        raise ValueError("Se requiere un grafo simple no dirigido.")
    if nx.number_of_selfloops(grafo):
        raise ValueError("El grafo no debe contener lazos.")

    pendientes = grafo.copy()
    cover = set()

    while pendientes.number_of_nodes() > 0:
        # Los grados corresponden a las aristas que todavía no cubrimos.
        vertice, grado = max(
            pendientes.degree(), key=lambda par: (par[1], -par[0])
        )
        if grado == 0:
            break  # Solo quedan vértices aislados: todas las aristas se cubrieron.

        cover.add(vertice)
        # Al borrar el vértice también se borran sus aristas incidentes.
        # NetworkX actualiza los grados de los vecinos automáticamente.
        pendientes.remove_node(vertice)

    return cover


def main() -> None:
    """Genera el mismo tipo de grafo que el exacto y mide la heurística."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("n", type=int, help="cantidad de vértices del grafo")
    args = parser.parse_args()
    if args.n < 0:
        parser.error("n debe ser un entero no negativo")

    grafo = nx.erdos_renyi_graph(args.n, 0.3, seed=SEMILLA)
    inicio = perf_counter()
    cover = vertex_cover_voraz(grafo)
    duracion = perf_counter() - inicio

    # La validación queda fuera de la medición.
    valido = all(u in cover or v in cover for u, v in grafo.edges())
    print(f"Vértices del grafo: {grafo.number_of_nodes()}")
    print(f"Aristas del grafo: {grafo.number_of_edges()}")
    print(f"Tamaño del vertex cover heurístico: {len(cover)}")
    print(f"Vértices del vertex cover: {sorted(cover)}")
    print(f"Recubrimiento válido: {'sí' if valido else 'no'}")
    print(f"Tiempo de ejecución: {duracion:.6f} segundos")


if __name__ == "__main__":
    main()
