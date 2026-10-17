# Código base — Semana 08
# Fuente: 02-Momento-2-Disciplina-y-jerarquia/08-Semana-08-Pilas/02-guia-de-laboratorio.html

def factorial_recursivo(n):
    if n <= 1:
        return 1
    return n * factorial_recursivo(n - 1)


def factorial_con_pila(n):
    """La misma cosa, con la pila a la vista."""
    from pila import PilaEnlazada
    pila = PilaEnlazada()
    while n > 1:
        pila.push(n)
        n -= 1
    resultado = 1
    while not pila.esta_vacia():
        resultado *= pila.pop()
    return resultado


# Comprueba que dan lo mismo
for n in range(1, 10):
    assert factorial_recursivo(n) == factorial_con_pila(n)

# Y ahora prueba esto:
import sys
print("Límite de recursión de Python:", sys.getrecursionlimit())
# factorial_recursivo(10000)    # descomenta: RecursionError
print(factorial_con_pila(10000) > 0)   # esto sí funciona

# Pregunta para la bitácora: ¿por qué la versión con pila explícita
# no tiene límite y la recursiva sí?
