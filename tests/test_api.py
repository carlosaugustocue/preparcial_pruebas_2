"""
Tests funcionales para la API REST de RecargaYa.
Usan el cliente de prueba de FastAPI (httpx + TestClient).
"""

from fastapi.testclient import TestClient

from src.recargaya.api import app

client = TestClient(app)


def test_health_check():
    response = client.get("/recarga/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_recarga_valida_sin_bonus():
    response = client.post("/recarga", json={"monto": 5000, "premium": False})
    assert response.status_code == 200
    data = response.json()
    assert data["monto"] == 5000
    assert data["porcentaje_bonus"] == 0.0


def test_recarga_con_bonus_10_por_ciento():
    response = client.post("/recarga", json={"monto": 10000, "premium": False})
    assert response.status_code == 200
    assert response.json()["porcentaje_bonus"] == 10.0


def test_recarga_con_bonus_25_por_ciento():
    response = client.post("/recarga", json={"monto": 30000, "premium": False})
    assert response.status_code == 200
    assert response.json()["porcentaje_bonus"] == 25.0


def test_recarga_premium_con_bonus():
    response = client.post("/recarga", json={"monto": 10000, "premium": True})
    assert response.status_code == 200
    assert response.json()["porcentaje_bonus"] == 15.0


def test_recarga_monto_invalido_retorna_422():
    response = client.post("/recarga", json={"monto": 999, "premium": False})
    assert response.status_code == 422


def test_recarga_monto_superior_invalido_retorna_422():
    response = client.post("/recarga", json={"monto": 50001, "premium": False})
    assert response.status_code == 422
