"""Tus pruebas: mínimo 2 por función, sobre casos que el contrato NO cubre
(un solo elemento, todos iguales, árbol degenerado, k negativo, ...).
Cada prueba lleva un comentario de una línea: qué caso cubre y por qué importa.
"""
from estructuras import ListaDoble, ABB
from solucion import quitar_repetidos, posicion_en_ranking

# ---------- quitar_repetidos ----------

def test_un_solo_elemento():
    # Un nodo es cabeza y cola a la vez: no debe eliminarse ni romperse nada.
    lista = ListaDoble([9])
    assert quitar_repetidos(lista) == 0
    assert list(lista) == [9]
    assert lista.cabeza is lista.cola

def test_todos_iguales():
    # Se eliminan n-1 nodos y debe quedar uno solo con cabeza y cola bien enlazadas.
    lista = ListaDoble([4, 4, 4, 4])
    assert quitar_repetidos(lista) == 3
    assert list(lista) == [4]
    assert len(lista) == 1
    assert lista.cabeza is lista.cola
    assert lista.cabeza.anterior is None and lista.cabeza.siguiente is None

def test_sin_repetidos_no_cambia():
    # Si no hay repetidos, la lista queda idéntica y se devuelve 0.
    lista = ListaDoble([1, 2, 3])
    assert quitar_repetidos(lista) == 0
    assert list(lista) == [1, 2, 3]

def test_repetido_en_la_cabeza_actualiza_cabeza():
    # Eliminar el primer nodo exige mover 'cabeza'; es el error clásico de punteros.
    lista = ListaDoble([1, 2, 1])
    assert quitar_repetidos(lista) == 1
    assert list(lista) == [2, 1]
    assert lista.cabeza.dato == 2
    assert lista.cabeza.anterior is None


# ---------- posicion_en_ranking ----------

def test_ranking_arbol_vacio():
    # Árbol sin raíz: no hay ningún puesto, debe devolver None sin fallar.
    assert posicion_en_ranking(ABB(), 1) is None

def test_ranking_k_negativo():
    # k negativo no es un puesto válido; no debe confundirse con indexar desde el final.
    assert posicion_en_ranking(ABB([5, 3, 8]), -1) is None

def test_ranking_arbol_degenerado():
    # Árbol en forma de lista (insertado en orden): el peor caso de altura debe funcionar.
    arbol = ABB(range(1, 2001))
    assert posicion_en_ranking(arbol, 1) == 2000
    assert posicion_en_ranking(arbol, 2000) == 1

def test_ranking_un_solo_nodo():
    # Con un único puntaje, el puesto 1 es ese nodo y el 2 no existe.
    arbol = ABB([42])
    assert posicion_en_ranking(arbol, 1) == 42
    assert posicion_en_ranking(arbol, 2) is None

def test_ranking_ultimo_puesto():
    # k = n debe devolver el mínimo, que obliga a recorrer todo el árbol.
    assert posicion_en_ranking(ABB([50, 30, 70, 20, 40, 60, 80]), 7) == 20