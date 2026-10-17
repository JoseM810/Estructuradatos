# Especificación — ADT Pila

## 1. Propósito
Colección con disciplina LIFO: el último elemento agregado es el primero
en salir. No se permite acceder a elementos intermedios.

## 2. Fuera de alcance
- No se puede acceder por índice
- No se puede recorrer sin desmontar la pila
- No se puede insertar en el medio

## 3. Operaciones
### push(elemento)
- Precondiciones: ninguna
- Postcondiciones: `elemento` queda en el tope; tamaño aumenta en 1
- Errores: ninguno

### pop() -> elemento
- Precondiciones: la pila NO está vacía
- Postcondiciones: se devuelve y se quita el elemento del tope;
  tamaño disminuye en 1
- Errores: PilaVaciaError si la precondición no se cumple

### peek() -> elemento
- Precondiciones: la pila NO está vacía
- Postcondiciones: se devuelve el tope SIN modificar la pila
- Errores: PilaVaciaError

### esta_vacia() -> bool
### tamaño() -> entero

## 4. Invariantes
- INV-01: tamaño >= 0
- INV-02: esta_vacia() es verdadero si y solo si tamaño() == 0
- INV-03: si haces push(x) y luego pop(), obtienes x y la pila queda como estaba

## 5. Criterios de aceptación
| ID | Criterio | Prueba |
|----|----------|--------|
| CA-01 | Una pila nueva está vacía | test_pila_nueva_vacia |
| CA-02 | push seguido de pop devuelve el mismo elemento | test_push_pop |
| CA-03 | Los elementos salen en orden inverso al que entraron | test_orden_lifo |
| CA-04 | pop sobre pila vacía lanza PilaVaciaError | test_pop_vacia |
| CA-05 | peek devuelve el tope sin modificar el tamaño | test_peek_no_modifica |
| CA-06 | peek sobre pila vacía lanza PilaVaciaError | test_peek_vacia |