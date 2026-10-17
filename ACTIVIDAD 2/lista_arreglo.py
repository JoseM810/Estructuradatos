"""Actividad 2 - El catálogo de la biblioteca: ¿ordenar o no ordenar?

ListaArreglo implementada desde cero sobre un arreglo de capacidad fija con
redimensionamiento. No se usan append, insert, pop, sort, bisect ni `in`:
la lista de Python solo se usa como bloque de memoria contigua (`[None] * n`),
accedido únicamente por índice.
"""


class PosicionInvalidaError(IndexError):
    """La posición solicitada está fuera del rango válido."""


class ListaArreglo:
    """Lista implementada sobre un arreglo de tamaño fijo con redimensionamiento.

    Atributos internos:
        _datos      arreglo subyacente (capacidad fija en cada momento)
        _capacidad  cuántas posiciones tiene el arreglo
        _tamaño     cuántas posiciones están realmente ocupadas

    Invariante de representación: 0 <= _tamaño <= _capacidad

    Complejidad:
        obtener           -> O(1)
        insertar(final)   -> O(1) amortizado
        insertar(inicio)  -> O(n)
        insertar_ordenado -> O(log n) para ubicar + O(n) para desplazar = O(n)
        eliminar          -> O(n)
        buscar_lineal     -> O(n)
        buscar_binaria    -> O(log n)   (exige lista ordenada ascendente)
    """

    CAPACIDAD_INICIAL = 4

    def __init__(self):
        self._capacidad = self.CAPACIDAD_INICIAL
        self._datos = [None] * self._capacidad
        self._tamaño = 0

    # ---------- operaciones públicas ----------

    def tamaño(self):
        return self._tamaño

    def obtener(self, posicion):
        """Devuelve el elemento en `posicion`. O(1)."""
        self._validar(posicion, incluir_final=False)
        return self._datos[posicion]

    def insertar(self, posicion, elemento):
        """Inserta desplazando los elementos siguientes hacia la derecha.

        O(n - posicion) desplazamientos; O(1) amortizado si posicion == tamaño.
        """
        self._validar(posicion, incluir_final=True)
        if self._tamaño == self._capacidad:
            self._redimensionar(self._capacidad * 2)
        # Desde el FINAL hacia atrás: si fuera desde el principio, cada
        # asignación sobrescribiría un dato que aún no se ha copiado.
        for i in range(self._tamaño, posicion, -1):
            self._datos[i] = self._datos[i - 1]
        self._datos[posicion] = elemento
        self._tamaño += 1

    def insertar_ordenado(self, elemento):
        """Inserta `elemento` conservando el orden ascendente.

        Precondición: la lista ya está ordenada.
        Usa búsqueda binaria (O(log n)) para hallar la posición y luego
        `insertar` para desplazar (O(n)). Si hay iguales, queda después de ellos
        (inserción estable).
        """
        izq, der = 0, self._tamaño
        while izq < der:
            medio = (izq + der) // 2
            if elemento < self._datos[medio]:
                der = medio
            else:
                izq = medio + 1
        self.insertar(izq, elemento)

    def eliminar(self, posicion):
        """Elimina y devuelve el elemento, desplazando los siguientes."""
        self._validar(posicion, incluir_final=False)
        elemento = self._datos[posicion]
        for i in range(posicion, self._tamaño - 1):
            self._datos[i] = self._datos[i + 1]
        self._datos[self._tamaño - 1] = None
        self._tamaño -= 1
        return elemento

    def buscar_lineal(self, elemento):
        """Devuelve la posición de la primera aparición, o -1. O(n)."""
        for i in range(self._tamaño):
            if self._datos[i] == elemento:
                return i
        return -1

    def buscar(self, elemento):
        """Alias de buscar_lineal (contrato de la semana 4)."""
        return self.buscar_lineal(elemento)

    def buscar_binaria(self, elemento):
        """Devuelve la posición de la primera aparición, o -1. O(log n).

        Precondición: la lista está ordenada ascendentemente.
        Intervalo semiabierto [izq, der): funciona con tamaño par o impar,
        lista vacía y elemento en cualquiera de los bordes.
        """
        izq, der = 0, self._tamaño
        while izq < der:
            medio = (izq + der) // 2
            if self._datos[medio] < elemento:
                izq = medio + 1
            else:
                der = medio
        if izq < self._tamaño and self._datos[izq] == elemento:
            return izq
        return -1

    # ---------- auxiliares ----------

    def _validar(self, posicion, incluir_final):
        limite = self._tamaño if incluir_final else self._tamaño - 1
        if not 0 <= posicion <= limite:
            raise PosicionInvalidaError(
                f"posicion {posicion} fuera de rango [0, {limite}]"
            )

    def _redimensionar(self, nueva_capacidad):
        """Crea un arreglo mayor y copia los elementos. O(n)."""
        nuevo = [None] * nueva_capacidad
        for i in range(self._tamaño):
            nuevo[i] = self._datos[i]
        self._datos = nuevo
        self._capacidad = nueva_capacidad

    # ---------- protocolo de Python ----------

    def __len__(self):
        return self._tamaño

    def __getitem__(self, i):
        return self.obtener(i)

    def __iter__(self):
        for i in range(self._tamaño):
            yield self._datos[i]

    def __repr__(self):
        return f"ListaArreglo({list(self)!r})"
