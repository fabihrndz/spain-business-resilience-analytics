# Spain Business Resilience Analytics

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=flat&logo=jupyter&logoColor=white)
![License](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey)

Análisis de la resiliencia empresarial en España mediante datos del INE (IPC, sociedades constituidas y disueltas) utilizando un modelo dimensional en esquema estrella.

## Fuentes de datos

| Dataset | Tabla INE | Descripción |
|---------|-----------|-------------|
| IPC | 76136 | Índice de Precios al Consumo por territorio y sector |
| Sociedades constituidas | 13913 | Creación de empresas mercantiles mensual |
| Sociedades disueltas | 13915 | Disolución de empresas mercantiles mensual |

## Requisitos previos

- Python 3.12
- MySQL 8.0+

## Instalación

```bash
pip install -r requirements.txt
```

## Configuración

Copiar `.env.example` como `.env` y completar las credenciales:

```
DB_USER=root
DB_PASSWORD=tu_password
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=ipc_analisis_empresarial
```

## Ejecución

### Pipeline completo

```bash
python run_pipeline.py
```

### Notebooks individualmente

```bash
jupyter notebook notebooks/01_extraction_ipc.ipynb
```

### Tests

```bash
pytest tests/ -v
```

## Estructura del proyecto

```
spain-business-resilience-analytics/
├── src/                           # Módulos Python reutilizables
│   ├── api/
│   │   ├── connection_api.py      # Conexión a la API del INE con caché
│   │   └── config.py              # URLs de la API del INE
│   ├── transformation/
│   │   ├── trans_normal.py        # Normalización de strings
│   │   └── trans_str.py           # Conversión de tipos
│   ├── load/
│   │   └── load_db.py             # Carga a MySQL (CRUD, PKs, FKs)
│   └── correlation/
│       └── correlation.py         # Análisis de correlación
├── notebooks/                     # Pipeline ETL en orden numérico
│   ├── 01_extraction_ipc.ipynb
│   ├── 02_extraction_constituidas.ipynb
│   ├── 03_extraction_disueltas.ipynb
│   ├── 04_eda.ipynb
│   ├── 05_transformation.ipynb
│   ├── 06_visualizations.ipynb
│   ├── 07_correlation.ipynb
│   └── 08_load.ipynb
├── tests/                         # Tests de validación y unit tests
│   ├── conftest.py
│   ├── test_types.py
│   ├── test_ranges.py
│   ├── test_duplicates.py
│   ├── test_fk_integrity.py
│   ├── test_trans_normal.py
│   ├── test_trans_str.py
│   ├── test_correlation.py
│   └── test_connection_api.py
├── files/
│   ├── data_raw/                  # CSVs extraídos (sin transformar)
│   ├── data_processed/            # CSVs transformados y limpios
│   └── cache/                     # Caché de llamadas a la API
├── data_base/
│   └── BBDD_spanish_ipc_analitic2.sql
├── documentation/
│   ├── documentation_v2.md        # Documentación técnica completa
│   ├── Conclusiones_EDA1_ETL.md   # Conclusiones del EDA
│   └── dictionary.md              # Diccionario de datos
├── topojson/
│   └── provincias_spain.geojson   # Mapa de provincias
├── dashboard_power_bi.pbix        # Dashboard en Power BI
├── requirements.txt               # Dependencias del proyecto
├── run_pipeline.py                # Ejecutor del pipeline completo
├── CHANGELOG.md                   # Historial de cambios
├── .env.example                   # Plantilla de credenciales
└── .gitignore                     # Archivos ignorados
```

## Documentación técnica

Para detalles completos sobre módulos, notebooks, modelo de datos y tests, consulta [documentation_v2.md](documentation/documentation_v2.md).

## Licencia

CC BY-NC-SA 4.0
