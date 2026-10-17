"""Actividad 5, partes C y D: el árbol de carpetas.

Conteo, ruta más profunda y profundidad: RECURSIVOS.
Listado por niveles: iterativo, con la cola propia (sin collections.deque).
"""


class Carpeta:
    def __init__(self, nombre, entregas=0):
        self.nombre = nombre
        self.entregas = entregas  # entregas guardadas directamente en esta carpeta
        self.hijos = []

    def agregar(self, hijo):
        self.hijos.append(hijo)
        return hijo


# ---------------------------------------------------------------- estructuras
class _Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.sig = None


class Cola:
    """FIFO con nodos enlazados. Reemplázala por la cola de tu Parte A."""

    def __init__(self):
        self._frente = None
        self._final = None

    def esta_vacia(self):
        return self._frente is None

    def encolar(self, dato):
        nodo = _Nodo(dato)
        if self._final is None:
            self._frente = self._final = nodo
        else:
            self._final.sig = nodo
            self._final = nodo

    def desencolar(self):
        if self._frente is None:
            raise IndexError("cola vacía")
        dato = self._frente.dato
        self._frente = self._frente.sig
        if self._frente is None:
            self._final = None
        return dato


class Pila:
    """LIFO con nodos enlazados (solo para la comparación de la Parte D)."""

    def __init__(self):
        self._tope = None

    def esta_vacia(self):
        return self._tope is None

    def apilar(self, dato):
        nodo = _Nodo(dato)
        nodo.sig = self._tope
        self._tope = nodo

    def desapilar(self):
        if self._tope is None:
            raise IndexError("pila vacía")
        dato = self._tope.dato
        self._tope = self._tope.sig
        return dato


# ------------------------------------------------------- consultas recursivas
def contar_entregas(nodo):
    """Total de entregas bajo `nodo` (incluido él). Árbol vacío -> 0."""
    if nodo is None:  # caso base 1: árbol vacío
        return 0
    total = nodo.entregas
    for hijo in nodo.hijos:  # si no hay hijos, el for no corre: caso base 2 (hoja)
        total += contar_entregas(hijo)
    return total


def ruta_mas_profunda(nodo):
    """Lista de nombres de la raíz a la hoja más lejana. Árbol vacío -> [].
    En empate gana la rama que aparece primero."""
    if nodo is None:
        return []
    mejor = []
    for hijo in nodo.hijos:
        candidata = ruta_mas_profunda(hijo)
        if len(candidata) > len(mejor):  # '>' estricto: conserva la primera
            mejor = candidata
    return [nodo.nombre] + mejor


def profundidad_maxima(nodo):
    """Número de niveles. Vacío -> 0, un solo nodo -> 1."""
    if nodo is None:
        return 0
    mayor = 0
    for hijo in nodo.hijos:
        mayor = max(mayor, profundidad_maxima(hijo))
    return 1 + mayor


# --------------------------------------------------------- listado por niveles
def listar_por_niveles(raiz):
    """Devuelve una lista de niveles; cada nivel es una lista de nombres.
    Usa la cola propia; el truco de los niveles es medir cuántos nodos
    hay en la cola al empezar cada vuelta."""
    if raiz is None:
        return []
    niveles = []
    cola = Cola()
    cola.encolar(raiz)
    pendientes = 1
    while not cola.esta_vacia():
        nivel = []
        siguientes = 0
        for _ in range(pendientes):
            actual = cola.desencolar()
            nivel.append(actual.nombre)
            for hijo in actual.hijos:
                cola.encolar(hijo)
                siguientes += 1
        niveles.append(nivel)
        pendientes = siguientes
    return niveles


def listar_con_pila(raiz):
    """MISMO código que arriba pero con pila: sirve para la Parte D.
    Devuelve el orden plano de visita (la pila ya no respeta los niveles)."""
    if raiz is None:
        return []
    orden = []
    pila = Pila()
    pila.apilar(raiz)
    while not pila.esta_vacia():
        actual = pila.desapilar()
        orden.append(actual.nombre)
        for hijo in actual.hijos:
            pila.apilar(hijo)
    return orden


# ------------------------------------------------------------- árbol de prueba
def arbol_de_prueba():
    srv = Carpeta("Servidor")
    ing = srv.agregar(Carpeta("Ingenieria"))
    der = srv.agregar(Carpeta("Derecho"))

    sis = ing.agregar(Carpeta("Sistemas"))
    edd = sis.agregar(Carpeta("EstructurasDatos"))
    edd.agregar(Carpeta("2026-1", 12))
    s2 = edd.agregar(Carpeta("2026-2", 10))
    s2.agregar(Carpeta("ProyectoFinal", 8))
    bd = sis.agregar(Carpeta("BasesDatos"))
    bd.agregar(Carpeta("2026-1B", 15))

    civ = ing.agregar(Carpeta("Civil"))
    est = civ.agregar(Carpeta("Estatica"))
    est.agregar(Carpeta("2025-2", 9))

    pen = der.agregar(Carpeta("DerechoPenal1"))
    pen.agregar(Carpeta("2026-2D", 7))
    return srv


if __name__ == "__main__":
    t = arbol_de_prueba()
    print("Total entregas:", contar_entregas(t))
    print("Ruta más profunda:", " / ".join(ruta_mas_profunda(t)))
    print("Profundidad máxima:", profundidad_maxima(t))
    print("Por niveles (cola):")
    for i, n in enumerate(listar_por_niveles(t), 1):
        print(f"  nivel {i}:", n)
    print("Con pila:", listar_con_pila(t))
