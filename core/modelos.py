from dataclasses import dataclass
from typing import List


@dataclass
class Producto:
    nombre: str
    precio: float  # en Bs


@dataclass
class Sucursal:
    nombre: str
    productos: List[Producto]

    def listar_productos(self):
        print(f"\nProductos en {self.nombre}:")
        if not self.productos:
            print("  (Sin productos)")
            return
        for i, p in enumerate(self.productos, start=1):
            print(f"{i}. {p.nombre} - {p.precio:.2f} Bs")

    def agregar_producto(self, nombre: str, precio: float):
        self.productos.append(Producto(nombre, precio))

    def actualizar_precio_por_indice(self, indice: int, nuevo_precio: float):
        if 0 <= indice < len(self.productos):
            self.productos[indice].precio = nuevo_precio
        else:
            print("Índice de producto inválido.")

    def eliminar_producto_por_indice(self, indice: int):
        if 0 <= indice < len(self.productos):
            eliminado = self.productos.pop(indice)
            print(f"Producto eliminado: {eliminado.nombre}")
        else:
            print("Índice de producto inválido.")
