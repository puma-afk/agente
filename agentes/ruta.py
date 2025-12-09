from typing import Dict, List, Tuple
import heapq

from core.mapa import MapaCiudad


class AgenteRuta:
    """
    Usa Búsqueda de Costo Uniforme para encontrar
    la sucursal más cercana desde un origen.
    """

    def __init__(self, mapa: MapaCiudad, nombres_sucursales: List[str]):
        self.mapa = mapa
        self.nombres_sucursales = set(nombres_sucursales)

    def sucursal_mas_cercana(self, origen: str):
        frontera: List[Tuple[float, str]] = [(0.0, origen)]
        visitado: Dict[str, float] = {}

        while frontera:
            costo, nodo = heapq.heappop(frontera)

            if nodo in visitado:
                continue
            visitado[nodo] = costo

            if nodo in self.nombres_sucursales:
                return nodo

            for vecino, d in self.mapa.ady.get(nodo, []):
                if vecino not in visitado:
                    heapq.heappush(frontera, (costo + d, vecino))

        return None
