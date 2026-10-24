"""Prueba individual · Estructuras de Datos · Parte II

Nombre: Jose Miguel Alvarez  Documento: 1092734488

Metodología del curso (SDD): la especificación manda. El contrato exacto de
cada función está en test_contrato.py. Léelo ANTES de programar: lo que no
diga el enunciado, lo dicen esas pruebas.

Reglas: recorre los nodos (cabeza, cola, siguiente, anterior, raiz, izquierdo,
derecho). No conviertas la estructura completa a una lista de Python.
Escribe en un comentario la complejidad Big-O de cada función y por qué.
"""
from estructuras import ListaDoble, ABB

# Big-O: O(n) tiempo y O(n) espacio.
# Recorro la lista una sola vez, de la cola a la cabeza. Uso un set para saber
# si un dato ya apareció (consultar y agregar cuesta O(1)) y, si ya estaba,
# elimino el nodo con eliminar_nodo, que también es O(1). Voy desde la cola
# para conservar la última aparición. El set guarda hasta n datos, de ahí el
# O(n) de espacio.
def quitar_repetidos(lista: ListaDoble) -> int:
    """Quita los datos repetidos: al terminar, cada dato aparece una sola vez en la lista.
    Devuelve cuántos nodos se eliminaron.
    """
    vistos = set()
    eliminados = 0
    actual = lista.cola
    while actual is not None:
        anterior = actual.anterior  # guardarlo ANTES de eliminar el nodo actual
        if actual.dato in vistos:
            lista.eliminar_nodo(actual)  # aparición más antigua: se descarta
            eliminados += 1
        else:
            vistos.add(actual.dato)  # primera vez que lo veo desde la cola: se conserva
        actual = anterior
    return eliminados
 
 
# Big-O: O(h + k) tiempo y O(h) espacio (h = altura, k = puesto).
# Bajo hasta el mayor por la derecha (h pasos) y recorro en orden descendente
# (derecho, nodo, izquierdo) hasta llegar al k-ésimo, sin pasar de ahí.
# La pila guarda como máximo un camino de la raíz a una hoja. En el peor caso,
# con un árbol degenerado, h = n y el costo es O(n).
def posicion_en_ranking(arbol: ABB, k: int):
    """El árbol guarda los puntajes de una competencia.
    Devuelve el puntaje que ocupa el puesto k del ranking.
    """
    if k < 1 or k > len(arbol):  # puesto inexistente: 0, negativo o mayor que n
        return None
    pila = []
    actual = arbol.raiz
    contador = 0
    while pila or actual is not None:
        while actual is not None:  # bajar por la derecha: primero los mayores
            pila.append(actual)
            actual = actual.derecho
        actual = pila.pop()
        contador += 1
        if contador == k:  # este es el k-ésimo mayor
            return actual.dato
        actual = actual.izquierdo  # después, el subárbol de los menores
    return None
