"""
Lee el CSV generado por Locust y verifica que el P95 sea < 300ms.

Uso:
    python scripts/check_p95.py tests/performance/results_stats.csv
"""

import csv
import sys

P95_LIMITE_MS = 300
archivo = sys.argv[1] if len(sys.argv) > 1 else "tests/performance/results_stats.csv"

fallos = []
with open(archivo, newline="") as f:
    for fila in csv.DictReader(f):
        nombre = fila["Name"]
        if nombre == "Aggregated":
            continue
        p95 = float(fila["95%"])
        if p95 >= P95_LIMITE_MS:
            fallos.append(f"  {nombre}: P95={p95}ms (limite={P95_LIMITE_MS}ms)")

if fallos:
    print("FALLO - P95 supera el limite en:")
    print("\n".join(fallos))
    sys.exit(1)

print(f"OK - Todos los endpoints tienen P95 < {P95_LIMITE_MS}ms")
