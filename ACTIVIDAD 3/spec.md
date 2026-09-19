# Spec — Actividad 3: La lista de reproducción

## Contexto del caso

Se está construyendo el reproductor de una emisora universitaria. La
lista de reproducción debe soportar cuatro operaciones, cada una con una
frecuencia real medida durante una semana de emisión:

| Operación                | Frecuencia/día |
|--------------------------|---------------:|
| Insertar al principio (canción de última hora) | 40 |
| Recorrer toda la lista (generar la parrilla)    | 3  |
| Ir a la canción número N (saltar en el aire)    | 200|
| Borrar la canción actual (se cayó el derecho de emisión) | 15 |

Ya existe `ListaArreglo` (actividad anterior). Este proyecto agrega
`ListaEnlazada` con el mismo contrato, y responde con datos cuál de las
dos debe usar el reproductor.

## Requisitos funcionales

- **RF-01**: `ListaEnlazada` expone `tamaño()`, `obtener(posicion)`,
  `insertar(posicion, elemento)`, `eliminar(posicion)`, `buscar(elemento)`,
  `__len__`, `__getitem__`, `__iter__`, `__repr__` — el mismo contrato
  público que `ListaArreglo`.
- **RF-02**: `insertar` y `eliminar` deben lanzar `PosicionInvalidaError`
  (subclase de `IndexError`) cuando la posición está fuera de rango, con
  los mismos límites que `ListaArreglo` (`incluir_final` en insertar,
  no incluirlo en eliminar/obtener).
- **RF-03**: la implementación debe mantener en todo momento las
  invariantes IR-01, IR-02 e IR-03 documentadas en `lista_enlazada.py`.
- **RF-04**: se debe documentar, con una cadena de nodos construida a
  mano (sin `ListaEnlazada`), qué ocurre al reasignar un enlace antes de
  guardar la referencia al resto de la cadena.
- **RF-05**: se debe producir una recomendación de estructura (arreglo o
  enlazada) para el reproductor, basada en el costo diario medido con
  las frecuencias reales del caso — no en la complejidad Big O aislada.
- **RF-06**: la recomendación debe venir acompañada de un análisis de
  sensibilidad: qué cambio en las frecuencias invertiría la decisión.

## Requisitos no funcionales

- **RNF-01**: `ListaEnlazada` no debe usar `list`, `dict`, `set`, `deque`
  ni `heapq` de Python como estructura de nodos interna.
- **RNF-02**: el archivo `test_lista.py` (contrato heredado de la
  actividad 2) no se modifica.
- **RNF-03**: las mediciones de rendimiento deben ser reproducibles
  (script versionado, semilla aleatoria fija donde aplique).

## Criterios de aceptación

1. `pytest -v` corre sin fallos sobre `test_lista.py`,
   `test_extremos.py` (`test_casos_extremos.py`) y cualquier prueba
   adicional.
2. Los cuatro casos extremos (lista vacía, lista de un elemento, borrar
   el primero, borrar el último) están probados y pasan.
3. `comparacion.md` presenta costo teórico y medido lado a lado para
   cada operación, el cálculo del costo de un día de emisión con ambas
   estructuras, una recomendación y el punto de equilibrio en
   frecuencias que la invertiría.
4. `nodos_a_mano.md` muestra, con diagramas, la cadena construida a mano
   y explica la pérdida de referencia al reasignar un enlace en el orden
   incorrecto.

## Fuera de alcance

- Persistencia de la lista de reproducción en disco o base de datos.
- Concurrencia (varios hilos modificando la lista al mismo tiempo).
- Estructuras distintas a arreglo dinámico y lista enlazada simple (no
  se evalúan listas doblemente enlazadas ni circulares).
