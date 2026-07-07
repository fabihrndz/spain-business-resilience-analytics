# Spain Business Resilience Analytics

Análisis de la resiliencia empresarial en España mediante datos del INE (IPC, sociedades constituidas y disueltas) utilizando un modelo dimensional en esquema estrella.

## Descripción

Proyecto que extrae, transforma y modela datos del Instituto Nacional de Estadística para analizar indicadores económicos clave y la evolución del tejido empresarial español.

## Estructura del proyecto

| Archivo | Descripción |
|---|---|
| `conexion_api.py` | Módulo Python para llamadas a la API del INE con logging |
| `01_extraccion.ipynb` | ETL del IPC — construye modelo dimensional |
| `02_extracion.ipynb` | ETL de sociedades constituidas |
| `03_extraccion.ipynb` | ETL de sociedades disueltas |
| `documentacion.md` | Notas legales sobre disolución de sociedades |

## Datos generados

- `ipc.csv` — Tabla de hechos con valores del IPC
- Dimensiones: `tiempo.csv`, `territorio.csv`, `sectores_ipc.csv`, `tipo_medida.csv`
- `empresas_constituidas.csv` / `empresas_disueltas.csv`

## Modelo de datos

Esquema estrella con tabla de hechos `ipc` y dimensiones de tiempo, territorio, sector y tipo de medida.

## Stack tecnológico

Python 3.12, pandas, requests, Jupyter Notebook, API REST del INE.

## Instalación

```bash
pip install pandas requests jupyter
```

## Uso

Ejecutar los notebooks en orden: `01_extraccion.ipynb` → `02_extracion.ipynb` → `03_extraccion.ipynb`

## Fuente de datos

[API JSON del INE](https://www.ine.es/dyngs/ODE/es/index.htm) — TABLA_76136 (IPC), TABLA_13913 (constituidas), TABLA_13915 (disueltas).

## Licencia

MIT
