"""Actividad 5, Parte B: simulación de la sala de cómputo.

Compara dos estrategias de atención sobre EXACTAMENTE los mismos trabajos:
  1. Orden de llegada (FIFO).
  2. Cola de prioridad con envejecimiento (cola_prioridad.py).
Y, solo como control del análisis, una tercera: prioridad SIN envejecimiento.

SUPUESTOS (documentados para quien califique)
---------------------------------------------
- Un puesto de atención (un técnico) que atiende un trabajo a la vez.
- Jornada de 480 min (8 h): llegan trabajos durante la jornada y luego se
  termina de atender lo que quedó en cola.
- Llegadas de Poisson (tiempos entre llegadas exponenciales, media 5 min).
- Servicio exponencial, media 4,5 min  ->  utilización ~ 90 %: sala ocupada,
  con cola, que es donde las estrategias se diferencian.
- Mezcla: 20 % ALTA (docentes / clases), 30 % MEDIA (proyectos), 50 % BAJA
  (uso libre).
- Se repite con 300 jornadas (semillas 0..299). En cada semilla las dos
  estrategias reciben los mismos trabajos, así la diferencia no es azar.
- Tiempo de espera = momento en que empieza el servicio - momento de llegada.
"""
import random

from cola_prioridad import Cola, ColaPrioridad, ALTA, MEDIA, BAJA

JORNADA = 480.0
MEDIA_LLEGADA = 5.0
MEDIA_SERVICIO = 4.5
MEZCLA = ((ALTA, 0.20), (MEDIA, 0.30), (BAJA, 0.50))
PASO_ENVEJECIMIENTO = 15.0   # min de espera que valen un nivel
SIN_ENVEJECER = 1e12         # paso enorme = la espera casi no pesa
JORNADAS = 300
NOMBRE = {ALTA: "alta", MEDIA: "media", BAJA: "baja"}


class Trabajo:
    def __init__(self, llegada, servicio, prioridad):
        self.llegada = llegada
        self.servicio = servicio
        self.prioridad = prioridad


def generar_trabajos(semilla):
    """Trabajos de una jornada, ordenados por llegada."""
    rng = random.Random(semilla)
    niveles = [n for n, _ in MEZCLA]
    pesos = [p for _, p in MEZCLA]
    trabajos, t = [], 0.0
    while True:
        t += rng.expovariate(1 / MEDIA_LLEGADA)
        if t > JORNADA:
            return trabajos
        prioridad = rng.choices(niveles, weights=pesos)[0]
        trabajos.append(Trabajo(t, rng.expovariate(1 / MEDIA_SERVICIO), prioridad))


class ColaFIFO:
    """Adaptador: la Cola FIFO con la misma interfaz que ColaPrioridad."""

    def __init__(self):
        self._cola = Cola()

    def esta_vacia(self):
        return self._cola.esta_vacia()

    def encolar(self, dato, prioridad, ahora):
        self._cola.encolar(dato)

    def desencolar(self, ahora):
        return self._cola.desencolar()


def simular(trabajos, cola):
    """Atiende todos los trabajos con la cola dada.
    Devuelve una lista de (espera, prioridad), una por trabajo."""
    esperas, t, i, n = [], 0.0, 0, len(trabajos)
    while i < n or not cola.esta_vacia():
        if cola.esta_vacia():                      # el técnico espera trabajo
            t = max(t, trabajos[i].llegada)
        while i < n and trabajos[i].llegada <= t:  # llegan los que ya vinieron
            cola.encolar(trabajos[i], trabajos[i].prioridad, trabajos[i].llegada)
            i += 1
        trabajo = cola.desencolar(t)
        esperas.append((t - trabajo.llegada, trabajo.prioridad))
        t += trabajo.servicio                      # lo atiende hasta terminar
    return esperas


ESTRATEGIAS = (
    ("Orden de llegada (FIFO)", ColaFIFO),
    ("Prioridad con envejecimiento", lambda: ColaPrioridad(PASO_ENVEJECIMIENTO)),
    ("Prioridad SIN envejecimiento (control)", lambda: ColaPrioridad(SIN_ENVEJECER)),
)


def experimento(jornadas=JORNADAS):
    """Devuelve {estrategia: métricas}."""
    res = {}
    for nombre, _ in ESTRATEGIAS:
        res[nombre] = {"todas": [], "peores": [], "por_nivel": {n: [] for n in NOMBRE}}
    for semilla in range(jornadas):
        trabajos = generar_trabajos(semilla)
        for nombre, fabrica in ESTRATEGIAS:
            esperas = simular(trabajos, fabrica())
            r = res[nombre]
            r["todas"].extend(e for e, _ in esperas)
            r["peores"].append(max(e for e, _ in esperas))
            for e, p in esperas:
                r["por_nivel"][p].append(e)
    return res


def _media(xs):
    return sum(xs) / len(xs)


def tabla(res):
    lineas = [
        "| Estrategia | Espera media (min) | Peor espera, promedio por jornada (min) | Peor espera de todas las jornadas (min) |",
        "|---|---|---|---|",
    ]
    for nombre, r in res.items():
        lineas.append(f"| {nombre} | {_media(r['todas']):.1f} | "
                      f"{_media(r['peores']):.1f} | {max(r['peores']):.1f} |")
    lineas += ["", "Espera media por nivel de prioridad (min):", "",
               "| Estrategia | alta | media | baja |", "|---|---|---|---|"]
    for nombre, r in res.items():
        m = r["por_nivel"]
        lineas.append(f"| {nombre} | {_media(m[ALTA]):.1f} | "
                      f"{_media(m[MEDIA]):.1f} | {_media(m[BAJA]):.1f} |")
    return "\n".join(lineas)


if __name__ == "__main__":
    n = len(generar_trabajos(0))
    print(f"{JORNADAS} jornadas de {JORNADA:.0f} min (~{n} trabajos por jornada), "
          f"paso de envejecimiento = {PASO_ENVEJECIMIENTO:.0f} min\n")
    print(tabla(experimento()))
