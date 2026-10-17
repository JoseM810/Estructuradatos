import pytest
from lista_arreglo import ListaArreglo, PosicionInvalidaError


def construir(valores):
    lista = ListaArreglo()
    for i, v in enumerate(valores):
        lista.insertar(i, v)
    return lista


def contenido(lista):
    return [lista.obtener(i) for i in range(lista.tamaño())]


# ---------- contrato base (CA-01 a CA-06) ----------

def test_lista_vacia():
    assert ListaArreglo().tamaño() == 0


def test_insertar_en_vacia():
    lista = ListaArreglo()
    lista.insertar(0, "a")
    assert lista.tamaño() == 1
    assert lista.obtener(0) == "a"


def test_insertar_inicio():
    lista = construir(["b", "c"])
    lista.insertar(0, "a")
    assert contenido(lista) == ["a", "b", "c"]


def test_eliminar():
    lista = construir(["x"])
    assert lista.eliminar(0) == "x"
    assert lista.tamaño() == 0


def test_posicion_invalida():
    lista = ListaArreglo()
    with pytest.raises(PosicionInvalidaError):
        lista.obtener(0)
    with pytest.raises(PosicionInvalidaError):
        lista.insertar(5, "x")
    with pytest.raises(PosicionInvalidaError):
        lista.insertar(-1, "x")


def test_buscar_ausente():
    assert ListaArreglo().buscar("fantasma") == -1


def test_redimensionamiento():
    lista = ListaArreglo()
    for i in range(100):
        lista.insertar(i, i)
    assert lista.tamaño() == 100
    assert contenido(lista) == list(range(100))


# ---------- los cuatro casos extremos exigidos ----------

def test_extremo_lista_vacia():
    lista = ListaArreglo()
    assert lista.tamaño() == 0
    assert lista.buscar_lineal(1) == -1
    assert lista.buscar_binaria(1) == -1
    with pytest.raises(PosicionInvalidaError):
        lista.obtener(0)
    with pytest.raises(PosicionInvalidaError):
        lista.eliminar(0)


def test_extremo_un_elemento():
    lista = construir([7])
    assert lista.buscar_lineal(7) == 0
    assert lista.buscar_binaria(7) == 0
    assert lista.buscar_binaria(1) == -1
    assert lista.buscar_binaria(9) == -1
    assert lista.eliminar(0) == 7
    assert lista.tamaño() == 0


def test_extremo_insertar_al_inicio_repetido():
    lista = ListaArreglo()
    for v in range(10):
        lista.insertar(0, v)
    assert contenido(lista) == list(range(9, -1, -1))


def test_extremo_insertar_al_final_repetido():
    lista = ListaArreglo()
    for v in range(10):
        lista.insertar(lista.tamaño(), v)
    assert contenido(lista) == list(range(10))


def test_insertar_justo_al_llenar_capacidad():
    # capacidad inicial 4: el 5.º elemento dispara el redimensionamiento
    lista = construir([1, 2, 3, 4])
    lista.insertar(0, 0)
    assert contenido(lista) == [0, 1, 2, 3, 4]


# ---------- insertar_ordenado ----------

def test_insertar_ordenado_en_vacia():
    lista = ListaArreglo()
    lista.insertar_ordenado(5)
    assert contenido(lista) == [5]


def test_insertar_ordenado_inicio_medio_final():
    lista = construir([10, 20, 30, 40])
    lista.insertar_ordenado(5)    # inicio
    lista.insertar_ordenado(25)   # medio
    lista.insertar_ordenado(99)   # final
    assert contenido(lista) == [5, 10, 20, 25, 30, 40, 99]


def test_insertar_ordenado_desordenado_produce_orden():
    lista = ListaArreglo()
    for v in [8, 3, 9, 1, 7, 2, 6, 4, 5, 0]:
        lista.insertar_ordenado(v)
    assert contenido(lista) == list(range(10))


def test_insertar_ordenado_con_repetidos_es_estable():
    lista = construir([1, 2, 2, 3])
    lista.insertar_ordenado(2)
    assert contenido(lista) == [1, 2, 2, 2, 3]


# ---------- busqueda binaria ----------

@pytest.mark.parametrize("n", [1, 2, 3, 4, 5, 8, 9, 100, 101])
def test_buscar_binaria_todos_los_presentes_y_ausentes(n):
    # tamaños pares e impares; valores pares para dejar huecos (impares ausentes)
    lista = construir([2 * i for i in range(n)])
    for i in range(n):
        assert lista.buscar_binaria(2 * i) == i
    assert lista.buscar_binaria(-1) == -1          # menor que todos
    assert lista.buscar_binaria(2 * n) == -1       # mayor que todos
    for i in range(n):
        assert lista.buscar_binaria(2 * i + 1) == -1


def test_buscar_binaria_bordes():
    lista = construir([1, 3, 5, 7])
    assert lista.buscar_binaria(1) == 0
    assert lista.buscar_binaria(7) == 3


def test_buscar_binaria_devuelve_primera_aparicion():
    lista = construir([1, 2, 2, 2, 3])
    assert lista.buscar_binaria(2) == 1


def test_buscar_binaria_coincide_con_lineal():
    lista = construir(list(range(0, 200, 3)))
    for x in range(-2, 205):
        assert lista.buscar_binaria(x) == lista.buscar_lineal(x)


# ---------- busqueda lineal y eliminar ----------

def test_buscar_lineal_primera_aparicion():
    lista = construir(["a", "b", "a"])
    assert lista.buscar_lineal("a") == 0
    assert lista.buscar_lineal("z") == -1


def test_eliminar_en_medio_conserva_orden():
    lista = construir([1, 2, 3, 4])
    assert lista.eliminar(1) == 2
    assert contenido(lista) == [1, 3, 4]
