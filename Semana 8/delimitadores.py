# Código base — Semana 08
# Fuente: 02-Momento-2-Disciplina-y-jerarquia/08-Semana-08-Pilas/02-guia-de-laboratorio.html

from pila import PilaEnlazada, PilaVaciaError

PAREJAS = {")": "(", "]": "[", "}": "{"}
APERTURAS = set(PAREJAS.values())


def esta_balanceada(expresion):
    """Devuelve True si los delimitadores están correctamente balanceados.

    Casos que debe manejar:
        "(a + b)"      -> True
        "[(a + b)]"    -> True
        "[(a + b])"    -> False   cierre que no coincide con la apertura
        "((a)"         -> False   queda una apertura sin cerrar
        "a)"           -> False   cierre sin apertura previa
        ""             -> True    vacío está balanceado

    Complejidad: O(n) en tiempo, O(n) en espacio en el peor caso.
    """
    pila = PilaEnlazada()
    for caracter in expresion:
        if caracter in APERTURAS:
            pass    # completa
        elif caracter in PAREJAS:
            pass    # completa: ¿qué comprobaciones necesitas ANTES de hacer pop?
    return pila.esta_vacia()


# --- pruebas ---
def test_balanceo():
    assert esta_balanceada("")
    assert esta_balanceada("(a + b)")
    assert esta_balanceada("[(a + b) * {c - d}]")
    assert not esta_balanceada("[(a + b])")     # cruzados
    assert not esta_balanceada("((a)")          # falta cerrar
    assert not esta_balanceada("a)")            # cierre huérfano
    assert not esta_balanceada("}{")            # orden invertido
