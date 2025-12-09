from typing import Dict, List, Tuple


class MapaCiudad:
    """
    Grafo no dirigido con distancias.
    Nodo: nombre (str), por ejemplo "Casa", "Hipermaxi Norte", etc.
    """

    def __init__(self):
        # nodo -> lista de (vecino, distancia)
        self.ady: Dict[str, List[Tuple[str, float]]] = {}

    def agregar_arista(self, a: str, b: str, distancia: float):
        self.ady.setdefault(a, []).append((b, distancia))
        self.ady.setdefault(b, []).append((a, distancia))
