from typing import Dict, List, Tuple, Optional
import heapq


class GrafoPasillos:
    """
    Grafo no dirigido para representar los pasillos dentro de una sucursal.
    Nodos: nombres de pasillos (str), por ejemplo: "Entrada", "Panetones", "Bebidas", "Caja", etc.
    Aristas: conexiones con una distancia (costo).
    """

    def __init__(self):
        # nodo -> lista de (vecino, distancia)
        self.ady: Dict[str, List[Tuple[str, float]]] = {}

    def agregar_arista(self, a: str, b: str, distancia: float):
        """Agrega una arista bidireccional entre dos pasillos."""
        self.ady.setdefault(a, []).append((b, distancia))
        self.ady.setdefault(b, []).append((a, distancia))

    def camino_mas_corto(self, origen: str, destino: str) -> Optional[Tuple[List[str], float]]:
        """
        Calcula el camino más corto entre 'origen' y 'destino' usando búsqueda
        de costo uniforme (equivalente a Dijkstra con pesos positivos).

        Devuelve:
          (lista_de_nodos_en_el_camino, distancia_total)
        o None si no hay camino.
        """
        if origen == destino:
            return [origen], 0.0

        # (costo_acumulado, nodo)
        frontera: List[Tuple[float, str]] = [(0.0, origen)]
        dist: Dict[str, float] = {origen: 0.0}
        padre: Dict[str, Optional[str]] = {origen: None}

        while frontera:
            costo, nodo = heapq.heappop(frontera)

            if nodo == destino:
                # reconstruir camino
                camino = []
                actual = destino
                while actual is not None:
                    camino.append(actual)
                    actual = padre[actual]
                camino.reverse()
                return camino, costo

            if costo > dist.get(nodo, float("inf")):
                continue

            for vecino, d in self.ady.get(nodo, []):
                nuevo_costo = costo + d
                if nuevo_costo < dist.get(vecino, float("inf")):
                    dist[vecino] = nuevo_costo
                    padre[vecino] = nodo
                    heapq.heappush(frontera, (nuevo_costo, vecino))

        return None
