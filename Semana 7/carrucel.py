class Nodo:

    def __init__(self, dato, anterior=None, siguiente=None):
        self.dato = dato
        self.anterior = anterior
        self.siguiente = siguiente

class Carrucel:

    def __init__(self):
        self.cabeza = None
        self.cola = None
        self.actual = None

    def insertar_incio (self, dato):
        nuevo = Nodo(dato)

        if self.cabeza is None:
            self.cabeza = nuevo
            self.cola = nuevo
            self.actual = nuevo
        else:
            nuevo.siguiente = self.cabeza
            self.cabeza = nuevo
            self.cola.siguiente = self.cabeza

    def insertar_final (self, dato):
        nuevo= Nodo(dato)

        if self.cabeza is None:
            self.cabeza = nuevo
            self.cola = nuevo
            self.actual = nuevo
        else:
            self.cola.siguiente = nuevo
            self.cola = nuevo
            self.cola.siguiente = self.cabeza

    def siguiente_imagen(self):
        if self.actual:
            self.actual = self.actual.siguiente
            print(f"Mostrando: {self.actual.dato}")

    def mostrar_actual(self):
        if self.actual:
            print(f"Mostrando: {self.actual.dato}")
        else:
            print("El carrucel está vacío.")


ca=Carrucel()
    
ca.insertar_final("foto1.jpg")
ca.insertar_final("foto2.jpg")
ca.insertar_final("foto3.jpg")
ca.insertar_inicio("foto0.jpg")

ca.mostrar_actual()
ca.siguiente_imagen()
ca.siguiente_imagen()