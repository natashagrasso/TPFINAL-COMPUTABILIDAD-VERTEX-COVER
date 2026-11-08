"""Punto 2 del TP: algoritmo exacto para el Recubrimiento Mínimo de Vértices.

Un *recubrimiento de vértices* (vertex cover) de un grafo es un conjunto de
vértices tal que toda arista tiene al menos uno de sus extremos en el conjunto.
Hallar el recubrimiento de menor tamaño es un problema NP-difícil: no se conoce
un algoritmo eficiente (polinomial) que lo resuelva de forma exacta.

Este programa lo resuelve por FUERZA BRUTA: prueba todos los subconjuntos de
vértices posibles y se queda con el más chico que sea un recubrimiento válido.
Cada subconjunto se representa con una MÁSCARA DE BITS, es decir un número
entero en el que el bit de la posición "i" vale 1 si el vértice "i" está en el
subconjunto. Recorrer los enteros de "0" a "2^n - 1" equivale entonces a
recorrer los "2^n" subconjuntos posibles de "n" vértices. Por ese costo
exponencial, el método solo es práctico para grafos pequeños.

La constante SEMILLA se define acá y la reutilizan los demás scripts del trabajo
(heurística, experimentación, comparación y escalabilidad) para generar siempre
el mismo grafo con cada valor de n, de modo que los resultados sean comparables.

Uso:
    python punto2_exacto.py 10
"""

import argparse
from time import perf_counter

import networkx as nx

# Semilla fija del generador de grafos. Reutilizada por el resto de los scripts
# para que un mismo n produzca siempre el mismo grafo (resultados reproducibles).
SEMILLA = 42


def vertex_cover_minimo(grafo: nx.Graph) -> set[int]:
    """Devuelve un recubrimiento de vértices de tamaño mínimo.

    Prueba exhaustivamente los "2^n" subconjuntos de vértices (uno por cada
    máscara de bits) y conserva el más pequeño que cubra todas las aristas. Al
    revisar todas las posibilidades, garantiza hallar el óptimo.

    :param grafo: grafo no dirigido de NetworkX.
    :return: conjunto con los vértices del recubrimiento mínimo.
    """
    # Lista de vértices del grafo (sus nombres/identificadores).
    vertices = list(grafo.nodes())

    # A cada vértice se le asigna una posición de bit: 0, 1, 2, ... Esa
    # posición es el bit que lo representa dentro de la máscara.
    posicion = {vertice: indice for indice, vertice in enumerate(vertices)}

    # Se reexpresan las aristas usando esas posiciones de bit, para poder
    # operar con máscaras directamente en lugar de con los nombres de vértice.
    aristas = [
        (posicion[origen], posicion[destino])
        for origen, destino in grafo.edges()
    ]

    # Candidato inicial: todos los vértices seleccionados. Es siempre un
    # recubrimiento válido (toca todas las aristas), aunque el más grande.
    # (1 << n) es 2^n; restarle 1 deja un número con los n bits en 1.
    mejor_mascara = (1 << len(vertices)) - 1
    mejor_tamano = len(vertices)

    # Cada entero entre 0 y 2^n - 1 es una máscara, es decir un subconjunto.
    for mascara in range(1 << len(vertices)):
        # Cantidad de bits en 1 = cantidad de vértices del subconjunto.
        tamano = mascara.bit_count()

        # Poda: si este subconjunto no es más chico que el mejor hallado, no
        # puede mejorar el resultado, así que se evita el chequeo de aristas.
        if tamano >= mejor_tamano:
            continue

        # Un subconjunto es un recubrimiento válido si toda arista tiene al
        # menos un extremo seleccionado. (mascara & (1 << pos)) es distinto de
        # cero cuando el vértice de esa posición está en el subconjunto.
        if all(
            (mascara & (1 << origen)) or (mascara & (1 << destino))
            for origen, destino in aristas
        ):
            mejor_mascara = mascara
            mejor_tamano = tamano

    # Se traduce la máscara ganadora de vuelta a los nombres de los vértices.
    return {
        vertice
        for indice, vertice in enumerate(vertices)
        if mejor_mascara & (1 << indice)
    }


def main() -> None:
    """Lee el tamaño del grafo, lo genera y muestra el resultado por pantalla."""
    # Configuración del argumento de línea de comandos: la cantidad de vértices.
    parser = argparse.ArgumentParser(
        description="Encuentra un vertex cover mínimo con fuerza bruta."
    )
    parser.add_argument(
        "n",
        type=int,
        help="cantidad de vértices del grafo aleatorio",
    )
    args = parser.parse_args()

    # Validación: un grafo no puede tener una cantidad negativa de vértices.
    if args.n < 0:
        parser.error("n debe ser un entero no negativo")

    # Grafo aleatorio no dirigido (modelo Erdős–Rényi): n vértices y cada
    # arista posible incluida con probabilidad 0.3. La semilla fija hace el
    # grafo reproducible: mismo n => mismo grafo => mismo resultado.
    grafo = nx.erdos_renyi_graph(args.n, 0.3, seed=SEMILLA)

    # Se cronometra solo la búsqueda, no la generación del grafo.
    inicio = perf_counter()
    cover = vertex_cover_minimo(grafo)
    duracion = perf_counter() - inicio

    print(f"Tamaño del vertex cover mínimo: {len(cover)}")
    print(f"Vértices del vertex cover: {sorted(cover)}")
    print(f"Tiempo de ejecución: {duracion:.6f} segundos")


if __name__ == "__main__":
    main()


# Ejemplos de uso desde la terminal:
#   python punto2_exacto.py 10
#   python punto2_exacto.py 12
#   python punto2_exacto.py 15
