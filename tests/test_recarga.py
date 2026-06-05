"""
Tests unitarios para el modulo de recargas - TDD.
Cada test se escribio ANTES que el codigo de produccion correspondiente.
"""

import pytest

from src.recargaya.recarga import ModuloRecarga


# =============================================================================
# CICLO 1 - Validacion de rango de monto
# =============================================================================


def test_monto_por_debajo_del_minimo_es_rechazado():
    """Un monto de $999 esta fuera del rango valido y debe lanzar ValueError."""
    modulo = ModuloRecarga()
    with pytest.raises(ValueError, match="rango"):
        modulo.calcular_recarga(monto=999)


def test_monto_cero_es_rechazado():
    """Un monto de $0 es invalido."""
    modulo = ModuloRecarga()
    with pytest.raises(ValueError, match="rango"):
        modulo.calcular_recarga(monto=0)


def test_monto_negativo_es_rechazado():
    """Un monto negativo es invalido."""
    modulo = ModuloRecarga()
    with pytest.raises(ValueError, match="rango"):
        modulo.calcular_recarga(monto=-500)


def test_monto_por_encima_del_maximo_es_rechazado():
    """Un monto de $50.001 supera el limite y debe lanzar ValueError."""
    modulo = ModuloRecarga()
    with pytest.raises(ValueError, match="rango"):
        modulo.calcular_recarga(monto=50_001)


def test_monto_extremo_alto_es_rechazado():
    """Un monto de $100.000 esta muy por encima del limite."""
    modulo = ModuloRecarga()
    with pytest.raises(ValueError, match="rango"):
        modulo.calcular_recarga(monto=100_000)


# =============================================================================
# CICLO 2 - Calculo de bonus de datos
# =============================================================================


def test_monto_minimo_valido_no_tiene_bonus():
    """$1.000 es el minimo valido y no genera bonus de datos."""
    modulo = ModuloRecarga()
    resultado = modulo.calcular_recarga(monto=1_000)
    assert resultado["monto"] == 1_000
    assert resultado["porcentaje_bonus"] == 0.0
    assert resultado["datos_bonus"] == 0.0


def test_monto_valido_sin_bonus():
    """$5.000 esta en rango valido pero no alcanza el umbral de bonus."""
    modulo = ModuloRecarga()
    resultado = modulo.calcular_recarga(monto=5_000)
    assert resultado["porcentaje_bonus"] == 0.0


def test_monto_limite_superior_sin_bonus():
    """$9.999 es el tope justo antes del umbral de 10% de bonus."""
    modulo = ModuloRecarga()
    resultado = modulo.calcular_recarga(monto=9_999)
    assert resultado["porcentaje_bonus"] == 0.0


def test_monto_umbral_diez_por_ciento_da_bonus():
    """$10.000 alcanza el umbral y debe generar 10% de bonus."""
    modulo = ModuloRecarga()
    resultado = modulo.calcular_recarga(monto=10_000)
    assert resultado["porcentaje_bonus"] == 10.0
    assert resultado["datos_bonus"] == 1_000.0


def test_monto_medio_clase_diez_por_ciento():
    """$20.000 esta dentro de la clase 10% de bonus."""
    modulo = ModuloRecarga()
    resultado = modulo.calcular_recarga(monto=20_000)
    assert resultado["porcentaje_bonus"] == 10.0
    assert resultado["datos_bonus"] == 2_000.0


def test_monto_limite_superior_diez_por_ciento():
    """$29.999 es el tope justo antes del umbral de 25% de bonus."""
    modulo = ModuloRecarga()
    resultado = modulo.calcular_recarga(monto=29_999)
    assert resultado["porcentaje_bonus"] == 10.0


def test_monto_umbral_veinticinco_por_ciento_da_bonus():
    """$30.000 alcanza el umbral y debe generar 25% de bonus."""
    modulo = ModuloRecarga()
    resultado = modulo.calcular_recarga(monto=30_000)
    assert resultado["porcentaje_bonus"] == 25.0
    assert resultado["datos_bonus"] == 7_500.0


def test_monto_maximo_valido_tiene_bonus_veinticinco():
    """$50.000 es el maximo valido y pertenece a la clase 25% de bonus."""
    modulo = ModuloRecarga()
    resultado = modulo.calcular_recarga(monto=50_000)
    assert resultado["porcentaje_bonus"] == 25.0
    assert resultado["datos_bonus"] == 12_500.0


# =============================================================================
# CICLO 3 - Bonus adicional para usuarios premium
# =============================================================================


def test_premium_sin_bonus_base_no_obtiene_bonus_adicional():
    """Un usuario premium con monto < $10.000 no obtiene bonus (no hay base)."""
    modulo = ModuloRecarga()
    resultado = modulo.calcular_recarga(monto=5_000, premium=True)
    assert resultado["porcentaje_bonus"] == 0.0


def test_premium_con_bonus_diez_por_ciento_obtiene_cinco_adicional():
    """Un usuario premium con $10.000 obtiene 10% + 5% = 15% de bonus."""
    modulo = ModuloRecarga()
    resultado = modulo.calcular_recarga(monto=10_000, premium=True)
    assert resultado["porcentaje_bonus"] == 15.0
    assert resultado["datos_bonus"] == 1_500.0


def test_premium_con_bonus_veinticinco_obtiene_cinco_adicional():
    """Un usuario premium con $30.000 obtiene 25% + 5% = 30% de bonus."""
    modulo = ModuloRecarga()
    resultado = modulo.calcular_recarga(monto=30_000, premium=True)
    assert resultado["porcentaje_bonus"] == 30.0
    assert resultado["datos_bonus"] == 9_000.0


def test_usuario_no_premium_no_obtiene_bonus_adicional():
    """Un usuario estandar con $30.000 obtiene exactamente 25%."""
    modulo = ModuloRecarga()
    resultado = modulo.calcular_recarga(monto=30_000, premium=False)
    assert resultado["porcentaje_bonus"] == 25.0
