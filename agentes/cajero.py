from typing import List

from core.modelos import Producto


class AgenteCajero:
    def __init__(self, monto_vale: float):
        self.monto_vale = monto_vale

    def verificar_compra(self, productos: List[Producto]) -> bool:
        total = sum(p.precio for p in productos)
        return total <= self.monto_vale + 1e-6

