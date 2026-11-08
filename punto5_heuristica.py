"""Punto 5 del TP: heurística para el recubrimiento de vértices.

Una HEURÍSTICA es un algoritmo rápido que da una solución buena, pero sin
garantizar que sea la óptima. A diferencia de la fuerza bruta (punto2_exacto.py),
que prueba los 2^n subconjuntos y es exponencial, esta heurística es polinomial
y por eso escala a grafos grandes.

La heurística implementada es la VORAZ DE MÁXIMO GRADO (greedy / highest-degree):
en cada paso elige el vértice que toca más aristas sin cubrir, lo agrega al
recubrimiento y lo quita del grafo (con lo que esas aristas quedan cubiertas).
Repite hasta que no quedan aristas. La intuición es que el vértice más conectado
"tapa" muchas aristas de una sola vez.
"""

import argparse
from time import perf_counter

import networkx as nx

from punto2_exacto import SEMILLA


def vertex_cover_voraz(grafo: nx.Graph) -> set[int]:
    """Devuelve un recubrimiento de vértices válido por la estrategia voraz.

    No garantiza el tamaño mínimo: puede dar un cover un poco más grande que el
    óptimo, a cambio de ser mucho más rápido que la fuerza bruta.

    Detalles de esta implementación:
    - Admite solo grafos simples no dirigidos y sin lazos.
    - En cada paso elige el vértice de mayor grado actual; los empates se
      resuelven por el menor identificador, para que el resultado sea
      determinista (siempre el mismo) y comparable con el exacto (punto 6).
    - Trabaja sobre una COPIA del grafo para no destruir el original.
    - Complejidad: tiempo O(n² + m) y memoria adicional O(n + m).

    :param grafo: grafo simple no dirigido de NetworkX, sin lazos.
    :return: conjunto de vértices que forman el recubrimiento.
    """
    # Validaciones: la heurística asume un grafo simple no dirigido sin lazos.
    if grafo.is_directed() or grafo.is_multigraph():
        raise ValueError("Se requiere un grafo simple no dirigido.")
    if nx.number_of_selfloops(grafo):
        raise ValueError("El grafo no debe contener lazos.")

    # Copia de trabajo: el algoritmo irá BORRANDO vértices de 'pendientes', así
    # que se usa una copia para dejar intacto el grafo que recibió la función.
    pendientes = grafo.copy()
    cover = set()  # Vértices elegidos; arranca vacío.

    # Se repite mientras queden vértices en la copia. En cada vuelta se elige y
    # se elimina un vértice, de modo que el bucle siempre avanza y termina.
    while pendientes.number_of_nodes() > 0:
        # pendientes.degree() da pares (vertice, grado). Como las aristas ya
        # cubiertas fueron borradas, el grado = cantidad de aristas que ese
        # vértice todavía no cubre. max() elige el de mayor grado; ante empate,
        # el '-par[0]' hace ganar al de menor identificador (desempate estable).
        vertice, grado = max(
            pendientes.degree(), key=lambda par: (par[1], -par[0])
        )

        # Si el mayor grado es 0, no queda ninguna arista por cubrir: lo que
        # resta son vértices aislados, que no hace falta agregar al cover.
        if grado == 0:
            break

        # Se agrega el vértice elegido y se lo borra de la copia. Al borrarlo,
        # NetworkX elimina también sus aristas incidentes (que quedan cubiertas)
        # y recalcula los grados de los vecinos para la vuelta siguiente.
        cover.add(vertice)
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
