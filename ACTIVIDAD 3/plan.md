# Plan — Actividad 3: La lista de reproducción


## Estructura de datos elegida para `ListaEnlazada`

- **Nodo** (`nodo.py`): objeto simple con `dato` y `siguiente`. Sin
  lógica propia de lista — su única responsabilidad es guardar un valor
  y una referencia al siguiente eslabón.
- **ListaEnlazada** (`lista_enlazada.py`): mantiene `_cabeza`, `_cola` y
  `_tamaño` como estado propio. El puntero `_cola` es la decisión de
  diseño clave: sin él, insertar al final sería O(n) (habría que
  recorrer toda la cadena); con él, es O(1). Esto se documenta en la
  tabla de complejidad, no como detalle interno sino como parte de la
  decisión de diseño (cumple la advertencia de "Si te atascas").

Justificación contra RNF-01 (constitución, principio 2): no hay ningún
`list`/`dict`/`set` interno en `ListaEnlazada`; el único "arreglo
subyacente" con soporte interno de Python vive en `ListaArreglo`
(`_datos`), que es la estructura donde sí está permitido por el enunciado
original de la actividad 4.

## División de casos en `insertar` y `eliminar`

Para evitar condicionales anidados confusos, cada operación se separa en
sub-casos con su propio método privado:

| Método público | Sub-casos                              | Complejidad |
|-----------------|-----------------------------------------|-------------|
| `insertar`      | `_insertar_al_inicio`, `_insertar_al_final`, `_insertar_en_medio` | O(1), O(1), O(n) |
| `eliminar`       | `_eliminar_primero`, `_eliminar_no_primero`                        | O(1), O(n)        |

El orden de reasignación de punteros dentro de `_insertar_en_medio` y
`_eliminar_no_primero` sigue el principio 5 de la constitución: primero
se conecta el nodo nuevo (o se guarda el nodo objetivo), y solo después
se reengancha el nodo anterior. Ese orden está explicado con diagramas en
`nodos_a_mano.md`.

## Estrategia de pruebas

1. **Contrato heredado** (`test_lista.py`): parametrizado sobre
   `IMPLEMENTACIONES = [ListaArreglo, ListaEnlazada]`, corre las mismas
   pruebas contra ambas clases. No se toca al agregar `ListaEnlazada`
   (RNF-02): si el contrato estaba bien escrito en la actividad 2, pasa
   solo.
2. **Casos extremos** (`test_extremos.py` / `test_casos_extremos.py`):
   pruebas específicas de `ListaEnlazada` que inspeccionan directamente
   `_cabeza` y `_cola` para verificar las invariantes IR-01/IR-02 tras
   los cuatro casos límite.
3. **Medición de rendimiento** (`benchmark.py`): no es una prueba de
   corrección, es un experimento de medición reproducible con semilla
   fija (`random.seed(42)`), 300 repeticiones por operación, y
   reconstrucción de la lista antes de cada repetición para no
   contaminar mediciones sucesivas.

## Plan de medición para la decisión (RF-05, RF-06)

1. Medir el costo promedio de cada una de las 4 operaciones sobre listas
   de 5.000 elementos, en ambas estructuras.
2. Multiplicar cada costo promedio por su frecuencia diaria real y sumar,
   para obtener el costo total de un día de emisión por estructura.
3. Comparar los dos totales y recomendar el menor.
4. Despejar, en función de la frecuencia de la operación más
   determinante, el valor donde ambos totales se igualan (punto de
   equilibrio), para poder decir qué cambio en las frecuencias invierte
   la recomendación.

## Riesgos y mitigaciones

- **Riesgo**: mediciones ruidosas por el estado de la máquina.
  **Mitigación**: 300 repeticiones y reporte de desviación estándar en
  `benchmark.py`, no solo el promedio.
- **Riesgo**: confundir "borrar la canción actual" con "borrar el
  primero" o "el último", sesgando la medición a favor de una estructura.
  **Mitigación**: se define explícitamente en `comparacion.md` que se
  mide en una posición aleatoria, no en un extremo.
