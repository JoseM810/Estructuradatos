from arbol_carpetas import *


def test_arbol_vacio():
    assert contar_entregas(None) == 0
    assert profundidad_maxima(None) == 0
    assert ruta_mas_profunda(None) == []
    assert listar_por_niveles(None) == []


def test_un_solo_nodo():
    n = Carpeta("solo", 4)
    assert contar_entregas(n) == 4
    assert profundidad_maxima(n) == 1
    assert ruta_mas_profunda(n) == ["solo"]
    assert listar_por_niveles(n) == [["solo"]]


def test_arbol_de_prueba():
    t = arbol_de_prueba()
    assert contar_entregas(t) == 61
    assert contar_entregas(t.hijos[1]) == 7  # solo Derecho
    assert profundidad_maxima(t) == 6
    assert ruta_mas_profunda(t) == [
        "Servidor", "Ingenieria", "Sistemas", "EstructurasDatos", "2026-2", "ProyectoFinal"]
    assert listar_por_niveles(t) == [
        ["Servidor"],
        ["Ingenieria", "Derecho"],
        ["Sistemas", "Civil", "DerechoPenal1"],
        ["EstructurasDatos", "BasesDatos", "Estatica", "2026-2D"],
        ["2026-1", "2026-2", "2026-1B", "2025-2"],
        ["ProyectoFinal"],
    ]


def test_pila_difiere_de_cola():
    t = arbol_de_prueba()
    plano = [n for nivel in listar_por_niveles(t) for n in nivel]
    assert listar_con_pila(t) != plano
    assert sorted(listar_con_pila(t)) == sorted(plano)
