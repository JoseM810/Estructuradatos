# Parte D — La decisión del reproductor

### 1. Metodología de medición.

Se construyó una lista de **N = 5.000 canciones** con cada estructura
(`ListaArreglo` y `ListaEnlazada`) y se midió, con `time.perf_counter()`,
el costo de una sola llamada a cada una de las cuatro operaciones de la
emisora. Cada medición se repitió **300 veces**, reconstruyendo la lista
desde cero antes de cada repetición (esa reconstrucción no se cronometra),
para evitar que el estado dejado por una medición contaminara la
siguiente. Se reporta el promedio.

Detalles de las operaciones tal como se midieron:

- **Insertar al principio**: `lista.insertar(0, "cancion_urgente")`.
- **Recorrer toda la lista**: iterar con `for _ in lista: pass` sobre las
  5.000 canciones.
- **Ir a la canción número N**: `lista.obtener(i)` con `i` elegido al azar
  en `[0, 4999]` — modela "saltar en el aire" a una canción cualquiera de
  la parrilla, no siempre la misma.
- **Borrar la canción actual**: `lista.eliminar(i)` con `i` elegido al
  azar en `[0, 4999]` — se asume que "la canción actual" puede estar en
  cualquier posición de la parrilla en el momento en que se cae el
  derecho de emisión, no siempre al inicio o al final.


## 2. Tabla resumen: costo teórico y medido.

| Operación                | Teórico Arreglo | Teórico Enlazada | Medido Arreglo (µs) | Medido Enlazada (µs) | ¿Quién gana medido? |
|--------------------------|:---------------:|:-----------------:|---------------------:|-----------------------:|:--------------------:|
| Insertar al principio    | O(n)            | O(1)               | 268.57               | 1.22                    | Enlazada (-447×)      |
| Recorrer toda la lista   | O(n)            | O(n)               | 142.07                | 115.46                  | Enlazada (leve)       |
| Ir a la canción número N | O(1)            | O(n)               | 0.61                  | 42.77                   | Arreglo (~70×)        |
| Borrar la canción actual | O(n)            | O(n)               | 90.87                 | 44.24                   | Enlazada (~2×)        |
| Memoria por elemento     | 1 referencia    | 2 referencias (dato + `siguiente`) | — | — | Arreglo |

Las dos operaciones O(n) en ambas estructuras ("recorrer" y "borrar en
posición aleatoria") no dan tiempos idénticos porque, aunque la cuenta de
pasos crece igual, el trabajo que hace cada paso es distinto: el arreglo
mueve datos en un bloque de memoria contiguo (bueno para el caché de la
CPU, pero copia valores), mientras que la enlazada solo sigue punteros
(salta de nodo en nodo, sin copiar nada, pero con peor localidad de
memoria). En "recorrer" ambos efectos casi se cancelan; en "borrar" gana
la enlazada porque no tiene que desplazar nada, solo reenganchar un
puntero una vez que llega a la posición.

### 3. Costo de un día de emisión con las frecuencias reales.

Frecuencias dadas por el caso:

| Operación                | Frecuencia/día |
|--------------------------|---------------:|
| Insertar al principio    | 40             |
| Recorrer toda la lista   | 3              |
| Ir a la canción número N | 200            |
| Borrar la canción actual | 15             |

Costo diario = Σ (frecuencia × costo medido de esa operación).

**ListaArreglo:**

```
40  × 193.03 µs =  7 721.20 µs
 3  × 142.07 µs =    426.21 µs
200 ×   0.61 µs =    122.09 µs
 15 ×  90.87 µs =  1 363.00 µs
                 ---------------
Total            ≈  9 632.63 µs/día  (≈ 9.63 ms/día)
```

**ListaEnlazada:**

```
40  ×   1.22 µs =     48.76 µs
 3  × 115.46 µs =    346.38 µs
200 ×  42.77 µs =  8 553.39 µs
 15 ×  44.24 µs =    663.59 µs
                 ---------------
Total            ≈  9 612.12 µs/día  (≈ 9.61 ms/día)
```

### 4. Recomendación.

Con las frecuencias reales dadas, **`ListaEnlazada` es la más barata**,
pero por un margen mínimo: **9.612 ms/día contra 9.633 ms/día**, apenas
un **0,21 % más barata**. Para el reproductor de esta emisora, en la
práctica **es un empate técnico**.

Esto no es casualidad de los números: `ListaArreglo` pierde en
"insertar al principio" (40 veces/día a 193 µs cada una) casi
exactamente lo mismo que `ListaEnlazada` pierde en "ir a la canción
número N" (200 veces/día a 42.77 µs cada una). Son las dos operaciones
más frecuentes de la lista, y cada estructura es mala en una de ellas.

### 5. Qué tendría que cambiar en las frecuencias para invertir la recomendación.

Fijando todo lo demás, se despeja el punto de equilibrio en función de
`x` = frecuencia diaria de "ir a la canción número N" (la variable que
más pesa, porque es la operación más frecuente y donde más se
diferencian las dos estructuras):

```
Costo_Arreglo(x)   = 40(193.03) + 3(142.07) + x(0.61)  + 15(90.87)
                    = 9 510.46 + 0.61 x        [µs]

Costo_Enlazada(x)  = 40(1.22)   + 3(115.46)  + x(42.77) + 15(44.24)
                    = 1 058.78 + 42.77 x      [µs]

Costo_Arreglo(x) = Costo_Enlazada(x)
9 510.46 + 0.61x = 1 058.78 + 42.77x
8 451.68 = 42.16x
x ≈ 200.5
```

**Las frecuencias reales dan `x = 200`, prácticamente sobre el punto de
equilibrio (`x ≈ 200.5`).** Esa es la razón por la que la ventaja medida
de la enlazada es de apenas 0,21 %: el caso está construido casi
exactamente en el filo de la decisión.

**Conclusión de sensibilidad:** si la emisora empezara a recibir
solicitudes de la audiencia y la operación "ir a la canción número N" se
usara aunque sea **un poco más de 200 veces al día** (por ejemplo, si
subiera a 210 u 220 veces/día, manteniendo las demás frecuencias
iguales), la recomendación se invertiría y **`ListaArreglo` pasaría a
ser la opción más barata**, porque el costo de la enlazada crece mucho
más rápido con esa operación (42.77 µs por cada punto de `x`, contra
solo 0.61 µs para el arreglo).

En el sentido contrario, si la frecuencia de "insertar al principio"
subiera bastante más allá de 40/día (manteniendo las demás iguales), la
ventaja de la enlazada se ampliaría, porque esa es la operación donde el
arreglo es catastróficamente más lento (193 µs contra 1.22 µs).

### 6. ¿Cuál usaría para...?

1. **Un historial de navegación donde solo agregas y quitas del final:**
   `ListaArreglo`. Insertar y eliminar al final son O(1) amortizado /
   O(1) en el arreglo, y además se aprovecha el acceso directo si alguna
   vez se necesita mostrar los últimos N elementos por índice.
2. **Una cola de impresión donde agregas al final y quitas del inicio:**
   `ListaEnlazada`. Gracias al puntero `_cola`, agregar al final es
   O(1), y quitar del inicio también es O(1) (`_eliminar_primero`). En
   el arreglo, quitar del inicio es O(n) porque hay que recorrer y
   desplazar todo lo demás.
3. **Un catálogo que se consulta mucho por índice y casi nunca cambia:**
   `ListaArreglo`. `obtener(i)` es O(1); en la enlazada sería O(n) cada
   consulta, y aquí las consultas son la operación dominante.
4. **Una lista de tareas donde insertas prioridades al principio:**
   `ListaEnlazada`. Insertar al principio es O(1) contra O(n) del
   arreglo — es exactamente el caso donde la enlazada gana de forma
   aplastante, como se vio en la medición (193 µs contra 1.22 µs).

### 7. Conclusión.

No hay una estructura mejor en abstracto: cada una tiene un perfil de
costo distinto, y ese perfil solo importa en función de **qué tan
seguido** se ejecuta cada operación en el caso de uso real. El criterio
para elegir es identificar la operación más frecuente del sistema y
preguntar cuál estructura la resuelve más barato — como se vio aquí, el
reproductor de la emisora resultó ser un caso límite donde ambas
estructuras cuestan casi lo mismo, porque sus dos operaciones más
frecuentes favorecen, cada una, a una estructura distinta.
