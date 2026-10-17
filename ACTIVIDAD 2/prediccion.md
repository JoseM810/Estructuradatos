# Predicción de complejidad


Notación: `n` = tamaño de la lista. Una "operación" es una comparación, una
lectura o una asignación sobre el arreglo (cada una cuesta tiempo constante).

## 1. `obtener(pos)` — O(1)

- Validación: 2 comparaciones (`0 <= pos <= limite`).
- Acceso: 1 lectura `_datos[pos]`.
- Total: 3 operaciones, **sin importar n** → T(n) = 3 → **O(1)**.
- Sale de que el arreglo es memoria contigua: la dirección se calcula con
  `base + pos * tamaño_celda`, sin recorrer nada.

## 2. `insertar(pos, x)` — O(n) en el peor caso, O(1) amortizado al final

El bucle desplaza `n - pos` elementos (1 lectura + 1 escritura cada uno).

- **Al inicio (`pos = 0`):** n desplazamientos → T(n) ≈ n + c → **O(n)**.
- **En el medio:** n/2 desplazamientos → O(n).
- **Al final (`pos = n`):** 0 desplazamientos + 1 escritura → O(1), salvo
  cuando el arreglo está lleno y hay que redimensionar (copiar n elementos).
  Con duplicación de capacidad las copias totales para n inserciones son
  4 + 8 + 16 + … + n < 2n, es decir menos de 2 copias por inserción:
  **O(1) amortizado**.

## 3. `insertar_ordenado(x)` — O(n)

- Ubicar la posición con búsqueda binaria: ⌊log₂ n⌋ + 1 iteraciones, cada una
  con ~2 operaciones → O(log n).
- Desplazar con `insertar`: n − pos elementos. Si la posición es uniforme
  entre 0 y n, el promedio es n/2; el peor caso es n.
- T(n) ≈ 2·log₂ n + n/2 (promedio) → **O(n)**. El desplazamiento domina:
  para n = 80.000 son ≈ 17 iteraciones frente a ≈ 40.000 desplazamientos.

## 4. `buscar_lineal(x)` — O(n)

- Mejor caso: 1 comparación (está en la posición 0).
- Promedio (está, posición uniforme): ≈ n/2 comparaciones.
- Peor caso (ausente o al final): n comparaciones.
- **O(n)**: se recorre el arreglo una posición a la vez.

## 5. `buscar_binaria(x)` — O(log n)

- Cada iteración descarta la mitad del intervalo: n → n/2 → n/4 → … → 1.
- Número de iteraciones en el peor caso: ⌊log₂ n⌋ + 1.
- Requiere lista ordenada. **O(log n)**.

## Operaciones contadas por tamaño (predicción)

| n | log₂ n (iter. binaria) | buscar_lineal peor | buscar_lineal promedio | desplazamientos insertar inicio | desplazamientos insertar_ordenado (prom.) |
|---:|---:|---:|---:|---:|---:|
| 1.000 | 10 | 1.000 | 500 | 1.000 | 500 |
| 10.000 | 14 | 10.000 | 5.000 | 10.000 | 5.000 |
| 80.000 | 17 | 80.000 | 40.000 | 80.000 | 40.000 |
| 200.000 | 18 | 200.000 | 100.000 | 200.000 | 100.000 |

## Forma esperada de las curvas

Al **duplicar n**:

| Operación | Esperado al duplicar n |
|---|---|
| `obtener` | ×1 (no cambia) |
| `insertar` al final | ×1 (no cambia, amortizado) |
| `buscar_binaria` | + 1 iteración (≈ ×1,05 a ×1,1: casi plana) |
| `insertar` al inicio | ×2 |
| `insertar_ordenado` | ×2 (casi) |
| `buscar_lineal` | ×2 |

De n = 1.000 a n = 200.000 (×200): las operaciones O(n) deberían crecer
≈ ×200; `buscar_binaria`, ≈ ×1,8 (de 10 a 18 iteraciones); las O(1), ≈ ×1.

## Predicción para la decisión

Costo de 50 búsquedas + 1 inserción:

- **Desordenado:** 50 · buscar_lineal(n) + insertar_final(n) ≈ 50 · n/2 + 1
  = 25·n operaciones.
- **Ordenado:** 50 · buscar_binaria(n) + insertar_ordenado(n) ≈ 50 · log₂ n +
  n/2 operaciones.

Para n = 80.000: ≈ 2.000.000 frente a ≈ 40.900 operaciones, o sea unas 50
veces menos con el catálogo ordenado.

 **Predicción: ordenar empieza a ser ventajoso cuando se realizan más de una búsqueda por cada inserción**, ya que el ahorro en búsquedas compensa el costo adicional de ordenar. En la práctica, como la proporción real de búsquedas frente a inserciones suele ser bastante mayor (por ejemplo, alrededor de 5 incluso en épocas de baja actividad), ordenar siempre resulta beneficioso. Además, este equilibrio apenas depende del tamaño del conjunto, porque los costos crecen de manera similar, y solo pequeñas diferencias en las constantes —como si comparar es más barato que desplazar— pueden mover el punto ligeramente por encima o por debajo de 1.