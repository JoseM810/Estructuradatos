from simulacion import (generar_trabajos, simular, ColaFIFO, experimento,
                        ESTRATEGIAS, Trabajo)
from cola_prioridad import ColaPrioridad, ALTA, BAJA


def test_mismos_trabajos_con_misma_semilla():
    a, b = generar_trabajos(3), generar_trabajos(3)
    assert [(t.llegada, t.servicio, t.prioridad) for t in a] == \
           [(t.llegada, t.servicio, t.prioridad) for t in b]


def test_todos_los_trabajos_se_atienden():
    trabajos = generar_trabajos(1)
    for _, fabrica in ESTRATEGIAS:
        assert len(simular(trabajos, fabrica())) == len(trabajos)


def test_fifo_calculo_a_mano():
    # llegadas 0, 1, 2; servicio 5 cada uno: esperas 0, 4, 8
    ts = [Trabajo(0, 5, BAJA), Trabajo(1, 5, ALTA), Trabajo(2, 5, BAJA)]
    esperas = [e for e, _ in simular(ts, ColaFIFO())]
    assert esperas == [0, 4, 8]


def test_prioridad_adelanta_al_alta_a_mano():
    # El trabajo 0 ocupa el puesto hasta t=5; en ese momento esperan
    # el BAJA (llegó en 1) y el ALTA (llegó en 2): sale primero el ALTA.
    ts = [Trabajo(0, 5, BAJA), Trabajo(1, 5, BAJA), Trabajo(2, 5, ALTA)]
    esperas = simular(ts, ColaPrioridad(1e12))
    assert [(round(e), p) for e, p in esperas] == [(0, BAJA), (3, ALTA), (9, BAJA)]


def test_experimento_corre_y_prioridad_favorece_al_alta():
    res = experimento(jornadas=5)
    pr = res["Prioridad con envejecimiento"]["por_nivel"]
    fifo = res["Orden de llegada (FIFO)"]["por_nivel"]
    assert sum(pr[ALTA]) / len(pr[ALTA]) < sum(fifo[ALTA]) / len(fifo[ALTA])
