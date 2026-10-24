class Automovil:

    marca: str
    color: str
    modelo: str
    anio: int

    def _init_(self, marca:  str):
        self.marca = marca

    def set_color(self, color: str):
        self.color = color

    def set_modelo(self, modelo: str):
        self.modelo = modelo

    def set_anio(self, anio: int):
        self.anio = anio

    def revisar_estado(self)-> bool:
        # codigo .....
        return True

auto1 = Automovil('Mazda')
auto2 = Automovil('Toyota')
auto3 = Automovil('Mazda')
auto4 = auto1



numero1 = 5
numero2 = 5
if auto1 == auto3:
    print("Son iguales")
else:
    print("No son iguales")

print("Objeto 1: ", auto1)
print("Objeto 2: ", auto2)
print("Objeto 3: ", auto3)
print("Objeto 4: ", auto4)
