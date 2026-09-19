# Código base — Semana 06
# Fuente: 01-Momento-1-Contrato-y-secuencia/06-Semana-06-Listas-enlazadas-simples/02-guia-de-laboratorio.html
#
# Contrato heredado de la actividad 2 (semana 04): las pruebas de este
# archivo corren contra CUALQUIER implementación listada en IMPLEMENTACIONES.
# No se modifica al pasar a la actividad 3: si ListaEnlazada cumple el mismo
# contrato que ListaArreglo, estas pruebas deben pasar sin tocarlas.

import pytest
from lista_arreglo import ListaArreglo, PosicionInvalidaError as PosArregloError
from lista_enlazada import ListaEnlazada, PosicionInvalidaError as PosEnlazadaError

# ANTES:  IMPLEMENTACIONES = [ListaArreglo]
IMPLEMENTACIONES = [ListaArreglo, ListaEnlazada]

# No cambies NADA más. Ejecuta:
#     pytest -v
# Deberías ver cada prueba corriendo dos veces, una por implementación.


@pytest.fixture(params=IMPLEMENTACIONES)
def lista_vacia(request):
    return request.param()


def _llenar(lista, elementos):
    for i, e in enumerate(elementos):
        lista.insertar(i, e)
    return lista


class TestTamañoYObtener:
    def test_lista_nueva_esta_vacia(self, lista_vacia):
        assert lista_vacia.tamaño() == 0
        assert len(lista_vacia) == 0

    def test_tamaño_crece_con_insertar(self, lista_vacia):
        _llenar(lista_vacia, ["a", "b", "c"])
        assert lista_vacia.tamaño() == 3

    def test_obtener_devuelve_elemento_correcto(self, lista_vacia):
        _llenar(lista_vacia, ["a", "b", "c"])
        assert lista_vacia.obtener(0) == "a"
        assert lista_vacia.obtener(1) == "b"
        assert lista_vacia.obtener(2) == "c"

    def test_obtener_posicion_invalida_lanza(self, lista_vacia):
        with pytest.raises(IndexError):
            lista_vacia.obtener(0)

    def test_obtener_posicion_negativa_lanza(self, lista_vacia):
        _llenar(lista_vacia, ["a"])
        with pytest.raises(IndexError):
            lista_vacia.obtener(-1)


class TestInsertar:
    def test_insertar_al_final_mantiene_orden(self, lista_vacia):
        _llenar(lista_vacia, ["a", "b", "c"])
        assert list(lista_vacia) == ["a", "b", "c"]

    def test_insertar_al_inicio_desplaza(self, lista_vacia):
        _llenar(lista_vacia, ["b", "c"])
        lista_vacia.insertar(0, "a")
        assert list(lista_vacia) == ["a", "b", "c"]

    def test_insertar_en_medio(self, lista_vacia):
        _llenar(lista_vacia, ["a", "c"])
        lista_vacia.insertar(1, "b")
        assert list(lista_vacia) == ["a", "b", "c"]

    def test_insertar_posicion_invalida_lanza(self, lista_vacia):
        with pytest.raises(IndexError):
            lista_vacia.insertar(1, "x")

    def test_insertar_muchos_elementos(self, lista_vacia):
        for i in range(50):
            lista_vacia.insertar(i, i)
        assert lista_vacia.tamaño() == 50
        assert list(lista_vacia) == list(range(50))


class TestEliminar:
    def test_eliminar_devuelve_el_elemento(self, lista_vacia):
        _llenar(lista_vacia, ["a", "b", "c"])
        assert lista_vacia.eliminar(1) == "b"

    def test_eliminar_reduce_tamaño(self, lista_vacia):
        _llenar(lista_vacia, ["a", "b", "c"])
        lista_vacia.eliminar(1)
        assert lista_vacia.tamaño() == 2

    def test_eliminar_desplaza_los_siguientes(self, lista_vacia):
        _llenar(lista_vacia, ["a", "b", "c"])
        lista_vacia.eliminar(0)
        assert list(lista_vacia) == ["b", "c"]

    def test_eliminar_posicion_invalida_lanza(self, lista_vacia):
        with pytest.raises(IndexError):
            lista_vacia.eliminar(0)


class TestBuscar:
    def test_buscar_elemento_presente(self, lista_vacia):
        _llenar(lista_vacia, ["a", "b", "c"])
        assert lista_vacia.buscar("b") == 1

    def test_buscar_elemento_ausente(self, lista_vacia):
        _llenar(lista_vacia, ["a", "b", "c"])
        assert lista_vacia.buscar("z") == -1

    def test_buscar_en_lista_vacia(self, lista_vacia):
        assert lista_vacia.buscar("cualquiera") == -1


class TestIteracionYRepr:
    def test_iterar_recorre_en_orden(self, lista_vacia):
        _llenar(lista_vacia, [1, 2, 3])
        assert [x for x in lista_vacia] == [1, 2, 3]

    def test_getitem_equivale_a_obtener(self, lista_vacia):
        _llenar(lista_vacia, ["x", "y"])
        assert lista_vacia[0] == "x"
        assert lista_vacia[1] == "y"
