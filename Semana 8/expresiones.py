# Código base — Semana 08
# Fuente: 02-Momento-2-Disciplina-y-jerarquia/08-Semana-08-Pilas/02-guia-de-laboratorio.html

from pila import PilaEnlazada

OPERADORES = {"+", "-", "*", "/"}


def evaluar_postfija(expresion):
    """Evalúa una expresión en notación postfija.

    Ejemplos:
        "3 4 +"          -> 7
        "5 1 2 + 4 * +"  -> 14      es 5 + ((1+2) * 4)
        "10 2 /"         -> 5.0

    ¡CUIDADO CON EL ORDEN! Al hacer pop obtienes primero el operando
    DERECHO. Si lo inviertes, la suma y la multiplicación siguen dando
    bien pero la resta y la división quedan al revés.

    Complejidad: O(n)
    """
    pila = PilaEnlazada()
    for token in expresion.split():
        if token in OPERADORES:
            derecho = pila.pop()      # ¡el primero que sale es el derecho!
            izquierdo = pila.pop()
            pass                      # aplica el operador y hace push del resultado
        else:
            pila.push(float(token))
    return pila.pop()


def infija_a_postfija(expresion):
    """Convierte de infija a postfija (shunting-yard simplificado).

    Ejemplo: "3 + 4 * 2"  ->  "3 4 2 * +"

    Reglas:
      - Un número va directo a la salida.
      - Un operador: mientras el tope de la pila tenga precedencia MAYOR
        o IGUAL, sácalo a la salida. Después haz push del nuevo.
      - "(" se apila siempre.
      - ")" saca todo hasta encontrar "(" y descarta el paréntesis.
      - Al final, vacía la pila a la salida.
    """
    PRECEDENCIA = {"+": 1, "-": 1, "*": 2, "/": 2}
    salida = []
    pila = PilaEnlazada()
    pass
    return " ".join(salida)


# --- pruebas ---
def test_evaluar_postfija():
    assert evaluar_postfija("3 4 +") == 7
    assert evaluar_postfija("5 1 2 + 4 * +") == 14
    assert evaluar_postfija("10 3 -") == 7      # detecta el orden invertido
    assert evaluar_postfija("10 2 /") == 5


def test_conversion():
    assert infija_a_postfija("3 + 4") == "3 4 +"
    assert infija_a_postfija("3 + 4 * 2") == "3 4 2 * +"
    assert infija_a_postfija("( 3 + 4 ) * 2") == "3 4 + 2 *"
