"""Parte C - Medición con timeit de las operaciones de ListaArreglo.

Para cada tamaño y operación: REPETICIONES mediciones independientes con
timeit.repeat; la cifra que se usa es la MEDIANA (una sola medición es ruido
del sistema operativo). Escribe resultados.csv y las gráficas.

Uso:  python medicion.py
"""
import csv
import statistics
import timeit

from lista_arreglo import ListaArreglo

TAMAÑOS = [1_000, 10_000, 80_000, 200_000]
REPETICIONES = 7


def construir_ordenada(n):
    """Lista con 0, 2, 4, ..., 2(n-1): ordenada y con huecos (impares ausentes)."""
    lista = ListaArreglo()
    for i in range(n):
        lista.insertar(lista.tamaño(), 2 * i)
    return lista


def operaciones(lista, n):
    """Devuelve {nombre: (callable, llamadas_por_medicion)}."""
    ausente = 2 * n + 1          # mayor que todos: peor caso de ambas búsquedas
    medio = 2 * (n // 2)         # presente, hacia la mitad: caso promedio lineal
    posicion_media = n // 2

    def insertar_final():
        # inserta y deshace con eliminar al final (O(1)): evita crecer la lista
        lista.insertar(lista.tamaño(), 1)
        lista.eliminar(lista.tamaño() - 1)

    return {
        # O(1)
        "obtener": (lambda: lista.obtener(posicion_media), 2000),
        "insertar_final": (insertar_final, 2000),
        # O(log n)
        "buscar_binaria": (lambda: lista.buscar_binaria(ausente), 2000),
        # O(n): una llamada por medición (el tamaño crece en 1 por repetición,
        # irrelevante frente a n >= 1.000 y sin disparar redimensionamientos)
        "insertar_inicio": (lambda: lista.insertar(0, -1), 1),
        "insertar_ordenado": (lambda: lista.insertar_ordenado(2 * (n // 2) + 1), 1),
        "buscar_lineal_peor": (lambda: lista.buscar_lineal(ausente), 1),
        "buscar_lineal_medio": (lambda: lista.buscar_lineal(medio), 1),
    }


def main():
    filas = []
    for n in TAMAÑOS:
        lista = construir_ordenada(n)
        holgura = lista._capacidad - lista.tamaño()
        assert holgura > REPETICIONES + 2, "habría redimensionamiento durante la medición"
        for nombre, (fn, numero) in operaciones(lista, n).items():
            tiempos = timeit.repeat(fn, number=numero, repeat=REPETICIONES)
            for r, t in enumerate(tiempos, start=1):
                filas.append((nombre, n, r, t / numero))
            print(f"n={n:>7,} {nombre:<20} mediana={statistics.median(t/numero for t in tiempos)*1e6:12.3f} µs")

    with open("resultados.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["operacion", "n", "repeticion", "segundos_por_llamada"])
        w.writerows(filas)
    print("Escrito resultados.csv")


if __name__ == "__main__":
    main()
