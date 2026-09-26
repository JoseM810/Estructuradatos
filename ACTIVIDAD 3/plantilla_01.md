# Arreglo frente a lista enlazada

### Tabla de complejidad
| Operación          | ListaArreglo | ListaEnlazada | ¿Quién gana? |
|--------------------|--------------|---------------|--------------|
| obtener(i)         | O(1)         | O(n)          | Arreglo      |
| insertar al inicio | O(n)         | O(1)          | Enlazada     |
| insertar al final  | O(1) amort.  | O(1)          | Empate       |
| insertar en medio  | O(n)         | O(n)          | Empate: ambas deben llegar a la posición (arreglo desplazando, enlazada recorriendo); ninguna tiene ventaja estructural aquí |
| eliminar al inicio | O(n)         | O(1)          | Enlazada     |
| eliminar al final  | O(1)         | O(n)          | Arreglo      |
| buscar             | O(n)         | O(n)          | Empate       |
| memoria por elem.  | 1 referencia (solo el dato, dentro del arreglo contiguo) | 2 referencias (el dato + el puntero `siguiente` de cada nodo) | Arreglo |

### ¿Cuál usaría para...?

1. Un historial de navegación donde solo agregas y quitas del final:
   `ListaArreglo` — ambas operaciones de punta final son O(1)/O(1)
   amortizado, y de paso se gana acceso directo por índice si luego se
   necesita mostrar los últimos N sitios visitados.
2. Una cola de impresión donde agregas al final y quitas del inicio:
   `ListaEnlazada` — con puntero a cola, agregar al final es O(1); quitar
   del inicio también es O(1) gracias a `_eliminar_primero`. En el
   arreglo, quitar del inicio es O(n).
3. Un catálogo que se consulta mucho por índice y casi nunca cambia:
   `ListaArreglo` — `obtener(i)` es O(1) y ese es el uso dominante; en
   la enlazada cada consulta sería O(n).
4. Una lista de tareas donde insertas prioridades al principio:
   `ListaEnlazada` — insertar al inicio es O(1) contra O(n) del arreglo,
   exactamente el patrón medido arriba.

## Conclusión

No hay ganador absoluto. `ListaArreglo` es imbatible cuando domina el
acceso por índice o las operaciones en la punta final; `ListaEnlazada`
es imbatible cuando domina insertar/eliminar al inicio. El criterio para
elegir es identificar cuál operación ocurre con más frecuencia en el uso
real del sistema y comparar el costo medido de esa operación específica
en cada estructura — como se detalla con datos reales en
`comparacion.md`.
