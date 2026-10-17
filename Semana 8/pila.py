# Código base — Semana 08
# Fuente: 02-Momento-2-Disciplina-y-jerarquia/08-Semana-08-Pilas/02-guia-de-laboratorio.html

from nodo import Nodo


class PilaVaciaError(IndexError):
    """Se intentó operar sobre una pila vacía."""


class PilaArreglo:
    """Pila sobre arreglo dinámico. El tope es el ÚLTIMO elemento.

    ¿Por qué el último y no el primero? Porque insertar y quitar al final
    de un arreglo es O(1); al inicio sería O(n) por los desplazamientos.

    Complejidad: push O(1) amortizado, pop O(1), peek O(1)
    """

    def __init__(self):
        self._datos = []

    def push(self, elemento):
        pass

    def pop(self):
        if self.esta_vacia():
            raise PilaVaciaError("pop sobre pila vacía")
        pass

    def peek(self):
        if self.esta_vacia():
            raise PilaVaciaError("peek sobre pila vacía")
        pass

    def esta_vacia(self):
        return len(self._datos) == 0

    def tamaño(self):
        return len(self._datos)

    def __len__(self):
        return self.tamaño()


class PilaEnlazada:
    """Pila sobre nodos enlazados. El tope es la CABEZA.

    ¿Por qué la cabeza? Porque insertar y quitar al inicio de una lista
    enlazada es O(1); al final sería O(n) por el recorrido.

    Complejidad: push O(1), pop O(1), peek O(1) — sin amortizar
    """

    def __init__(self):
        self._tope = None
        self._tamaño = 0

    def push(self, elemento):
        pass

    def pop(self):
        if self.esta_vacia():
            raise PilaVaciaError("pop sobre pila vacía")
        pass

    def peek(self):
        if self.esta_vacia():
            raise PilaVaciaError("peek sobre pila vacía")
        return self._tope.dato

    def esta_vacia(self):
        return self._tope is None

    def tamaño(self):
        return self._tamaño

    def __len__(self):
        return self._tamaño
