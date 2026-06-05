"""
Modulo RecargaYa: calculo del valor final de recargas de celular.
Construido con TDD - ciclos Red-Green-Refactor.
"""


class ModuloRecarga:
    """Calcula recargas y bonificaciones de datos para RecargaYa S.A.S."""

    MONTO_MINIMO = 1_000
    MONTO_MAXIMO = 50_000
    UMBRAL_BONUS_10 = 10_000
    UMBRAL_BONUS_25 = 30_000

    def _validar_monto(self, monto: int) -> None:
        if monto < self.MONTO_MINIMO or monto > self.MONTO_MAXIMO:
            raise ValueError(
                f"Monto fuera de rango: debe estar entre {self.MONTO_MINIMO} "
                f"y {self.MONTO_MAXIMO}, recibido {monto}"
            )

    def _calcular_porcentaje_bonus(self, monto: int) -> float:
        if monto >= self.UMBRAL_BONUS_25:
            return 25.0
        if monto >= self.UMBRAL_BONUS_10:
            return 10.0
        return 0.0

    def calcular_recarga(self, monto: int, premium: bool = False) -> dict:
        self._validar_monto(monto)
        porcentaje_bonus = self._calcular_porcentaje_bonus(monto)
        datos_bonus = monto * (porcentaje_bonus / 100)
        return {
            "monto": monto,
            "porcentaje_bonus": porcentaje_bonus,
            "datos_bonus": datos_bonus,
        }
