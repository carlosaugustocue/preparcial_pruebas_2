"""
API REST para el modulo de recargas de RecargaYa S.A.S.
Construida con FastAPI.

Ejecutar:
    uv run uvicorn src.recargaya.api:app --port 8000 --reload
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator

from src.recargaya.recarga import ModuloRecarga

app = FastAPI(title="RecargaYa API", version="1.0.0")

_modulo = ModuloRecarga()


# ── Modelos de entrada ──────────────────────────────────────────────


class RecargaInput(BaseModel):
    monto: int
    premium: bool = False

    @field_validator("monto")
    @classmethod
    def monto_debe_ser_positivo(cls, v):
        if v <= 0:
            raise ValueError("El monto debe ser un entero positivo")
        return v


# ── Endpoints ──────────────────────────────────────────────────────


@app.get("/recarga/health")
def health_check():
    return {"status": "ok"}


@app.post("/recarga", status_code=200)
def calcular_recarga(recarga: RecargaInput):
    """
    Calcula el resultado de una recarga de celular.

    - **monto**: valor en pesos (1000 - 50000)
    - **premium**: si el usuario tiene plan premium (por defecto False)

    Retorna el monto, porcentaje de bonus y datos de bonificacion.
    """
    try:
        resultado = _modulo.calcular_recarga(monto=recarga.monto, premium=recarga.premium)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    return resultado
