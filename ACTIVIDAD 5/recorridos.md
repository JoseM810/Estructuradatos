# Parte D — Cola vs. pila sobre el mismo árbol

## Árbol de prueba

```
Servidor
├── Ingenieria
│   ├── Sistemas
│   │   ├── EstructurasDatos
│   │   │   ├── 2026-1 (12)
│   │   │   └── 2026-2 (10)
│   │   │       └── ProyectoFinal (8)
│   │   └── BasesDatos
│   │       └── 2026-1B (15)
│   └── Civil
│       └── Estatica
│           └── 2025-2 (9)
└── Derecho
    └── DerechoPenal1
        └── 2026-2D (7)
```


## Salida con cola (por niveles)

```
nivel 1: Servidor
nivel 2: Ingenieria, Derecho
nivel 3: Sistemas, Civil, DerechoPenal1
nivel 4: EstructurasDatos, BasesDatos, Estatica, 2026-2D
nivel 5: 2026-1, 2026-2, 2026-1B, 2025-2
nivel 6: ProyectoFinal
```

## Salida con pila (mismo código, cambiando la cola por una pila)

```
Servidor, Derecho, DerechoPenal1, 2026-2D, Ingenieria, Civil, Estatica,
2025-2, Sistemas, BasesDatos, 2026-1B, EstructurasDatos, 2026-2, ProyectoFinal, 2026-1
```

## Por qué difieren

Los dos algoritmos hacen lo mismo: sacar un nodo, visitarlo y meter sus hijos.
Lo único que cambia es *cuál nodo sale primero*.

- **Cola (FIFO):** sale el que lleva más tiempo esperando. Los hijos de la raíz
  entran antes que los nietos, así que todo el nivel k sale antes que cualquiera
  del nivel k+1. Eso es exactamente "por niveles".
- **Pila (LIFO):** sale el último que entró, o sea el hijo más reciente.
  El algoritmo se hunde por una rama hasta una hoja antes de volver a las otras:
  es un recorrido en profundidad (preorden, con los hermanos en orden inverso
  porque el último hijo apilado es el primero en salir). Por eso `Derecho`
  aparece antes que `Ingenieria` y `2026-1` sale al final.

La pila visita los mismos 15 nodos, pero mezcla niveles: el nivel 5 (`2025-2`)
sale antes que el nivel 3 (`Sistemas`). La causa es solo la política de salida
de la estructura de datos.
