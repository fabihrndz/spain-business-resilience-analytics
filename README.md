# Spain Business Resilience Analytics

Análisis de la resiliencia empresarial en España mediante datos del INE (IPC, sociedades constituidas y disueltas) utilizando un modelo dimensional en esquema estrella.

## Descripción

Proyecto que extrae, transforma y modela datos del Instituto Nacional de Estadística para analizar indicadores económicos clave y la evolución del tejido empresarial español.

## Estructura del proyecto

```
spain-business-resilience-analytics/
├── src/                           # Módulos Python reutilizables
│   ├── api/conection_api.py       # Conexión a la API del INE con logging
│   ├── transformacion/
│   │   ├── trans_normal.py        # Normalización de strings
│   │   └── trans_str.py           # Conversión de tipos
│   └── load/load_db.py            # Carga a MySQL (CRUD, PKs, FKs)
├── notebooks/                     # Pipeline ETL en orden numérico
│   ├── 01_extraction_ipc.ipynb
│   ├── 02_extraction_constituidas.ipynb
│   ├── 03_extraction_disueltas.ipynb
│   ├── 04_eda.ipynb
│   ├── 05_transformation.ipynb
│   └── 06_load.ipynb
├── files/
│   ├── data_raw/                  # CSVs extraídos (sin transformar)
│   └── data_processed/            # CSVs transformados y limpios
├── documentation/
│   ├── documentation.md           # Documentación técnica completa
│   └── dictionary.md              # Diccionario de datos
├── requirements.txt               # Dependencias del proyecto
├── .env                           # Credenciales de base de datos
└── .gitignore                     # Archivos ignorados
```

## Stack tecnológico

Python 3.12, pandas, requests, Jupyter Notebook, SQLAlchemy, PyMySQL, API REST del INE.

## Instalación

```bash
pip install -r requirements.txt
```

## Configuración

Crear un archivo `.env` en la raíz del proyecto con:

```
DB_USER=root
DB_PASSWORD=tu_contraseña
DB_HOST=127.0.0.1
DB_NAME=ipc_analisis_empresarial
```

## Uso

Ejecutar los notebooks en orden secuencial con Jupyter:

```bash
jupyter notebook notebooks/01_extraction_ipc.ipynb
```

## Datos generados

- `ipc.csv` — Tabla de hechos con valores del IPC (esquema estrella)
- Dimensiones: `tiempo.csv`, `territorio.csv`, `sectores_ipc.csv`, `tipo_medida.csv`
- `empresas_constituidas.csv` / `empresas_disueltas.csv`

## Modelo de datos

Esquema estrella con tabla de hechos `ipc` y dimensiones de tiempo, territorio, sector y tipo de medida. Las tablas de empresas referencian la dimensión temporal mediante `id_tiempo`.

## Fuente de datos

[API JSON del INE](https://www.ine.es/dyngs/ODE/es/index.htm) — TABLA_76136 (IPC), TABLA_13913 (constituidas), TABLA_13915 (disueltas).

## Licencia

MIT
