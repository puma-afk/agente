from typing import List
import random
import math

from core.modelos import Sucursal, Producto


class AgenteComprador:
    """
    Agente basado en utilidad con búsqueda de Temple Simulado (Simulated Annealing).

    - Restricción: la suma de precios no debe exceder el monto del vale.
    - Objetivo: maximizar la suma (usar lo máximo posible del vale).
    """

    def __init__(self, sucursal: Sucursal, monto_vale: float):
        self.sucursal = sucursal
        self.monto_vale = monto_vale

    def _evaluar(self, seleccion: List[bool]) -> float:
        total = 0.0
        for toma, prod in zip(seleccion, self.sucursal.productos):
            if toma:
                total += prod.precio
        return total

    def _es_valida(self, seleccion: List[bool]) -> bool:
        return self._evaluar(seleccion) <= self.monto_vale + 1e-6

    def _generar_solucion_inicial(self) -> List[bool]:
        n = len(self.sucursal.productos)
        seleccion = [False] * n
        indices = list(range(n))
        random.shuffle(indices)

        for i in indices:
            seleccion[i] = True
            if not self._es_valida(seleccion):
                seleccion[i] = False
        return seleccion

    def _vecino_aleatorio(self, seleccion: List[bool]) -> List[bool] | None:
        """
        Genera un vecino al azar cambiando un producto,
        manteniendo la solución válida.
        """
        n = len(seleccion)
        indices = list(range(n))
        random.shuffle(indices)

        for i in indices:
            nueva = seleccion.copy()
            nueva[i] = not nueva[i]
            if self._es_valida(nueva):
                return nueva
        return None

    def planificar_compra(self) -> List[Producto]:
        if not self.sucursal.productos:
            return []

        actual = self._generar_solucion_inicial()
        valor_actual = self._evaluar(actual)

        mejor = actual.copy()
        mejor_valor = valor_actual

        T = max(self.monto_vale, 1.0)
        T_min = 1e-3
        alpha = 0.95
        max_iter = 1000

        for _ in range(max_iter):
            if T < T_min:
                break

            vecino = self._vecino_aleatorio(actual)
            if vecino is None:
                break

            valor_vecino = self._evaluar(vecino)
            delta = valor_vecino - valor_actual

            if delta >= 0:
                actual = vecino
                valor_actual = valor_vecino
            else:
                try:
                    prob = math.exp(delta / T)
                except OverflowError:
                    prob = 0.0
                if random.random() < prob:
                    actual = vecino
                    valor_actual = valor_vecino

            if valor_actual > mejor_valor + 1e-6:
                mejor = actual.copy()
                mejor_valor = valor_actual

            T = max(T * alpha, T_min)

        resultado: List[Producto] = []
        for toma, prod in zip(mejor, self.sucursal.productos):
            if toma:
                resultado.append(prod)
        return resultado
