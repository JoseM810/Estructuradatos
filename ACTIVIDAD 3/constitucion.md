# Constitución — Actividad 3: La lista de reproducción

Principios no negociables para este proyecto. Toda decisión de diseño
tomada en `spec.md`, `plan.md` o `task.md` debe poder justificarse contra
estos principios; si algo los contradice, se corrige el código, no la
constitución.

## Principio 1 — El contrato manda, no la implementación

`ListaEnlazada` debe cumplir exactamente el mismo contrato público que
`ListaArreglo` (mismos nombres de método, mismos argumentos, mismas
excepciones ante los mismos errores). El archivo de pruebas de la
actividad anterior (`test_lista.py`) es la fuente de verdad de ese
contrato y **no se modifica** bajo ninguna circunstancia para hacer
pasar la implementación.

## Principio 2 — Nada de estructuras prestadas por dentro

`ListaEnlazada` se construye únicamente con objetos `Nodo` y referencias
explícitas (`siguiente`). Usar `list`, `dict`, `set`, `deque` o `heapq`
de Python como reemplazo de la estructura de nodos —aunque el contrato
externo se vea igual— invalida el ejercicio: el objetivo es entender el
manejo manual de punteros, no delegarlo.

## Principio 3 — Toda afirmación de rendimiento se mide, no se asume

Ninguna recomendación de "usa esta estructura" se acepta solo por
notación Big O. Toda comparación de costos debe estar respaldada por una
medición reproducible (`benchmark.py`) sobre datos de tamaño realista
(N = 5.000 canciones) y con las frecuencias reales del caso, no con
intuiciones generales del tipo "las enlazadas siempre son mejores para
insertar".

## Principio 4 — Los casos extremos son parte del contrato, no un extra

Lista vacía, lista de un elemento, borrar el primero y borrar el último
deben estar probados explícitamente y deben pasar. Un envío que solo
pasa el caso general y falla en algún extremo se considera incompleto,
no "casi listo".

## Principio 5 — El orden de las operaciones sobre punteros se documenta

Cualquier método que reasigne más de una referencia (`siguiente`,
`_cabeza`, `_cola`) debe dejar explícito, en comentario o en
`nodos_a_mano.md`, por qué se reasigna en ese orden y qué se rompería si
se invirtiera. Una reasignación de puntero sin justificación del orden
no se considera terminada.

## Principio 6 — Trazabilidad entre spec, plan, tareas y código

Cada entregable de código debe poder rastrearse a una tarea de
`task.md`, cada tarea a una sección de `plan.md`, y cada sección de
`plan.md` a un requisito de `spec.md`. Si un archivo entregado no
responde a ninguna tarea, no debería existir.
