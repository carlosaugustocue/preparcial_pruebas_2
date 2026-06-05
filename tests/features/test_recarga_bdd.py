"""
Step definitions para los escenarios BDD de recargas.
Cada funcion implementa un paso (Given/When/Then) del feature file.
"""

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from src.recargaya.recarga import ModuloRecarga

scenarios("recarga.feature")


# ──────────────────────────────────────────────────────
# GIVEN: Precondiciones
# ──────────────────────────────────────────────────────


@given("un usuario estandar", target_fixture="contexto")
def usuario_estandar():
    return {"modulo": ModuloRecarga(), "premium": False, "resultado": None, "error": None}


@given(parsers.parse("un usuario {tipo_usuario}"), target_fixture="contexto")
def usuario_por_tipo(tipo_usuario):
    es_premium = tipo_usuario.strip().lower() == "premium"
    return {"modulo": ModuloRecarga(), "premium": es_premium, "resultado": None, "error": None}


# ──────────────────────────────────────────────────────
# WHEN: Acciones
# ──────────────────────────────────────────────────────


@when(parsers.parse("intento realizar una recarga de {monto:d} pesos"))
def intentar_recarga(contexto, monto):
    try:
        contexto["resultado"] = contexto["modulo"].calcular_recarga(
            monto=monto, premium=contexto["premium"]
        )
    except ValueError as exc:
        contexto["error"] = str(exc)


@when(parsers.parse("realizo una recarga de {monto:d} pesos"))
def realizar_recarga(contexto, monto):
    contexto["resultado"] = contexto["modulo"].calcular_recarga(
        monto=monto, premium=contexto["premium"]
    )


# ──────────────────────────────────────────────────────
# THEN: Verificaciones
# ──────────────────────────────────────────────────────


@then("la recarga es rechazada con un error de rango")
def verificar_recarga_rechazada(contexto):
    assert contexto["error"] is not None, "Se esperaba un error pero la recarga fue aceptada"
    assert "rango" in contexto["error"], (
        f"El error no menciona 'rango': {contexto['error']}"
    )


@then("la recarga es aprobada")
def verificar_recarga_aprobada(contexto):
    assert contexto["error"] is None, f"No se esperaba error: {contexto['error']}"
    assert contexto["resultado"] is not None, "El resultado no debe ser None"


@then(parsers.parse("el porcentaje de bonus es {bonus:f}"))
def verificar_porcentaje_bonus(contexto, bonus):
    assert contexto["resultado"]["porcentaje_bonus"] == bonus, (
        f"Bonus esperado: {bonus}%, obtenido: {contexto['resultado']['porcentaje_bonus']}%"
    )


@then(parsers.parse("los datos de bonus son {datos:f}"))
def verificar_datos_bonus(contexto, datos):
    assert contexto["resultado"]["datos_bonus"] == datos, (
        f"Datos bonus esperados: {datos}, obtenidos: {contexto['resultado']['datos_bonus']}"
    )
