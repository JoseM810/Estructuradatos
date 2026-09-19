# Parte D — La decisión del reproductor

## 1. Metodología de medición

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

El script completo está en `benchmark.py`. Estos resultados se obtuvieron
ejecutando `python benchmark.py` en el equipo del estudiante.

## 2. Tabla resumen: costo teórico y medido, lado a lado

| Operación                | Teórico Arreglo | Teórico Enlazada | Medido Arreglo (µs) | Medido Enlazada (µs) | ¿Quién gana medido? |
|--------------------------|:---------------:|:-----------------:|---------------------:|-----------------------:|:--------------------:|
| Insertar al principio    | O(n)            | O(1)               | 268.57                | 0.60                    | Enlazada (~447×)      |
| Recorrer toda la lista   | O(n)            | O(n)               | 190.04                | 150.44                  | Enlazada (leve)       |
| Ir a la canción número N | O(1)            | O(n)               | 0.31                  | 50.44                   | Arreglo (~163×)       |
| Borrar la canción actual | O(n)            | O(n)               | 135.67                | 47.47                   | Enlazada (~2.9×)      |
| Memoria por elemento     | 1 referencia    | 2 referencias (dato + `siguiente`) | — | — | Arreglo |



Las dos operaciones O(n) en ambas estructuras ("recorrer" y "borrar en
posición aleatoria") no dan tiempos idénticos porque, aunque la cuenta de
pasos crece igual, el trabajo que hace cada paso es distinto: el arreglo
mueve datos en un bloque de memoria contiguo (bueno para el caché de la
CPU, pero copia valores), mientras que la enlazada solo sigue punteros
(salta de nodo en nodo, sin copiar nada, pero con peor localidad de
memoria). En "borrar" gana la enlazada porque no tiene que desplazar
nada, solo reenganchar un puntero una vez que llega a la posición.

## 3. Costo de un día de emisión con las frecuencias reales

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
40  × 268.57 µs = 10 742.80 µs
 3  × 190.04 µs =    570.12 µs
200 ×   0.31 µs =     62.00 µs
 15 × 135.67 µs =  2 035.05 µs
                 ---------------
Total            ≈ 13 409.97 µs/día  (≈ 13.41 ms/día)
```

**ListaEnlazada:**

```
40  ×   0.60 µs =     24.00 µs
 3  × 150.44 µs =    451.32 µs
200 ×  50.44 µs = 10 088.00 µs
 15 ×  47.47 µs =    712.05 µs
                 ---------------
Total            ≈ 11 275.37 µs/día  (≈ 11.28 ms/día)
```

## 4. Recomendación

Con las frecuencias reales dadas y las mediciones tomadas en este
equipo, **`ListaEnlazada` es la más barata**: **11 275.37 µs/día contra
13 409.97 µs/día**, es decir, **~15.9 % más barata** que el arreglo.

El resultado se explica igual que con cualquier otra máquina: cada
estructura es mala en la operación más frecuente de la otra.
`ListaArreglo` pierde fuerte en "insertar al principio" (40 veces/día a
268.57 µs cada una = 10 742.80 µs, el 80 % de su costo total), mientras
que `ListaEnlazada` pierde fuerte en "ir a la canción número N" (200
veces/día a 50.44 µs cada una = 10 088.00 µs, el 89 % de su costo
total). En este equipo, la pérdida del arreglo termina pesando un poco
más que la de la enlazada, por eso la enlazada gana con más margen que
en otras máquinas donde el resultado puede salir más parejo.

## 5. Qué tendría que cambiar en las frecuencias para invertir la recomendación

Fijando todo lo demás, se despeja el punto de equilibrio en función de
`x` = frecuencia diaria de "ir a la canción número N" (la variable que
más pesa, porque es la operación más frecuente y donde más se
diferencian las dos estructuras):

```
Costo_Arreglo(x)   = 40(268.57) + 3(190.04) + x(0.31)  + 15(135.67)
                    = 13 347.97 + 0.31 x       [µs]

Costo_Enlazada(x)  = 40(0.60)   + 3(150.44)  + x(50.44) + 15(47.47)
                    = 1 187.37 + 50.44 x      [µs]

Costo_Arreglo(x) = Costo_Enlazada(x)
13 347.97 + 0.31x = 1 187.37 + 50.44x
12 160.60 = 50.13x
x ≈ 242.6
```

**Las frecuencias reales dan `x = 200`, por debajo del punto de
equilibrio de este equipo (`x ≈ 242.6`).** Por eso la recomendación es
`ListaEnlazada`: hace falta que la operación "ir a la canción número N"
se pida bastante más seguido (de 200 a más de 243 veces al día,
manteniendo las demás frecuencias iguales) para que la balanza se
invierta y `ListaArreglo` pase a ser la opción más barata en este
equipo.

En el sentido contrario, si la frecuencia de "insertar al principio"
subiera bastante más allá de 40/día (manteniendo las demás iguales), la
ventaja de la enlazada se ampliaría todavía más, porque esa es la
operación donde el arreglo es catastróficamente más lento (268.57 µs
contra 0.60 µs).

**Nota sobre reproducibilidad**: estos números de equilibrio (`x ≈
242.6`) son específicos de la máquina donde se midió. En otro equipo,
con otra velocidad de procesador y otra carga de trabajo en segundo
plano, los tiempos absolutos cambian y por lo tanto el punto de
equilibrio también se mueve un poco — pero la estructura del argumento
(despejar `x` igualando ambos costos) es la misma sin importar la
máquina.

## 6. ¿Cuál usarías para...?

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
   aplastante, como se vio en la medición (268.57 µs contra 0.60 µs).

## 7. Conclusión general

No hay una estructura mejor en abstracto: cada una tiene un perfil de
costo distinto, y ese perfil solo importa en función de **qué tan
seguido** se ejecuta cada operación en el caso de uso real. El criterio
para elegir es identificar la operación más frecuente del sistema y
preguntar cuál estructura la resuelve más barato. Para mi con
las frecuencias reales del caso, `ListaEnlazada` resultó ser la opción
más barata por un margen razonablemente claro (~15.9 %), porque el
costo de insertar al principio en el arreglo (que ocurre 40 veces al
día) pesa un poco más que el costo de ir a la canción N en la enlazada
(que ocurre 200 veces al día), aunque ambas estructuras están cerca de
su punto de equilibrio, a solo ~43 consultas de diferencia.
