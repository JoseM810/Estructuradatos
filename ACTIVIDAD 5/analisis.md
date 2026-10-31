# Parte B — Simulación y análisis

Ejecutar: `python simulacion.py`. Los supuestos (un técnico, jornada de 480 min,
llegadas de Poisson cada 5 min en promedio, servicio medio de 4,5 min, mezcla
20 % alta / 30 % media / 50 % baja, 300 jornadas con los mismos trabajos para
todas las estrategias) están en la cabecera de `simulacion.py`.

## Resultados (300 jornadas, ~99 trabajos por jornada, paso de envejecimiento = 15 min)

| Estrategia | Espera media (min) | Peor espera, promedio por jornada (min) | Peor espera de todas las jornadas (min) |
|---|---|---|---|
| Orden de llegada (FIFO) | 21.1 | 55.3 | 150.6 |
| Prioridad con envejecimiento | 21.2 | 63.2 | 158.5 |
| Prioridad SIN envejecimiento (control) | 21.1 | 90.6 | 288.4 |

Espera media por nivel de prioridad (min):

| Estrategia | alta | media | baja |
|---|---|---|---|
| Orden de llegada (FIFO) | 20.6 | 21.3 | 21.3 |
| Prioridad con envejecimiento | 11.0 | 18.4 | 27.0 |
| Prioridad SIN envejecimiento (control) | 4.6 | 8.0 | 35.9 |

## Interpretación

1. **La media no distingue las estrategias (≈21 min en las tres).** No es
   casualidad: hay un solo técnico que nunca se queda quieto mientras haya
   cola, así que el trabajo total pendiente es el mismo con cualquier orden.
   Cambiar el orden no hace que se espere menos en total; solo **reparte la
   espera de otra forma**. Quedarse con la media sería concluir que dan igual.
2. **La prioridad sí cambia quién espera.** A los de prioridad alta los atiende
   en 11 min (con envejecimiento) o 4,6 min (sin él), contra 20,6 min en FIFO.
   Ese beneficio se paga con los de prioridad baja (27,0 y 35,9 min).
3. **El peor caso es donde la prioridad sale peor.** Sin envejecimiento, la
   peor espera es 90,6 min en promedio por jornada y llega a 288,4 min, casi el
   doble que FIFO (150,6): un trabajo bajo puede quedar rezagado mientras siguen
   llegando trabajos de más prioridad.
4. **El envejecimiento acota ese daño.** Con paso de 15 min, el peor caso baja
   de 90,6 a 63,2 min (promedio) y de 288,4 a 158,5 min (absoluto), cerca de
   FIFO (55,3 y 150,6), conservando casi todo el beneficio para los de
   prioridad alta (11,0 min frente a 20,6 de FIFO). Queda un costo residual
   (63,2 contra 55,3): es el precio de dar preferencia.
5. **Decisión:** si a la sala le importa que lo urgente se atienda rápido y
   que nadie espere sin límite, conviene prioridad con envejecimiento. Si todos
   los trabajos valen lo mismo, FIFO es más simple y tiene el mejor peor caso.
   El paso (15 min) es una perilla: más pequeño acerca el comportamiento a
   FIFO, más grande a la prioridad pura.

## Verificación

`test_simulacion.py` comprueba a mano casos de 3 trabajos (esperas 0, 4 y 8 en
FIFO; el ALTA que adelanta a un BAJA en prioridad) y que todas las estrategias
atienden todos los trabajos. `test_cola_prioridad.py` demuestra la garantía:
un BAJA con ráfaga constante de ALTA nunca sale sin envejecimiento y sale antes
de `2 * paso` minutos con envejecimiento.
