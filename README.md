# RecargaYa - Modulo de recargas de celular

Modulo TDD/BDD para calcular el valor final de recargas de celular con bonificaciones de datos.

## Reglas de negocio

| Condicion                        | Resultado             |
|----------------------------------|-----------------------|
| Monto < $1.000 o > $50.000       | Rechazado (error)     |
| $1.000 <= monto < $10.000        | 0% bonus datos        |
| $10.000 <= monto < $30.000       | 10% bonus datos       |
| monto >= $30.000                 | 25% bonus datos       |
| Usuario premium + bonus > 0      | +5% adicional         |

## Requisitos

- Python 3.12+
- [uv](https://github.com/astral-sh/uv)

```bash
uv sync --dev
```

## Comandos para ejecutar cada tipo de prueba

### Tests TDD (unitarios)

```bash
uv run pytest tests/test_recarga.py -v
```

### Tabla de equivalencia y valores limite

```bash
uv run pytest tests/test_tabla_equivalencia.py -v
```

### Tests BDD (Gherkin)

```bash
uv run pytest tests/features/ -v
```

### Tests de la API REST

```bash
uv run pytest tests/test_api.py -v
```

### Suite completa con cobertura

```bash
uv run pytest --cov=src --cov-report=term-missing -v
```

### Prueba de rendimiento con Locust (P95 < 300ms, 30 usuarios)

Primero levantar la API:

```bash
uv run uvicorn src.recargaya.api:app --port 8000
```

En otra terminal, correr Locust:

```bash
uv run locust -f tests/performance/locustfile.py \
  --headless -u 30 -r 10 --run-time 30s \
  --csv=tests/performance/results \
  --host http://localhost:8000
```

Verificar que el P95 sea menor a 300ms:

```bash
uv run python scripts/check_p95.py tests/performance/results_stats.csv
```

## Estructura del proyecto

```
src/recargaya/
  recarga.py       # Logica de negocio
  api.py           # API REST con FastAPI

tests/
  test_recarga.py              # Tests TDD unitarios
  test_tabla_equivalencia.py   # Tabla de particion de equivalencia
  test_api.py                  # Tests funcionales de la API
  features/
    recarga.feature            # Escenarios BDD en Gherkin
    test_recarga_bdd.py        # Step definitions
  performance/
    locustfile.py              # Script de carga Locust

scripts/
  check_p95.py     # Verifica P95 < 300ms sobre el CSV de Locust

.github/workflows/
  ci.yml           # Pipeline CI/CD
```
