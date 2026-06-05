"""
Modulo RecargaYa: calculo del valor final de recargas de celular.
Construido con TDD - ciclos Red-Green-Refactor.
"""


class ModuloRecarga:
    """Calcula recargas y bonificaciones de datos para RecargaYa S.A.S."""

    MONTO_MINIMO = 1_000
    MONTO_MAXIMO = 50_000

    def _validar_monto(self, monto: int) -> None:
        if monto < self.MONTO_MINIMO or monto > self.MONTO_MAXIMO:
            raise ValueError(
                f"Monto fuera de rango: debe estar entre {self.MONTO_MINIMO} "
                f"y {self.MONTO_MAXIMO}, recibido {monto}"
            )

    def calcular_recarga(self, monto: int, premium: bool = False) -> dict:
        self._validar_monto(monto)
        raise NotImplementedError
