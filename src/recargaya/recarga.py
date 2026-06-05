"""
Modulo RecargaYa: calculo del valor final de recargas de celular.
Construido con TDD - ciclos Red-Green-Refactor.
"""


class ModuloRecarga:
    """Calcula recargas y bonificaciones de datos para RecargaYa S.A.S."""

    def calcular_recarga(self, monto: int, premium: bool = False) -> dict:
        raise NotImplementedError
