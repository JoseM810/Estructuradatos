"""Actividad 5, Parte A: cola FIFO y cola de prioridad con envejecimiento.

Sin heapq: la cola de prioridad se construye aquí, con nodos enlazados.

DISEÑO
------
Tres niveles de prioridad (ALTA=3, MEDIA=2, BAJA=1). Se guarda UNA cola FIFO
por nivel. Dentro de un mismo nivel el que lleva más tiempo esperando es
siempre el primero de su cola, así que para decidir quién sigue basta mirar
el frente de cada una de las 3 colas (3 comparaciones: O(1)).

MECANISMO CONTRA LA ESPERA INDEFINIDA: ENVEJECIMIENTO
-----------------------------------------------------
Cada trabajo tiene un puntaje que crece mientras espera:

    puntaje = prioridad * paso + (ahora - llegada)

`paso` son los minutos de espera que equivalen a subir un nivel de
prioridad. Sale el trabajo con mayor puntaje; si hay empate, el que llegó
primero.

GARANTÍA (la que se demuestra en test_cola_prioridad.py)
--------------------------------------------------------
Un trabajo A solo puede ser superado por otro B que llegó DESPUÉS de A si
    (prioridad_B - prioridad_A) * paso > llegada_B - llegada_A.
Como la diferencia máxima de prioridad es 2, ningún trabajo es superado por
uno que llegó más de 2*paso minutos después. Un trabajo BAJA que espera
2*paso minutos queda por delante de todo lo que llegue después, así que la
espera de nadie es indefinida.

Sin envejecimiento (paso enorme) el puntaje se decide solo por la prioridad
y una ráfaga constante de trabajos ALTA deja a los BAJA esperando para siempre.
"""

ALTA, MEDIA, BAJA = 3, 2, 1
NIVELES = (ALTA, MEDIA, BAJA)  # se revisan de mayor a menor prioridad


class _Nodo:
    """Eslabón de una lista enlazada: un dato y la referencia al siguiente."""

    def __init__(self, dato):
        self.dato = dato
        self.sig = None


class Cola:
    """Cola FIFO con nodos enlazados. encolar/desencolar/ver_frente: O(1)."""

    def __init__(self):
        self._frente = None  # de aquí se saca
        self._final = None   # aquí se agrega
        self._tam = 0

    def __len__(self):
        return self._tam

    def esta_vacia(self):
        return self._frente is None

    def encolar(self, dato):
        nodo = _Nodo(dato)
        if self._final is None:        # cola vacía: primero y último a la vez
            self._frente = self._final = nodo
        else:
            self._final.sig = nodo     # primero se enlaza...
            self._final = nodo         # ...y luego se mueve el final
        self._tam += 1

    def ver_frente(self):
        """Devuelve el primero sin sacarlo."""
        if self._frente is None:
            raise IndexError("cola vacía")
        return self._frente.dato

    def desencolar(self):
        if self._frente is None:
            raise IndexError("cola vacía")
        dato = self._frente.dato
        self._frente = self._frente.sig
        if self._frente is None:       # quedó vacía: no dejar _final colgando
            self._final = None
        self._tam -= 1
        return dato


class _Entrada:
    """Lo que se guarda en la cola: el dato, su nivel y cuándo llegó."""

    def __init__(self, dato, prioridad, llegada):
        self.dato = dato
        self.prioridad = prioridad
        self.llegada = llegada


class ColaPrioridad:
    """Cola de prioridad de 3 niveles con envejecimiento.

    paso: minutos de espera que valen un nivel de prioridad.
    Para simular "sin envejecimiento" se usa un paso enorme (p. ej. 1e12).
    """

    def __init__(self, paso_envejecimiento=10.0):
        if paso_envejecimiento <= 0:
            raise ValueError("el paso de envejecimiento debe ser positivo")
        self.paso = paso_envejecimiento
        self._colas = {nivel: Cola() for nivel in NIVELES}
        self._tam = 0

    def __len__(self):
        return self._tam

    def esta_vacia(self):
        return self._tam == 0

    def encolar(self, dato, prioridad, ahora):
        """Agrega `dato` con su prioridad; `ahora` es el momento de llegada."""
        if prioridad not in self._colas:
            raise ValueError(f"prioridad inválida: {prioridad}")
        self._colas[prioridad].encolar(_Entrada(dato, prioridad, ahora))
        self._tam += 1

    def puntaje(self, entrada, ahora):
        """Prioridad efectiva: nivel base + espera acumulada (en minutos)."""
        return entrada.prioridad * self.paso + (ahora - entrada.llegada)

    def desencolar(self, ahora):
        """Saca el de mayor puntaje en el instante `ahora`."""
        if self._tam == 0:
            raise IndexError("cola vacía")
        mejor_nivel, mejor_puntaje, mejor_llegada = None, None, None
        for nivel in NIVELES:
            cola = self._colas[nivel]
            if cola.esta_vacia():
                continue
            frente = cola.ver_frente()   # el que más espera de su nivel
            p = self.puntaje(frente, ahora)
            if (mejor_nivel is None or p > mejor_puntaje
                    or (p == mejor_puntaje and frente.llegada < mejor_llegada)):
                mejor_nivel, mejor_puntaje, mejor_llegada = nivel, p, frente.llegada
        self._tam -= 1
        return self._colas[mejor_nivel].desencolar().dato
