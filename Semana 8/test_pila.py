# Código base — Semana 08
# Fuente: 02-Momento-2-Disciplina-y-jerarquia/08-Semana-08-Pilas/02-guia-de-laboratorio.html

import pytest
from pila import PilaArreglo, PilaEnlazada, PilaVaciaError


@pytest.fixture(params=[PilaArreglo, PilaEnlazada])
def Pila(request):
    return request.param


def test_pila_nueva_vacia(Pila):
    """CA-01: una pila nueva está vacía."""
    p = Pila()
    assert p.esta_vacia()
    assert p.tamaño() == 0


def test_push_pop(Pila):
    """CA-02: push seguido de pop devuelve el mismo elemento."""
    p = Pila()
    p.push("x")
    assert p.pop() == "x"
    assert p.esta_vacia()


def test_orden_lifo(Pila):
    """CA-03: los elementos salen en orden inverso."""
    p = Pila()
    for v in [1, 2, 3]:
        p.push(v)
    assert [p.pop(), p.pop(), p.pop()] == [3, 2, 1]


def test_pop_vacia(Pila):
    """CA-04: pop sobre pila vacía lanza excepción."""
    with pytest.raises(PilaVaciaError):
        Pila().pop()


def test_peek_no_modifica(Pila):
    """CA-05: peek no cambia el tamaño."""
    p = Pila()
    p.push("a")
    assert p.peek() == "a"
    assert p.tamaño() == 1
    assert p.peek() == "a"      # dos veces seguidas: el mismo resultado


def test_peek_vacia(Pila):
    """CA-06: peek sobre pila vacía lanza excepción."""
    with pytest.raises(PilaVaciaError):
        Pila().peek()
