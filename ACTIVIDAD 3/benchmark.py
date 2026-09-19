"""
Mide el costo real de las 4 operaciones de la emisora sobre una lista de
5.000 canciones, en ListaArreglo y ListaEnlazada.

Metodología: por cada operación y cada estructura se repite el experimento
TRIALS veces. En cada repetición se construye una lista NUEVA de N=5000
elementos (sin medir ese tiempo) y se cronometra UNA sola llamada a la
operación objetivo con time.perf_counter(). Se reporta el promedio y la
desviación estándar en microsegundos.
"""
import random
import statistics
import time

from lista_arreglo import ListaArreglo
from lista_enlazada import ListaEnlazada

N = 5000
TRIALS = 300
random.seed(42)


def construir(cls, n=N):
    lista = cls()
    for i in range(n):
        lista.insertar(i, f"cancion_{i}")
    return lista


def medir(func_una_llamada, trials=TRIALS):
    tiempos = []
    for _ in range(trials):
        t = func_una_llamada()
        tiempos.append(t)
    media = statistics.mean(tiempos)
    desv = statistics.stdev(tiempos)
    return media, desv


def op_insertar_al_principio(cls):
    def una():
        lista = construir(cls)
        t0 = time.perf_counter()
        lista.insertar(0, "cancion_urgente")
        return time.perf_counter() - t0
    return una


def op_recorrer_toda(cls):
    def una():
        lista = construir(cls)
        t0 = time.perf_counter()
        for _ in lista:
            pass
        return time.perf_counter() - t0
    return una


def op_ir_a_cancion_n(cls):
    def una():
        lista = construir(cls)
        i = random.randint(0, N - 1)
        t0 = time.perf_counter()
        lista.obtener(i)
        return time.perf_counter() - t0
    return una


def op_borrar_actual(cls):
    def una():
        lista = construir(cls)
        i = random.randint(0, N - 1)
        t0 = time.perf_counter()
        lista.eliminar(i)
        return time.perf_counter() - t0
    return una


OPERACIONES = {
    "insertar_al_principio": op_insertar_al_principio,
    "recorrer_toda_la_lista": op_recorrer_toda,
    "ir_a_cancion_n": op_ir_a_cancion_n,
    "borrar_actual": op_borrar_actual,
}

ESTRUCTURAS = {
    "ListaArreglo": ListaArreglo,
    "ListaEnlazada": ListaEnlazada,
}

if __name__ == "__main__":
    resultados = {}
    print(f"N = {N} canciones, {TRIALS} repeticiones por medición\n")
    print(f"{'Operación':<24}{'Estructura':<16}{'Media (µs)':>14}{'Desv (µs)':>14}")
    print("-" * 68)
    for nombre_op, fabrica in OPERACIONES.items():
        resultados[nombre_op] = {}
        for nombre_est, cls in ESTRUCTURAS.items():
            media, desv = medir(fabrica(cls))
            resultados[nombre_op][nombre_est] = media
            print(f"{nombre_op:<24}{nombre_est:<16}{media*1e6:>14.2f}{desv*1e6:>14.2f}")

    print("\nRESULTADOS_PYTHON =", resultados)
