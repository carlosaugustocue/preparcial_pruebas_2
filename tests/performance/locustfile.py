"""
Prueba de carga para la API de RecargaYa.
Verifica que el P95 sea menor a 300ms con 30 usuarios simultaneos.

Ejecutar headless:
    uv run locust -f tests/performance/locustfile.py \
        --headless -u 30 -r 10 --run-time 30s \
        --csv=tests/performance/results \
        --host http://localhost:8000

Luego verificar P95:
    python scripts/check_p95.py
"""

from locust import HttpUser, between, task


class UsuarioRecarga(HttpUser):
    wait_time = between(1, 2)

    @task(3)
    def recarga_estandar(self):
        self.client.post(
            "/recarga",
            json={"monto": 20000, "premium": False},
            name="/recarga POST",
        )

    @task(2)
    def recarga_premium(self):
        self.client.post(
            "/recarga",
            json={"monto": 30000, "premium": True},
            name="/recarga POST premium",
        )

    @task(1)
    def health_check(self):
        self.client.get("/recarga/health", name="/recarga/health GET")
