# Código base — Semana 08
# Fuente: 02-Momento-2-Disciplina-y-jerarquia/08-Semana-08-Pilas/02-guia-de-laboratorio.html

from pila import PilaEnlazada, PilaVaciaError


class Historial:
    """Sistema de deshacer y rehacer con dos pilas.

    La regla que casi todos olvidan: cuando llega una acción NUEVA,
    la pila de rehacer debe vaciarse. Si no, podrías «rehacer» una
    acción que ya no tiene sentido en el nuevo estado.

    Complejidad: registrar O(1), deshacer O(1), rehacer O(1)
    """

    def __init__(self):
        self._hechas = PilaEnlazada()
        self._deshechas = PilaEnlazada()

    def registrar(self, accion):
        """Registra una acción nueva. Invalida el historial de rehacer."""
        pass

    def deshacer(self):
        """Devuelve la última acción y la mueve a la pila de rehacer.
        Lanza PilaVaciaError si no hay nada que deshacer."""
        pass

    def rehacer(self):
        """Devuelve la última acción deshecha y la vuelve a aplicar.
        Lanza PilaVaciaError si no hay nada que rehacer."""
        pass

    def puede_deshacer(self):
        return not self._hechas.esta_vacia()

    def puede_rehacer(self):
        return not self._deshechas.esta_vacia()


# --- pruebas ---
import pytest


def test_deshacer_rehacer_basico():
    h = Historial()
    h.registrar("escribir A")
    h.registrar("escribir B")
    assert h.deshacer() == "escribir B"
    assert h.rehacer() == "escribir B"


def test_accion_nueva_invalida_rehacer():
    """La regla crítica."""
    h = Historial()
    h.registrar("A")
    h.registrar("B")
    h.deshacer()                       # deshace B
    assert h.puede_rehacer()
    h.registrar("C")                   # acción nueva
    assert not h.puede_rehacer()       # B ya no se puede rehacer


def test_deshacer_sin_nada():
    with pytest.raises(PilaVaciaError):
        Historial().deshacer()
