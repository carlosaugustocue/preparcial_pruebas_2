"""
Tabla de casos de prueba - Particion de equivalencia y valores limite.

Campo analizado: monto de recarga

Clases de equivalencia identificadas:
  CE1 - Invalido inferior: monto < 1000           -> ValueError
  CE2 - Valido sin bonus:  1000 <= monto < 10000  -> 0% bonus
  CE3 - Valido 10% bonus:  10000 <= monto < 30000 -> 10% bonus
  CE4 - Valido 25% bonus:  30000 <= monto <= 50000 -> 25% bonus
  CE5 - Invalido superior: monto > 50000          -> ValueError

Valores limite del campo monto:
  Limite inferior: 999 (invalido), 1000 (valido min)
  Limite clase 2/3: 9999 (sin bonus), 10000 (10% bonus)
  Limite clase 3/4: 29999 (10% bonus), 30000 (25% bonus)
  Limite superior: 50000 (valido max), 50001 (invalido)
"""

import pytest

from src.recargaya.recarga import ModuloRecarga

modulo = ModuloRecarga()

# ---------------------------------------------------------------------------
# Tabla de casos: cada tupla es (id_caso, descripcion, monto, premium,
#                                 es_valido, porcentaje_bonus_esperado)
# ---------------------------------------------------------------------------
CASOS = [
    # --- CE1: Invalidos inferiores ---
    ("TC01", "Monto cero - invalido absoluto",      0,        False, False, None),
    ("TC02", "Monto negativo - invalido",          -500,      False, False, None),
    ("TC03", "Limite inferior invalido (999)",      999,       False, False, None),

    # --- CE2: Validos sin bonus ---
    ("TC04", "Limite inferior valido (1000)",       1_000,     False, True,  0.0),
    ("TC05", "Representante clase sin bonus",       5_000,     False, True,  0.0),
    ("TC06", "Limite superior sin bonus (9999)",    9_999,     False, True,  0.0),

    # --- CE3: Validos con 10% de bonus ---
    ("TC07", "Limite inferior 10% bonus (10000)",  10_000,    False, True,  10.0),
    ("TC08", "Representante clase 10% bonus",      20_000,    False, True,  10.0),
    ("TC09", "Limite superior 10% bonus (29999)",  29_999,    False, True,  10.0),

    # --- CE4: Validos con 25% de bonus ---
    ("TC10", "Limite inferior 25% bonus (30000)",  30_000,    False, True,  25.0),
    ("TC11", "Representante clase 25% bonus",      40_000,    False, True,  25.0),
    ("TC12", "Limite superior valido (50000)",     50_000,    False, True,  25.0),

    # --- CE5: Invalidos superiores ---
    ("TC13", "Limite superior invalido (50001)",   50_001,    False, False, None),
    ("TC14", "Monto extremo invalido",            100_000,    False, False, None),

    # --- Premium: combinaciones con plan premium ---
    ("TC15", "Premium sin bonus base (monto < 10000)",  5_000, True,  True,  0.0),
    ("TC16", "Premium con 10% bonus (10000)",          10_000, True,  True,  15.0),
    ("TC17", "Premium con 25% bonus (30000)",          30_000, True,  True,  30.0),
]


@pytest.mark.parametrize(
    "id_caso, descripcion, monto, premium, es_valido, bonus_esperado",
    CASOS,
    ids=[c[0] for c in CASOS],
)
def test_tabla_equivalencia(id_caso, descripcion, monto, premium, es_valido, bonus_esperado):
    """
    Ejecuta cada caso de la tabla de particion de equivalencia y valores limite.
    - Si es_valido=False se espera ValueError.
    - Si es_valido=True se verifica el porcentaje de bonus correcto.
    """
    if not es_valido:
        with pytest.raises(ValueError, match="rango"):
            modulo.calcular_recarga(monto=monto, premium=premium)
    else:
        resultado = modulo.calcular_recarga(monto=monto, premium=premium)
        assert resultado["monto"] == monto, f"{id_caso} - {descripcion}: monto incorrecto"
        assert resultado["porcentaje_bonus"] == bonus_esperado, (
            f"{id_caso} - {descripcion}: bonus esperado {bonus_esperado}%, "
            f"obtenido {resultado['porcentaje_bonus']}%"
        )
        datos_bonus_esperados = monto * (bonus_esperado / 100)
        assert resultado["datos_bonus"] == datos_bonus_esperados, (
            f"{id_caso} - {descripcion}: datos_bonus incorrecto"
        )
