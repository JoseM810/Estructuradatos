class Nodo:

    def __init__(self, dato, anterior=None, siguiente=None):
        self.dato = dato
        self.anterior = anterior
        self.siguiente = siguiente

class ListaEnlazada:
     
     def __init__(self):
         self.cabeza = None
         self.cola = None
         self.actual = None

     def hacer(self, dato):
        nuevo = Nodo(dato)

        if self.actual is not None and self.actual.siguiente is not None:
            self.actual.siguiente = None
            self.cola = self.actual

        if self.cabeza is None:
            self.cabeza = nuevo
            self.cola = nuevo
        else:
            nuevo.anterior = self.actual
            self.cola.siguiente = nuevo
            self.cola = nuevo

        self.actual = nuevo

     def deshacer(self):  

        if self.actual is None:
            print("No hay nada que deshacer")
            return None

        dato = self.actual.dato
        self.actual = self.actual.anterior
        return dato

     def rehacer(self):
         siguiente_nodo = self.cabeza if self.actual is None else self.actual.siguiente

         if siguiente_nodo is None:
             print("No hay nada que rehacer")
             return None

         self.actual = siguiente_nodo
         return self.actual.dato

     def mostrar(self):
        if self.cabeza is None:
            print("La lista está vacía.")
            return
        nodo = self.cabeza
        elementos = []
        while nodo is not None:
            elementos.append(str(nodo.dato))
            nodo = nodo.siguiente
        print (" -> ".join(elementos))


lista = ListaEnlazada()
lista.hacer("primer elemento")
lista.hacer("segundo elemento")
lista.hacer("tercer elemento")
lista.mostrar()

deshecho = lista.deshacer()
print(f"Deshecho: {deshecho}")
lista.mostrar()

rehecho = lista.rehacer()
print(f"Rehecho: {rehecho}")
lista.mostrar()

    



    


