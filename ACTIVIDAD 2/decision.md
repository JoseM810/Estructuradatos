# Decisión: ¿conviene mantener ordenado el catálogo? (Parte D)

Todas las cifras salen de `resultados.csv` (mediana de 7 mediciones con
`timeit`, ejecutadas en mi PC con Windows; script `decision_calculo.py`).

## 1. Mediciones usadas (mediana, µs por llamada)

| Operación | n = 1.000 | n = 10.000 | n = 80.000 | n = 200.000 |
|---|---:|---:|---:|---:|
| obtener | 0,293 | 0,340 | 0,336 | 0,239 |
| insertar al final | 1,273 | 1,278 | 0,849 | 1,431 |
| buscar_binaria (ausente = peor caso) | 1,580 | 2,317 | 2,858 | 2,506 |
| insertar al inicio | 74,0 | 1.097,7 | 6.693,9 | 17.989,5 |
| insertar_ordenado (posición media) | 44,2 | 586,7 | 3.554,6 | 7.966,7 |
| buscar_lineal (ausente = peor caso) | 76,2 | 663,3 | 5.384,9 | 12.240,3 |
| buscar_lineal (presente, hacia la mitad = caso promedio) | 26,8 | 358,7 | 2.803,2 | 5.986,7 |

### Predicción vs. medición (Parte C)

- **O(n)** (`insertar` al inicio, `insertar_ordenado`, `buscar_lineal`): entre
  n = 1.000 y n = 200.000 (×200) el tiempo crece ×243, ×180, ×161 y ×223.
  La predicción era ×200: la forma coincide (en las gráficas son rectas),
  aunque la constante varía ±20 % entre operaciones. Entre 10.000 y 80.000
  (×8) `insertar` al inicio pasa de 1.097,7 a 6.693,9 µs (×6,1) y entre
  80.000 y 200.000 (×2,5) pasa de 6.693,9 a 17.989,5 µs (×2,7). Como no
  hay una tendencia sistemática, atribuyo esa dispersión al ruido del
  sistema operativo y de la caché del procesador, no a un error de la
  complejidad.
- **O(1)** (`obtener`, `insertar` al final): sin tendencia creciente.
  `obtener` oscila entre 0,24 y 0,34 µs; `insertar_final`, entre 0,85 y
  1,43 µs. Esa variación no sigue a n (el valor menor está en 80.000 y el
  mayor en 200.000), por lo que es ruido.
- **O(log n)** (`buscar_binaria`): sube de 1,58 a 2,86 µs al pasar de 1.000 a
  80.000 registros (×1,8; la predicción por iteraciones era ×1,7, de 10 a
  17), y baja a 2,51 µs con 200.000. Ese último descenso contradice el
  modelo y lo explico con ruido: son valores de microsegundos medidos
  sobre el costo fijo de cada llamada. Aun así es dos órdenes de magnitud
  menor que `buscar_lineal`, que es lo que importa.
- **Donde no coincidió mi predicción:** el punto de equilibrio (ver §3).
  Predije k ≈ 1 asumiendo que desplazar un elemento y comparar un elemento
  costaban lo mismo. En mi PC desplazar cuesta ≈ 84 ns por elemento
  (6.693,9 µs / 80.000) y comparar ≈ 67 ns (5.384,9 µs / 80.000), es decir
  desplazar es ≈ 1,24 veces más caro (con n = 200.000, ≈ 90 ns frente a
  ≈ 61 ns, un 1,47). Desplazar hace una lectura y una escritura con dos
  índices; comparar hace una lectura y una comparación.

## 2. Costo total de 50 búsquedas + 1 inserción

Desordenado = 50 · buscar_lineal + insertar al final.
Ordenado = 50 · buscar_binaria + insertar_ordenado.
Búsqueda lineal en el caso promedio (el libro está, hacia la mitad); entre
paréntesis el peor caso (libro ausente o al final).

| n | Desordenado | Ordenado | Ordenado es más rápido |
|---:|---:|---:|---:|
| 80.000 | 50 · 2.803,2 µs + 0,85 µs = **140,16 ms** (peor: 269,2 ms) | 50 · 2,858 µs + 3.554,6 µs = **3,70 ms** | **38×** (peor caso: 73×) |
| 200.000 | 50 · 5.986,7 µs + 1,43 µs = **299,34 ms** (peor: 612,0 ms) | 50 · 2,506 µs + 7.966,7 µs = **8,09 ms** | **37×** (peor caso: 76×) |

## 3. Respuesta a la biblioteca

**Sí, conviene mantener el catálogo ordenado.** Con 50 búsquedas por libro
nuevo, el catálogo ordenado resuelve el trabajo en 3,70 ms frente a 140,16 ms
con 80.000 registros (38 veces menos), y en 8,09 ms frente a 299,34 ms con
200.000 registros (37 veces menos). La inserción ordenada es mucho más cara
que insertar al final (3.554,6 µs frente a 0,85 µs con 80.000), pero cada
búsqueda ahorra ≈ 2.800 µs (2.803,2 − 2,86), y con 50 búsquedas ese ahorro
supera ampliamente el sobrecosto.

### ¿Cambia la respuesta según la época del año?

**No. La conclusión es la misma en las tres épocas.**

| Época | Búsquedas por inserción (k) | n = 80.000: desordenado / ordenado | n = 200.000: desordenado / ordenado |
|---|---:|---|---|
| Vacaciones | 5 | 14,02 ms / 3,57 ms (3,9×) | 29,94 ms / 7,98 ms (3,8×) |
| Normal | 50 | 140,16 ms / 3,70 ms (38×) | 299,34 ms / 8,09 ms (37×) |
| Exámenes | 300 | 840,96 ms / 4,41 ms (191×) | 1.796,01 ms / 8,72 ms (206×) |

Lo que cambia con la época es **cuánto** se gana (de 4× a 200×), no **qué
conviene**.

### Punto de equilibrio

Se busca k tal que k · lineal + insertar_final = k · binaria + insertar_ordenado:

    k* = (insertar_ordenado − insertar_final) / (buscar_lineal − buscar_binaria)

- n = 80.000: k* = (3.554,6 − 0,85) / (2.803,2 − 2,86) = **1,27**
- n = 200.000: k* = (7.966,7 − 1,43) / (5.986,7 − 2,51) = **1,33**

**El catálogo ordenado empieza a convenir a partir de ≈ 1,3 búsquedas por
cada libro nuevo** (con un libro promedio hacia la mitad). Si la búsqueda es
siempre de peor caso (libro ausente), el equilibrio baja a k* = 0,66
(80.000) y 0,65 (200.000).

Como el mínimo observado es 5 búsquedas por inserción (vacaciones), la
proporción real está casi 4 veces por encima del punto de equilibrio incluso
en la época más desfavorable. El equilibrio casi no depende de n (1,27
frente a 1,33) porque insertar ordenado y buscar linealmente son ambos
O(n) y su cociente tiende a una constante.

## 4. Salvedades

- Las cifras son de mi máquina y de mi intérprete; en otro equipo los
  valores absolutos cambian, pero las razones (≈ 38×, k* ≈ 1,3) deberían
  mantenerse en orden de magnitud.
- Hay ruido visible en las operaciones de microsegundos (`obtener`,
  `insertar_final`, `buscar_binaria`); no afecta la decisión porque la
  diferencia con las operaciones O(n) es de varios órdenes de magnitud.
- La inserción ordenada se midió en la posición media. Si los libros nuevos
  llegan con códigos crecientes y entran al final, insertar_ordenado cuesta
  O(1) y la ventaja del ordenado sería todavía mayor.
- Ordenar un catálogo ya existente cuesta una sola vez; no se incluyó porque
  la pregunta compara el costo de mantener cada opción libro a libro.
