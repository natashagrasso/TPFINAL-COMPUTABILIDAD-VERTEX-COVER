"""Mide el algoritmo exacto para tamaños de entrada crecientes."""

import argparse
import csv
import json
import subprocess
import sys
from itertools import count
from pathlib import Path


def medir_ejecucion(n: int, limite_segundos: float) -> tuple[str, str, str]:
    """Ejecuta un caso aislado y devuelve tiempo, tamaño de solución y estado."""
    codigo = (
        "import json, sys, time; "
        "import networkx as nx; "
        "from vertex_cover import SEMILLA, vertex_cover_minimo; "
        "n = int(sys.argv[1]); "
        "grafo = nx.erdos_renyi_graph(n, 0.3, seed=SEMILLA); "
        "inicio = time.perf_counter(); "
        "print('INICIO_ALGORITMO', flush=True); "
        "cover = vertex_cover_minimo(grafo); "
        "print(json.dumps({'tiempo': time.perf_counter() - inicio, "
        "'tamano': len(cover)}))"
    )
    proyecto = Path(__file__).resolve().parent

    proceso = subprocess.Popen(
        [sys.executable, "-c", codigo, str(n)],
        cwd=proyecto,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )
    if proceso.stdout is None or proceso.stderr is None:
        proceso.kill()
        raise RuntimeError("No se pudieron capturar las salidas del proceso.")

    marca_inicio = proceso.stdout.readline()
    if marca_inicio.strip() != "INICIO_ALGORITMO":
        _, error = proceso.communicate()
        detalle = error.strip() or "el proceso terminó antes de iniciar el algoritmo"
        raise RuntimeError(
            f"Falló la ejecución para n={n}: {detalle}"
        )

    try:
        salida, error = proceso.communicate(timeout=limite_segundos)
    except subprocess.TimeoutExpired:
        proceso.kill()
        proceso.communicate()
        return f">{limite_segundos:g}", "", "supero el limite de tiempo"

    if proceso.returncode != 0:
        detalle = error.strip() or "sin detalle de error"
        raise RuntimeError(f"Falló la ejecución para n={n}: {detalle}")

    resultado = json.loads(salida)
    tiempo = float(resultado["tiempo"])
    tamano = int(resultado["tamano"])
    if tiempo >= limite_segundos:
        return f">{limite_segundos:g}", str(tamano), "superó el límite de tiempo"
    return f"{tiempo:.6f}", str(tamano), "completado"


def main() -> None:
    """Registra tiempos para n crecientes hasta superar el límite."""
    parser = argparse.ArgumentParser(
        description="Registra tiempos del algoritmo exacto en un archivo CSV."
    )
    parser.add_argument(
        "--desde",
        type=int,
        default=10,
        help="primer tamaño de entrada (predeterminado: 10)",
    )
    parser.add_argument(
        "--hasta",
        type=int,
        help="límite opcional de n para una prueba acotada",
    )
    parser.add_argument(
        "--limite-segundos",
        type=float,
        default=3600,
        help="tiempo máximo por caso (predeterminado: 3600 segundos)",
    )
    parser.add_argument(
        "--salida",
        type=Path,
        default=Path("resultados_experimento.csv"),
        help="ruta del CSV de resultados",
    )
    args = parser.parse_args()

    if args.desde < 0:
        parser.error("--desde debe ser un entero no negativo")
    if args.hasta is not None and args.hasta < args.desde:
        parser.error("--hasta debe ser mayor o igual que --desde")
    if args.limite_segundos <= 0:
        parser.error("--limite-segundos debe ser mayor que cero")

    salida = args.salida.resolve()
    if salida.exists():
        parser.error(
            f"el archivo {salida} ya existe; elegí otra ruta con --salida"
        )

    with salida.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(("n", "tiempo_segundos", "tamano_vertex_cover", "estado"))
        archivo.flush()

        for n in count(args.desde):
            tiempo, tamano, estado = medir_ejecucion(n, args.limite_segundos)
            escritor.writerow((n, tiempo, tamano, estado))
            archivo.flush()
            print(
                f"n={n}: tiempo={tiempo} s, tamaño del cover={tamano or 'no alcanzado'}, "
                f"estado={estado}"
            )

            if estado != "completado":
                break
            if args.hasta is not None and n >= args.hasta:
                break

    print(f"Resultados guardados en: {salida}")


if __name__ == "__main__":
    main()
