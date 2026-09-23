class Nodo:

    def __init__(self, dato, anterior=None, siguiente=None):
        self.dato = dato
        self.anterior = anterior
        self.siguiente = siguiente

class listaEnlazada:
     
     def __init__(self):
         self.cabeza = None
         self.cola = None
         self.siguiente = None

     def hacer (self,dato):
        self.dato= nuevo

        if self.cabeza is None:
            nuevo= self.cabeza
            nuevo = self.cola
        else:
            self.cola.siguiente = nuevo
            self.nuevo.anterior = self.cola
            self.cola = nuevo

     def deshacer (self, dato):

        if self.cabeza is None:
            print("No hay nada que deshacer")
            return None

        nodo_eliminado = self.cola

        if self.cola.anterior is None:
            self.cabeza = None
            self.cola = None
        else:
            self.cola = self.cola.anterior
            self.siguiente = None

        return nodo_eliminado.dato

    
    



    


