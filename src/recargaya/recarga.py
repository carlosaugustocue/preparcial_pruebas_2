"""
Modulo RecargaYa: calculo del valor final de recargas de celular.
Construido con TDD - ciclos Red-Green-Refactor.
"""


class ModuloRecarga:
    """Calcula recargas y bonificaciones de datos para RecargaYa S.A.S."""

    def calcular_recarga(self, monto: int, premium: bool = False) -> dict:
        if monto < 1000 or monto > 50000:
            raise ValueError(f"Monto fuera de rango: debe estar entre 1000 y 50000, recibido {monto}")
        raise NotImplementedError
