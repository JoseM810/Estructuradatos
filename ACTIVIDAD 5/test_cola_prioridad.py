import pytest
from cola_prioridad import Cola, ColaPrioridad, ALTA, MEDIA, BAJA

SIN_ENVEJECER = 1e12


# ------------------------------------------------------------------ Cola FIFO
def test_cola_fifo_orden_y_vacia():
    c = Cola()
    assert c.esta_vacia() and len(c) == 0
    for x in "abc":
        c.encolar(x)
    assert len(c) == 3 and c.ver_frente() == "a"
    assert [c.desencolar() for _ in range(3)] == ["a", "b", "c"]
    assert c.esta_vacia()
    with pytest.raises(IndexError):
        c.desencolar()


def test_cola_reutilizable_tras_vaciarse():
    c = Cola()
    c.encolar(1)
    c.desencolar()
    c.encolar(2)          # falla si _final quedó colgando
    c.encolar(3)
    assert c.desencolar() == 2 and c.desencolar() == 3


# ------------------------------------------------------------ Cola prioridad
def test_tres_niveles_salen_por_prioridad():
    q = ColaPrioridad(paso_envejecimiento=SIN_ENVEJECER)
    q.encolar("baja", BAJA, 0)
    q.encolar("alta", ALTA, 0)
    q.encolar("media", MEDIA, 0)
    assert [q.desencolar(0) for _ in range(3)] == ["alta", "media", "baja"]


def test_mismo_nivel_respeta_orden_de_llegada():
    q = ColaPrioridad()
    for i in range(4):
        q.encolar(i, MEDIA, i)
    assert [q.desencolar(10) for _ in range(4)] == [0, 1, 2, 3]


def test_errores():
    q = ColaPrioridad()
    with pytest.raises(IndexError):
        q.desencolar(0)
    with pytest.raises(ValueError):
        q.encolar("x", 7, 0)
    with pytest.raises(ValueError):
        ColaPrioridad(0)


def _llegan_altas_sin_parar(paso):
    """Un BAJA llega en t=0; luego llega 1 ALTA por minuto y se atiende 1 por
    minuto. Devuelve el minuto en que sale el BAJA (o None si no sale)."""
    q = ColaPrioridad(paso)
    q.encolar("BAJA", BAJA, 0)
    for t in range(1, 200):
        q.encolar(f"alta{t}", ALTA, t)
        if q.desencolar(t) == "BAJA":
            return t
    return None


def test_sin_envejecimiento_el_baja_nunca_sale():
    assert _llegan_altas_sin_parar(SIN_ENVEJECER) is None


def test_con_envejecimiento_el_baja_sale_antes_de_2_pasos():
    # Caso de prueba de la garantía: cota = 2 * paso
    for paso in (5, 10, 15):
        t = _llegan_altas_sin_parar(paso)
        assert t is not None and t <= 2 * paso


def test_nadie_es_superado_por_uno_que_llego_mas_de_2_pasos_despues():
    paso = 10
    q = ColaPrioridad(paso)
    q.encolar("viejo-baja", BAJA, 0)
    q.encolar("nuevo-alta", ALTA, 2 * paso)   # llega 2*paso minutos después
    assert q.desencolar(2 * paso) == "viejo-baja"
