class Nodo:

    def __init__(self, dato, anterior=None, siguiente=None):
        self.dato = dato
        self.anterior = anterior
        self.siguiente = siguiente

class ListaEnlazada:
     
     def __init__(self):
         self.cabeza = None
         self.cola = None

     def hacer(self, dato):
        nuevo = Nodo(dato)

        if self.cabeza is None:
            self.cabeza = nuevo
            self.cola = nuevo
        else:
            nuevo.anterior = self.cola
            self.cola.siguiente = nuevo
            self.cola = nuevo

     def deshacer(self):  

        if self.cabeza is None:
            print("No hay nada que deshacer")
            return None

        nodo_eliminado = self.cola

        if self.cola.anterior is None:
            self.cabeza = None
            self.cola = None
        else:
            self.cola = self.cola.anterior
            self.cola.siguiente = None

        return nodo_eliminado.dato

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

    
    



    


