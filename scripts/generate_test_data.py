"""Genera datos dummy en files/data_processed/ para que los tests
funcionen sin depender de la API del INE ni de ejecutar los notebooks.
"""
import itertools
import pandas as pd
import numpy as np
from pathlib import Path

DATA_DIR = Path("files/data_processed")
DATA_DIR.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(42)

# 1. Dimensión tiempo — 12 meses reales de 2024
fechas = pd.date_range("2024-01-01", periods=12, freq="ME")
tiempo = pd.DataFrame({
    "id_tiempo": fechas.strftime("%Y%m").astype(int),
    "anio": fechas.year.astype(int),
    "mes": fechas.month.astype(int),
    "nombre_mes": fechas.strftime("%B").str.lower(),
})
tiempo.to_csv(DATA_DIR / "tiempo.csv", index=False)

# 2. Dimensión territorio (20 comunidades)
territorio = pd.DataFrame({
    "id_territorio": range(1, 21),
    "nombre_territorio": [f"territorio_{i}" for i in range(1, 21)],
})
territorio.to_csv(DATA_DIR / "territorio.csv", index=False)

# 3. Dimensión sectores IPC (14 sectores)
sectores = pd.DataFrame({
    "id_sector": range(1, 15),
    "nombre_sector": [f"sector_{i}" for i in range(1, 15)],
})
sectores.to_csv(DATA_DIR / "sectores_ipc.csv", index=False)

# 4. Dimensión tipo medida (4 tipos)
tipo_medida = pd.DataFrame({
    "id_medida": range(1, 5),
    "nombre_medida": ["indice", "variacion_mensual", "variacion_anual", "variacion_acumulada"],
})
tipo_medida.to_csv(DATA_DIR / "tipo_medida.csv", index=False)

# 5. Tabla de hechos IPC (combinaciones únicas)
tiempos = range(202401, 202413)
territorios = range(1, 21)
sectores = range(1, 15)
medidas = range(1, 5)

combinaciones = list(itertools.product(tiempos, territorios, sectores, medidas))
seleccion = rng.choice(len(combinaciones), size=500, replace=False)
ipc = pd.DataFrame({
    "id_tiempo": [combinaciones[i][0] for i in seleccion],
    "id_territorio": [combinaciones[i][1] for i in seleccion],
    "id_sector": [combinaciones[i][2] for i in seleccion],
    "id_medida": [combinaciones[i][3] for i in seleccion],
    "valor_ipc": rng.uniform(80, 120, 500).round(3),
})
ipc.to_csv(DATA_DIR / "ipc.csv", index=False)

# 6. Empresas constituidas
constituidas = pd.DataFrame({
    "id_const": range(1, 301),
    "id_tiempo": rng.integers(202401, 202413, 300),
    "tipo": rng.choice(["S.A.", "S.L.", "S.Com./S.C."], 300),
    "numero_sociedades": rng.integers(100, 5000, 300),
    "capital": rng.integers(50000, 5_000_000, 300),
    "id_territorio": rng.integers(1, 21, 300),
})
constituidas.to_csv(DATA_DIR / "empresas_constituidas.csv", index=False)

# 7. Empresas disueltas
disueltas = pd.DataFrame({
    "id_dis": range(1, 301),
    "id_tiempo": rng.integers(202401, 202413, 300),
    "razon": rng.choice(["voluntaria", "por_fusion", "otras"], 300),
    "numero_sociedades": rng.integers(10, 1000, 300),
    "id_territorio": rng.integers(1, 21, 300),
})
disueltas.to_csv(DATA_DIR / "empresas_disueltas.csv", index=False)

print(f"Datos de prueba generados en {DATA_DIR}")