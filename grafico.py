"""Grafica los tiempos del algoritmo exacto a partir de un archivo CSV."""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


LIMITE_SEGUNDOS = 3600
COLUMNAS_REQUERIDAS = {
    "n",
    "tiempo_segundos",
    "tamano_vertex_cover",
    "estado",
}


def cargar_resultados(entrada: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Separa filas completadas y no completadas sin convertir texto invalido."""
    datos = pd.read_csv(entrada, dtype={"estado": "string"})
    faltantes = COLUMNAS_REQUERIDAS - set(datos.columns)
    if faltantes:
        raise ValueError(
            "Faltan columnas requeridas en el CSV: "
            + ", ".join(sorted(faltantes))
        )

    datos["estado"] = datos["estado"].str.strip().str.casefold()
    completados = datos.loc[datos["estado"] == "completado"].copy()
    no_completados = datos.loc[datos["estado"] != "completado"].copy()

    # Convierto solo las filas completadas y reporto datos numericos invalidos.
    for columna in ("n", "tiempo_segundos"):
        valores = pd.to_numeric(completados[columna], errors="coerce")
        if valores.isna().any():
            filas = (valores.index + 2).tolist()
            raise ValueError(
                f"Valores invalidos en '{columna}' en las filas: {filas}"
            )
        completados[columna] = valores

    if completados.empty:
        raise ValueError("El CSV no contiene filas con estado 'completado'.")

    # Para ubicar una fila incompleta solo necesito su tamano n.
    no_completados["n"] = pd.to_numeric(
        no_completados["n"], errors="coerce"
    )
    if no_completados["n"].isna().any():
        filas = (no_completados.index[no_completados["n"].isna()] + 2).tolist()
        raise ValueError(f"Valor de n invalido en filas no completadas: {filas}")

    completados = completados.sort_values("n")
    no_completados = no_completados.sort_values("n")
    return completados, no_completados


def imprimir_tabla(completados: pd.DataFrame) -> None:
    """Imprime tiempos y cocientes con el caso anterior n-1."""
    tiempos = completados.set_index("n")["tiempo_segundos"]
    filas = []
    for fila in completados.itertuples(index=False):
        anterior = tiempos.get(fila.n - 1)
        cociente = (
            fila.tiempo_segundos / anterior
            if anterior is not None and anterior > 0
            else float("nan")
        )
        filas.append(
            {
                "n": int(fila.n),
                "tiempo_segundos": fila.tiempo_segundos,
                "tiempo(n)/tiempo(n-1)": cociente,
            }
        )

    tabla = pd.DataFrame(filas)
    print(tabla.to_string(index=False, float_format=lambda valor: f"{valor:.6f}"))


def crear_grafico(
    completados: pd.DataFrame,
    no_completados: pd.DataFrame,
    salida: Path,
    escala_log: bool,
) -> None:
    """Guarda el grafico lineal o logaritmico con limite y casos incompletos."""
    figura, eje = plt.subplots(figsize=(10, 6))
    tiempos = completados["tiempo_segundos"]
    tamaños = completados["n"]

    eje.plot(tamaños, tiempos, marker="o", label="Tiempo medido")
    eje.axhline(
        LIMITE_SEGUNDOS,
        color="gray",
        linestyle=":",
        label="Limite: 1 hora",
    )

    if escala_log:
        ultimo_n = int(completados.iloc[-1]["n"])
        ultimo_tiempo = float(completados.iloc[-1]["tiempo_segundos"])
        constante = ultimo_tiempo / (2**ultimo_n)
        teoricos = [constante * (2**int(n)) for n in tamaños]
        eje.plot(
            tamaños,
            teoricos,
            linestyle="--",
            label="Teorico O(2^n)",
        )
        eje.set_yscale("log")

    # Marco los casos que no terminaron en el limite de una hora.
    for indice, fila in enumerate(no_completados.itertuples(index=False)):
        etiqueta = "Supero 1 hora" if indice == 0 else "_nolegend_"
        eje.scatter(
            fila.n,
            LIMITE_SEGUNDOS,
            color="red",
            marker="x",
            s=90,
            label=etiqueta,
            zorder=5,
        )

    eje.set_xlabel("Tamano de entrada n (vertices)")
    eje.set_ylabel("Tiempo de ejecucion (segundos)")
    titulo_escala = "logaritmica" if escala_log else "lineal"
    eje.set_title(
        f"Tiempo del algoritmo exacto de Vertex Cover ({titulo_escala})"
    )
    eje.grid(True, which="both", linestyle=":", alpha=0.7)
    eje.legend()
    figura.tight_layout()
    figura.savefig(salida, dpi=150)
    plt.close(figura)


def main() -> None:
    """Lee las opciones, muestra la tabla y genera los dos graficos."""
    parser = argparse.ArgumentParser(
        description="Grafica los resultados del algoritmo exacto de Vertex Cover."
    )
    parser.add_argument(
        "--entrada",
        type=Path,
        default=Path("resultados.csv"),
        help="CSV de resultados (predeterminado: resultados.csv)",
    )
    args = parser.parse_args()

    if not args.entrada.is_file():
        parser.error(f"no se encontro el archivo de entrada: {args.entrada}")

    try:
        completados, no_completados = cargar_resultados(args.entrada)
    except (OSError, pd.errors.ParserError, ValueError) as error:
        parser.error(str(error))

    imprimir_tabla(completados)
    crear_grafico(
        completados,
        no_completados,
        Path("grafico_tiempo_lineal.png"),
        escala_log=False,
    )
    crear_grafico(
        completados,
        no_completados,
        Path("grafico_tiempo_log.png"),
        escala_log=True,
    )
    print("Graficos guardados en grafico_tiempo_lineal.png y grafico_tiempo_log.png")


if __name__ == "__main__":
    main()
