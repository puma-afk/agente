from typing import List
import random

from core.modelos import Sucursal, Producto


class AgenteComprador:
    """
    Agente basado en utilidad con búsqueda de Ascensión de Colinas.

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

    def _vecinos(self, seleccion: List[bool]) -> List[List[bool]]:
        vecinos = []
        n = len(seleccion)
        for i in range(n):
            nueva = seleccion.copy()
            nueva[i] = not nueva[i]
            if self._es_valida(nueva):
                vecinos.append(nueva)
        return vecinos

    def planificar_compra(self) -> List[Producto]:
        if not self.sucursal.productos:
            return []

        actual = self._generar_solucion_inicial()
        valor_actual = self._evaluar(actual)

        mejorando = True
        while mejorando:
            vecinos = self._vecinos(actual)
            if not vecinos:
                break

            mejor_vecino = actual
            mejor_valor = valor_actual

            for v in vecinos:
                val = self._evaluar(v)
                if val > mejor_valor:
                    mejor_valor = val
                    mejor_vecino = v

            if mejor_valor <= valor_actual + 1e-6:
                mejorando = False
            else:
                actual = mejor_vecino
                valor_actual = mejor_valor

        resultado: List[Producto] = []
        for toma, prod in zip(actual, self.sucursal.productos):
            if toma:
                resultado.append(prod)
        return resultado

