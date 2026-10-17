def multiplicacion(n, i):
    if i == 0:
        return 0
    return n + multiplicacion (n, i -1)

print(multiplicacion(5,4))

    