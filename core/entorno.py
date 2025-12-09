from typing import Dict, List, Tuple

from .modelos import Producto, Sucursal
from .mapa import MapaCiudad


class EntornoHipermaxi:
    """
    Maneja todas las sucursales de Hipermaxi.
    """
    def __init__(self):
        self.sucursales: Dict[str, Sucursal] = {}

    def agregar_sucursal(self, sucursal: Sucursal):
        self.sucursales[sucursal.nombre] = sucursal

    def listar_sucursales(self):
        print("\nSucursales disponibles:")
        if not self.sucursales:
            print("  (No hay sucursales)")
            return
        for i, nombre in enumerate(self.sucursales.keys(), start=1):
            print(f"{i}. {nombre}")

    def obtener_por_indice(self, indice: int):
        nombres = list(self.sucursales.keys())
        if 0 <= indice < len(nombres):
            return self.sucursales[nombres[indice]]
        return None

    def obtener_por_nombre(self, nombre: str):
        return self.sucursales.get(nombre)

    def nombres_sucursales(self) -> List[str]:
        return list(self.sucursales.keys())


def crear_entorno_y_mapa() -> Tuple[EntornoHipermaxi, MapaCiudad]:
    entorno = EntornoHipermaxi()

    entorno.agregar_sucursal(Sucursal(
        nombre="Hipermaxi Norte",
        productos=[
            Producto("Panetón pequeño", 35.50),
            Producto("Gaseosa 2L", 15.00),
            Producto("Chocolate navideño", 12.50),
            Producto("Galletas surtidas", 18.75),
            Producto("Sidra", 25.00),
        ]
    ))

    entorno.agregar_sucursal(Sucursal(
        nombre="Hipermaxi Sur",
        productos=[
            Producto("Panetón grande", 65.90),
            Producto("Gaseosa 3L", 18.50),
            Producto("Turrón", 22.00),
            Producto("Mantequilla", 10.00),
        ]
    ))

    entorno.agregar_sucursal(Sucursal(
        nombre="Hipermaxi Este",
        productos=[
            Producto("Panetón mediano", 50.00),
            Producto("Chocolate en barra", 11.00),
            Producto("Galletas saladas", 14.00),
            Producto("Almendras", 24.50),
        ]
    ))

    entorno.agregar_sucursal(Sucursal(
        nombre="Hipermaxi Oeste",
        productos=[
            Producto("Panetón familiar", 80.00),
            Producto("Gaseosa 1.5L", 12.00),
            Producto("Turrón de maní", 18.00),
            Producto("Queso rallado", 17.50),
        ]
    ))

    mapa = MapaCiudad()
    mapa.agregar_arista("Casa", "Hipermaxi Norte", 10.0)
    mapa.agregar_arista("Casa", "Hipermaxi Sur", 6.0)
    mapa.agregar_arista("Casa", "Hipermaxi Este", 9.0)
    mapa.agregar_arista("Casa", "Hipermaxi Oeste", 12.0)

    mapa.agregar_arista("Hipermaxi Norte", "Hipermaxi Este", 5.0)
    mapa.agregar_arista("Hipermaxi Sur", "Hipermaxi Oeste", 7.0)

    return entorno, mapa

