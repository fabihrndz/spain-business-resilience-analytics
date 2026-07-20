# Spain Business Resilience Analytics

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=flat&logo=jupyter&logoColor=white)
![License](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey)

Análisis de la resiliencia empresarial en España mediante datos del INE (IPC, sociedades constituidas y disueltas) utilizando un modelo dimensional en esquema estrella.

## Descripción

Proyecto que extrae, transforma y modela datos del Instituto Nacional de Estadística para analizar indicadores económicos clave y la evolución del tejido empresarial español.

### Fuentes de datos

| Dataset | Tabla INE | Descripción |
|---------|-----------|-------------|
| IPC | 76136 | Índice de Precios al Consumo por territorio y sector |
| Sociedades constituidas | 13913 | Creación de empresas mercantiles mensual |
| Sociedades disueltas | 13915 | Disolución de empresas mercantiles mensual |

## Estructura del proyecto

```
spain-business-resilience-analytics/
+-- src/                           # Módulos Python reutilizables
|   +-- api/
|   |   +-- connection_api.py      # Conexión a la API del INE con caché y logging
|   |   +-- config.py              # URLs de la API del INE
|   +-- transformation/
|   |   +-- trans_normal.py        # Normalización de strings
|   |   +-- trans_str.py           # Conversión de tipos
|   +-- load/
|   |   +-- load_db.py             # Carga a MySQL (CRUD, PKs, FKs)
|   +-- correlation/
|       +-- correlation.py         # Análisis de correlación
+-- notebooks/                     # Pipeline ETL en orden numérico
|   +-- 01_extraction_ipc.ipynb
|   +-- 02_extraction_constituidas.ipynb
|   +-- 03_extraction_disueltas.ipynb
|   +-- 04_eda.ipynb
|   +-- 05_transformation.ipynb
|   +-- 06_visualizations.ipynb
|   +-- 07_correlation.ipynb
|   +-- 08_load.ipynb
+-- tests/                         # Tests de validación y unit tests
|   +-- conftest.py
|   +-- test_types.py               # Validación de tipos de columnas
|   +-- test_ranges.py              # Validación de rangos de valores
|   +-- test_duplicates.py          # Detección de duplicados
|   +-- test_fk_integrity.py        # Integridad referencial (FK)
|   +-- test_trans_normal.py        # Unit tests: normalizar_col
|   +-- test_trans_str.py           # Unit tests: int_a_str
|   +-- test_correlation.py         # Unit tests: comparar_correlaciones
|   +-- test_connection_api.py      # Unit tests: llamada_api (mock)
+-- files/
|   +-- data_raw/                  # CSVs extraídos (sin transformar)
|   +-- data_processed/            # CSVs transformados y limpios
|   +-- cache/                     # Caché de llamadas a la API
+-- data_base/
|   +-- BBDD_spanish_ipc_analitic2.sql
+-- documentation/
|   +-- documentation.md           # Documentación técnica completa
|   +-- Conclusiones_EDA1_ETL.md   # Conclusiones del EDA
|   +-- dictionary.md              # Diccionario de datos
+-- topojson/
|   +-- provincias_spain.geojson   # Mapa de provincias para visualizaciones
+-- dashboard_power_bi.pbix        # Dashboard en Power BI
+-- requirements.txt               # Dependencias del proyecto
+-- run_pipeline.py                # Ejecutor del pipeline completo
+-- CHANGELOG.md                   # Historial de cambios
+-- .env.example                   # Plantilla de credenciales
+-- .gitignore                     # Archivos ignorados
```

## Stack tecnológico

Python 3.12, pandas, numpy, requests, SQLAlchemy, PyMySQL, Jupyter Notebook, seaborn, matplotlib, pytest.

## Instalación

```bash
pip install -r requirements.txt
```

## Configuración

Copiar el archivo `.env.example` como `.env` y completar las credenciales de base de datos:

```
DB_USER=root
DB_PASSWORD=tu_password
DB_HOST=127.0.0.1
DB_NAME=ipc_analisis_empresarial
```

## Uso

### Ejecutar el pipeline completo

```bash
python run_pipeline.py
```

### Ejecutar notebooks individualmente

```bash
jupyter notebook notebooks/01_extraction_ipc.ipynb
```

### Ejecutar tests

```bash
pytest tests/ -v
```

## Modelo de datos

Esquema estrella con tabla de hechos `ipc` y dimensiones:

- `tiempo` — Dimensión temporal (año, mes)
- `territorio` — Dimensión geográfica (comunidades autónomas)
- `sectores_ipc` — Dimensión de sectores del IPC
- `tipo_medida` — Dimensión de tipos de medida

Tablas de hechos adicionales:
- `empresas_constituidas` — Creación de empresas por mes y territorio
- `empresas_disueltas` — Disolución de empresas por mes y territorio

## Fuente de datos

[API JSON del INE](https://www.ine.es/dyngs/ODE/es/index.htm) — TABLA_76136 (IPC), TABLA_13913 (constituidas), TABLA_13915 (disueltas).

## Licencia

CC BY-NC-SA 4.0
