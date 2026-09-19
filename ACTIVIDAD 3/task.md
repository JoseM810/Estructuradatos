# Task — Actividad 3: La lista de reproducción


| ID    | Tarea                                                                 | Sección de plan.md                    | Requisito(s) | Archivo(s)                          | Estado |
|-------|------------------------------------------------------------------------|-----------------------------------------|--------------|--------------------------------------|--------|
| T-01  | Construir cadena de 3 nodos a mano y recorrerla con un bucle           | (Parte A, previa al plan de código)     | RF-04        | `nodo.py`, `nodos_a_mano.md`         | Hecho  |
| T-02  | Documentar con diagramas el efecto de reasignar un enlace antes de guardar el siguiente | (Parte A) | RF-04        | `nodos_a_mano.md`                    | Hecho  |
| T-03  | Completar `ListaArreglo` (contrato heredado de la actividad 2)         | Estructura de datos elegida             | RF-01        | `lista_arreglo.py`                   | Hecho  |
| T-04  | Implementar `_insertar_en_medio` en `ListaEnlazada`                    | División de casos en insertar/eliminar  | RF-01, RF-03 | `lista_enlazada.py`                  | Hecho  |
| T-05  | Implementar `_eliminar_no_primero` en `ListaEnlazada`, actualizando `_cola` cuando corresponde | División de casos en insertar/eliminar | RF-01, RF-03 | `lista_enlazada.py` | Hecho |
| T-06  | Construir el contrato de pruebas heredado (`test_lista.py`) parametrizado sobre ambas implementaciones | Estrategia de pruebas, punto 1 | RF-02, RNF-02 | `test_lista.py` | Hecho |
| T-07  | Verificar los cuatro casos extremos (vacía, un elemento, borrar primero, borrar último) | Estrategia de pruebas, punto 2 | RF-03 |  `test_casos_extremos.py` | Hecho — 6/6 pruebas pasan |
| T-08  | Escribir `benchmark.py`: medir las 4 operaciones en ambas estructuras con N=5.000 | Plan de medición, punto 1 | RF-05, RNF-03 | `benchmark.py` | Hecho |
| T-09  | Calcular el costo de un día de emisión con las frecuencias reales, en ambas estructuras | Plan de medición, punto 2-3 | RF-05 | `comparacion.md` | Hecho |
| T-10  | Calcular el punto de equilibrio en frecuencias y la recomendación final | Plan de medición, punto 4 | RF-06 | `comparacion.md` | Hecho |
| T-11  | Completar tabla de complejidad (`plantilla_01.md`) | — | RF-05 | `plantilla_01.md` | Hecho |
| T-12  | Correr `pytest -v` completo y verificar 0 fallos antes de entregar     | Criterios de aceptación 1              | RNF-02       | (verificación, sin archivo nuevo)    | Hecho — 44 + 6 = 50 pruebas, 0 fallos |


