from typing import List, Dict, Set

from core.pasillos import GrafoPasillos
from core.modelos import Producto


class AgenteNavegadorPasillos:
    """
    Agente que planifica la ruta interna dentro de una sucursal.
    - Recibe el grafo de pasillos de la sucursal.
    - Recibe el mapa producto -> pasillo.
    - A partir de la lista de productos seleccionados, calcula una ruta:
      Entrada -> ...pasillos necesarios... -> Caja
    """

    def __init__(self, grafo_pasillos: GrafoPasillos, producto_a_pasillo: Dict[str, str]):
        self.grafo = grafo_pasillos
        self.producto_a_pasillo = producto_a_pasillo

    def planificar_ruta(self, productos: List[Producto]) -> List[str]:
        # Obtener el conjunto de pasillos donde hay que recoger productos
        pasillos_necesarios: Set[str] = set()

        for p in productos:
            pasillo = self.producto_a_pasillo.get(p.nombre)
            if pasillo is not None:
                pasillos_necesarios.add(pasillo)
            else:
                # Producto sin pasillo asignado (por ejemplo, agregado dinámicamente)
                print(f"[Agente Navegador] Advertencia: el producto '{p.nombre}' no tiene pasillo asignado.")

        # Si no hay pasillos (caso raro), simplemente ir de Entrada a Caja
        if not pasillos_necesarios:
            # Intentamos buscar camino directo, si es posible
            resultado = self.grafo.camino_mas_corto("Entrada", "Caja")
            if resultado is None:
                return ["Entrada", "Caja"]
            camino, _ = resultado
            return camino

        ruta: List[str] = []
        actual = "Entrada"
        ruta.append(actual)

        pendientes: Set[str] = set(pasillos_necesarios)

        # Estrategia simple: desde el nodo actual, ir siempre al pasillo pendiente más cercano
        while pendientes:
            mejor_camino = None
            mejor_dist = None
            mejor_objetivo = None

            for objetivo in pendientes:
                resultado = self.grafo.camino_mas_corto(actual, objetivo)
                if resultado is None:
                    continue
                camino, dist = resultado

                if mejor_dist is None or dist < mejor_dist:
                    mejor_dist = dist
                    mejor_camino = camino
                    mejor_objetivo = objetivo

            if mejor_camino is None or mejor_objetivo is None:
                # No se puede llegar a alguno de los pasillos (grafo incompleto)
                break

            # Agregar el camino, excluyendo el nodo inicial (ya está en ruta)
            for nodo in mejor_camino[1:]:
                ruta.append(nodo)

            actual = mejor_objetivo
            pendientes.remove(mejor_objetivo)

        # Finalmente, ir desde el último pasillo visitado hasta la Caja
        resultado_caja = self.grafo.camino_mas_corto(actual, "Caja")
        if resultado_caja is not None:
            camino_caja, _ = resultado_caja
            for nodo in camino_caja[1:]:
                ruta.append(nodo)
        else:
            # Si no hay camino a la caja, al menos la agregamos como destino conceptual
            ruta.append("Caja")

        return ruta

