from typing import Dict, List, Tuple

from .modelos import Producto, Sucursal
from .mapa import MapaCiudad
from .pasillos import GrafoPasillos


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


def crear_entorno_y_mapa() -> Tuple[
    EntornoHipermaxi,
    MapaCiudad,
    Dict[str, GrafoPasillos],
    Dict[str, Dict[str, str]],
]:
    """
    Crea:
      - EntornoHipermaxi con varias sucursales
      - MapaCiudad (grafo entre Casa y sucursales)
      - Un grafo de pasillos por sucursal
      - Un mapa producto -> pasillo por sucursal
    """
    entorno = EntornoHipermaxi()

    # --------- Definición de sucursales y productos ---------
    suc_norte = Sucursal(
        nombre="Hipermaxi Norte",
        productos=[
            Producto("Panetón pequeño", 35.50),
            Producto("Gaseosa 2L", 15.00),
            Producto("Chocolate navideño", 12.50),
            Producto("Galletas surtidas", 18.75),
            Producto("Sidra", 25.00),
        ],
    )

    suc_sur = Sucursal(
        nombre="Hipermaxi Sur",
        productos=[
            Producto("Panetón grande", 65.90),
            Producto("Gaseosa 3L", 18.50),
            Producto("Turrón", 22.00),
            Producto("Mantequilla", 10.00),
        ],
    )

    suc_este = Sucursal(
        nombre="Hipermaxi Este",
        productos=[
            Producto("Panetón mediano", 50.00),
            Producto("Chocolate en barra", 11.00),
            Producto("Galletas saladas", 14.00),
            Producto("Almendras", 24.50),
        ],
    )

    suc_oeste = Sucursal(
        nombre="Hipermaxi Oeste",
        productos=[
            Producto("Panetón familiar", 80.00),
            Producto("Gaseosa 1.5L", 12.00),
            Producto("Turrón de maní", 18.00),
            Producto("Queso rallado", 17.50),
        ],
    )

    # Agregar al entorno
    for s in [suc_norte, suc_sur, suc_este, suc_oeste]:
        entorno.agregar_sucursal(s)

    # --------- Mapa de la ciudad ---------
    mapa = MapaCiudad()
    mapa.agregar_arista("Casa", "Hipermaxi Norte", 10.0)
    mapa.agregar_arista("Casa", "Hipermaxi Sur", 6.0)
    mapa.agregar_arista("Casa", "Hipermaxi Este", 9.0)
    mapa.agregar_arista("Casa", "Hipermaxi Oeste", 12.0)

    mapa.agregar_arista("Hipermaxi Norte", "Hipermaxi Este", 5.0)
    mapa.agregar_arista("Hipermaxi Sur", "Hipermaxi Oeste", 7.0)

    # --------- Grafos de pasillos y mapa producto -> pasillo ---------
    grafos_pasillos: Dict[str, GrafoPasillos] = {}
    mapas_producto_pasillo: Dict[str, Dict[str, str]] = {}

    # Hipermaxi Norte
    grafo_norte = GrafoPasillos()
    # Nodos: "Entrada", "Panetones", "Bebidas", "Dulces", "Caja"
    grafo_norte.agregar_arista("Entrada", "Panetones", 3.0)
    grafo_norte.agregar_arista("Panetones", "Bebidas", 2.0)
    grafo_norte.agregar_arista("Bebidas", "Dulces", 2.0)
    grafo_norte.agregar_arista("Dulces", "Caja", 3.0)
    # Mapa producto -> pasillo
    mapa_norte = {
        "Panetón pequeño": "Panetones",
        "Gaseosa 2L": "Bebidas",
        "Chocolate navideño": "Dulces",
        "Galletas surtidas": "Dulces",
        "Sidra": "Bebidas",
    }
    grafos_pasillos[suc_norte.nombre] = grafo_norte
    mapas_producto_pasillo[suc_norte.nombre] = mapa_norte

    # Hipermaxi Sur
    grafo_sur = GrafoPasillos()
    grafo_sur.agregar_arista("Entrada", "Panetones", 4.0)
    grafo_sur.agregar_arista("Panetones", "Bebidas", 2.0)
    grafo_sur.agregar_arista("Bebidas", "Dulces", 3.0)
    grafo_sur.agregar_arista("Dulces", "Caja", 2.0)

    mapa_sur = {
        "Panetón grande": "Panetones",
        "Gaseosa 3L": "Bebidas",
        "Turrón": "Dulces",
        "Mantequilla": "Dulces",
    }
    grafos_pasillos[suc_sur.nombre] = grafo_sur
    mapas_producto_pasillo[suc_sur.nombre] = mapa_sur

    # Hipermaxi Este
    grafo_este = GrafoPasillos()
    grafo_este.agregar_arista("Entrada", "Panetones", 3.0)
    grafo_este.agregar_arista("Panetones", "Dulces", 2.5)
    grafo_este.agregar_arista("Dulces", "Snacks", 2.0)
    grafo_este.agregar_arista("Snacks", "Caja", 3.0)

    mapa_este = {
        "Panetón mediano": "Panetones",
        "Chocolate en barra": "Dulces",
        "Galletas saladas": "Snacks",
        "Almendras": "Snacks",
    }
    grafos_pasillos[suc_este.nombre] = grafo_este
    mapas_producto_pasillo[suc_este.nombre] = mapa_este

    # Hipermaxi Oeste
    grafo_oeste = GrafoPasillos()
    grafo_oeste.agregar_arista("Entrada", "Panetones", 5.0)
    grafo_oeste.agregar_arista("Panetones", "Bebidas", 3.0)
    grafo_oeste.agregar_arista("Bebidas", "Lácteos", 2.0)
    grafo_oeste.agregar_arista("Lácteos", "Caja", 2.5)

    mapa_oeste = {
        "Panetón familiar": "Panetones",
        "Gaseosa 1.5L": "Bebidas",
        "Turrón de maní": "Lácteos",  # solo como ejemplo de sección
        "Queso rallado": "Lácteos",
    }
    grafos_pasillos[suc_oeste.nombre] = grafo_oeste
    mapas_producto_pasillo[suc_oeste.nombre] = mapa_oeste

    return entorno, mapa, grafos_pasillos, mapas_producto_pasillo
