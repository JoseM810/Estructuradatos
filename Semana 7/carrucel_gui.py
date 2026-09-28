import tkinter as tk
from PIL import Image, ImageTk


class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class Carrucel:
    def __init__(self):
        self.cabeza = None
        self.cola = None
        self.actual = None

    def insertar_inicio(self, dato):
        nuevo = Nodo(dato)

        if self.cabeza is None:
            self.cabeza = nuevo
            self.cola = nuevo
            self.actual = nuevo
        else:
            nuevo.siguiente = self.cabeza
            self.cabeza = nuevo

        self.cola.siguiente = self.cabeza

    def insertar_final(self, dato):
        nuevo = Nodo(dato)

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

    def anterior_imagen(self):
        if self.actual is None:
            return
       
        nodo = self.actual
        while nodo.siguiente != self.actual:
            nodo = nodo.siguiente
        self.actual = nodo

    def mostrar_actual(self):
        if self.actual:
            print(f"Mostrando: {self.actual.dato}")


class VentanaCarrucel:
    def __init__(self, carrucel):
        self.carrucel = carrucel

        self.ventana = tk.Tk()
        self.ventana.title("Carrusel de imágenes")

        self.etiqueta_imagen = tk.Label(self.ventana)
        self.etiqueta_imagen.pack(padx=10, pady=10)

        marco_botones = tk.Frame(self.ventana)
        marco_botones.pack(pady=10)

        boton_anterior = tk.Button(marco_botones, text="Anterior", command=self.mostrar_anterior)
        boton_anterior.pack(side=tk.LEFT, padx=5)

        boton_siguiente = tk.Button(marco_botones, text="Siguiente", command=self.mostrar_siguiente)
        boton_siguiente.pack(side=tk.LEFT, padx=5)

        self.actualizar_imagen()

    def actualizar_imagen(self):
        ruta = self.carrucel.actual.dato
        imagen = Image.open(ruta)
        imagen.thumbnail((500, 500))  # ajusta el tamaño sin deformar
        self.imagen_tk = ImageTk.PhotoImage(imagen)
        self.etiqueta_imagen.config(image=self.imagen_tk)

    def mostrar_siguiente(self):
        self.carrucel.siguiente_imagen()
        self.actualizar_imagen()

    def mostrar_anterior(self):
        self.carrucel.anterior_imagen()
        self.actualizar_imagen()

    def ejecutar(self):
        self.ventana.mainloop()


if __name__ == "__main__":
    ca = Carrucel()

ca.insertar_final("imagenes/gato.jpg")
ca.insertar_final("imagenes/jaguar.jpg")
ca.insertar_final("imagenes/leon.jpg")
ca.insertar_final("imagenes/pantera.jpg")
ca.insertar_final("imagenes/tigre.jpg")
    

app = VentanaCarrucel(ca)
app.ejecutar()
