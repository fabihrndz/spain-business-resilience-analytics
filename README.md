# Spain Business Resilience Analytics

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=flat&logo=jupyter&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

AnÃ¡lisis de la resiliencia empresarial en EspaÃ±a mediante datos del INE (IPC, sociedades constituidas y disueltas) utilizando un modelo dimensional en esquema estrella.

## DescripciÃ³n

Proyecto que extrae, transforma y modela datos del Instituto Nacional de EstadÃ­stica para analizar indicadores econÃ³micos clave y la evoluciÃ³n del tejido empresarial espaÃ±ol.

### Fuentes de datos

| Dataset | Tabla INE | DescripciÃ³n |
|---------|-----------|-------------|
| IPC | 76136 | Ãndice de Precios al Consumo por territorio y sector |
| Sociedades constituidas | 13913 | CreaciÃ³n de empresas mercantiles mensual |
| Sociedades disueltas | 13915 | DisoluciÃ³n de empresas mercantiles mensual |

## Estructura del proyecto

```
spain-business-resilience-analytics/
â”œâ”€â”€ src/                               # MÃ³dulos Python reutilizables
â”‚   â”œâ”€â”€ api/
â”‚   â”‚   â”œâ”€â”€ connection_api.py          # ConexiÃ³n a la API del INE con cachÃ© y logging
â”‚   â”‚   â””â”€â”€ config.py                  # URLs de la API del INE
â”‚   â”œâ”€â”€ correlation/
â”‚   â”‚   â””â”€â”€ correlation.py             # AnÃ¡lisis de correlaciÃ³n entre variables
â”‚   â”œâ”€â”€ load/
â”‚   â”‚   â””â”€â”€ load_db.py                 # Carga a MySQL (CRUD, PKs, FKs)
â”‚   â””â”€â”€ transformation/
â”‚       â”œâ”€â”€ trans_normal.py            # NormalizaciÃ³n de strings (acentos, guiones)
â”‚       â””â”€â”€ trans_str.py               # ConversiÃ³n de tipos (int â†’ str)
â”œâ”€â”€ notebooks/                         # Pipeline ETL en orden numÃ©rico
â”‚   â”œâ”€â”€ 01_extraction_ipc.ipynb        # ExtracciÃ³n IPC (modelo dimensional)
â”‚   â”œâ”€â”€ 02_extraction_constituidas.ipynb  # ExtracciÃ³n sociedades constituidas
â”‚   â”œâ”€â”€ 03_extraction_disueltas.ipynb  # ExtracciÃ³n sociedades disueltas
â”‚   â”œâ”€â”€ 04_eda.ipynb                   # AnÃ¡lisis exploratorio de datos
â”‚   â”œâ”€â”€ 05_transformation.ipynb        # TransformaciÃ³n y limpieza
â”‚   â”œâ”€â”€ 06_Visualizations.ipynb        # GrÃ¡ficos y visualizaciones
â”‚   â”œâ”€â”€ 07_correlation.ipynb           # AnÃ¡lisis de correlaciÃ³n
â”‚   â””â”€â”€ 08_load.ipynb                  # Carga a base de datos
â”œâ”€â”€ tests/                             # Tests de validaciÃ³n de datos
â”‚   â”œâ”€â”€ conftest.py                    # Fixtures compartidos
â”‚   â”œâ”€â”€ test_types.py                  # ValidaciÃ³n de tipos de columna
â”‚   â”œâ”€â”€ test_ranges.py                 # ValidaciÃ³n de rangos numÃ©ricos
â”‚   â”œâ”€â”€ test_duplicates.py             # DetecciÃ³n de duplicados
â”‚   â””â”€â”€ test_fk_integrity.py           # Integridad de claves forÃ¡neas
â”œâ”€â”€ files/
â”‚   â”œâ”€â”€ data_raw/                      # CSVs extraÃ­dos (sin transformar)
â”‚   â”œâ”€â”€ data_processed/                # CSVs transformados y limpios
â”‚   â””â”€â”€ cache/                         # CachÃ© de respuestas de la API
â”œâ”€â”€ data_base/
â”‚   â””â”€â”€ BBDD_spanish_ipc_analitic2.sql # Script de creaciÃ³n de la base de datos
â”œâ”€â”€ topojson/
â”‚   â””â”€â”€ provincias_spain.geojson       # GeoJSON de provincias para mapas
â”œâ”€â”€ documentation/
â”‚   â”œâ”€â”€ documentation.md               # DocumentaciÃ³n tÃ©cnica completa
â”‚   â”œâ”€â”€ dictionary.md                  # Diccionario de datos
â”‚   â””â”€â”€ Conclusiones_EDA1_ETL.md       # Conclusiones del EDA y ETL
â”œâ”€â”€ dashboard_power_bi.pbix            # Dashboard interactivo en Power BI
â”œâ”€â”€ run_pipeline.py                    # Ejecutor del pipeline completo
â”œâ”€â”€ requirements.txt                   # Dependencias del proyecto
â”œâ”€â”€ .env.example                       # Plantilla de credenciales
â”œâ”€â”€ .env                               # Credenciales de base de datos (no versionado)
â””â”€â”€ .gitignore                         # Archivos ignorados
```

## Stack tecnolÃ³gico

- **Lenguaje**: Python 3.12
- **Procesamiento**: pandas, numpy
- **API**: requests (API REST JSON del INE)
- **VisualizaciÃ³n**: matplotlib, seaborn
- **Base de datos**: SQLAlchemy, PyMySQL
- **Notebooks**: Jupyter Notebook
- **Dashboard**: Power BI

## InstalaciÃ³n

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/spain-business-resilience-analytics.git
cd spain-business-resilience-analytics

# Instalar dependencias
pip install -r requirements.txt
```

## ConfiguraciÃ³n

1. Copiar el archivo de plantilla de credenciales:

```bash
cp .env.example .env
```

2. Editar `.env` con los datos de conexiÃ³n a MySQL:

```
DB_HOST=localhost
DB_PORT=3306
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseÃ±a
DB_NAME=ipc_analisis_empresarial
```

## Uso

### EjecuciÃ³n manual (notebooks)

Ejecutar los notebooks en orden secuencial (01 â†’ 08):

```bash
jupyter notebook notebooks/01_extraction_ipc.ipynb
```

### EjecuciÃ³n automatizada (pipeline)

```bash
python run_pipeline.py
```

Ejecuta todos los notebooks del pipeline en orden y reporta Ã©xitos/fallos.

## Tests

```bash
pytest tests/ -v
```

Los tests validan:
- **Tipos de columna**: Cada DataFrame tiene los tipos esperados
- **Rangos numÃ©ricos**: Valores dentro de rangos lÃ³gicos
- **Duplicados**: No hay filas duplicadas en tablas clave
- **Integridad referencial**: Las claves forÃ¡neas apuntan a registros existentes

## Modelo de datos

Esquema estrella con tabla de hechos `ipc` y dimensiones de tiempo, territorio, sector y tipo de medida. Las tablas de empresas constituidas y disueltas tambiÃ©n referencian las dimensiones temporal y geogrÃ¡fica.

```
                          â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                          â”‚   tiempo     â”‚
                          â”‚â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”‚
                          â”‚ id_tiempo PK â”‚
                          â”‚ anio         â”‚
                          â”‚ mes          â”‚
                          â”‚ nombre_mes   â”‚
                          â””â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”˜
                                 â”‚
               â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
               â”‚                 â”‚                 â”‚
               â–¼                 â–¼                 â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚empresas_const.   â”‚  â”‚     ipc          â”‚  â”‚empresas_disuelt. â”‚
â”‚â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”‚  â”‚â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”‚  â”‚â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”‚
â”‚ id_const    PK   â”‚  â”‚ id_ipc      PK   â”‚  â”‚ id_dis      PK   â”‚
â”‚ id_tiempo    FK  â”‚  â”‚ id_tiempo    FK  â”‚  â”‚ id_tiempo    FK  â”‚
â”‚ id_territ    FK  â”‚  â”‚ id_territ    FK  â”‚  â”‚ id_territ    FK  â”‚
â”‚ tipo             â”‚  â”‚ id_sector    FK  â”‚  â”‚ razon            â”‚
â”‚ num_sociedades   â”‚  â”‚ id_medida    FK  â”‚  â”‚ num_sociedades   â”‚
â”‚ capital          â”‚  â”‚ valor_ipc        â”‚  â”‚                  â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
               â–²                 â–²    â–²            â–²
               â”‚                 â”‚    |____________|____________
               â”‚                 â”‚                 â”‚           |
               â”‚        â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”         â”‚           |
               â”‚        â”‚                â”‚         â”‚           |
               â”‚        |                |         â”‚           |
               â”‚ â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”‚           |
               â””â”€â”‚  territorio  â”‚ â”‚sectores_ipc  â”‚ â”‚           |
                 â”‚â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”‚ â”‚â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”‚ â”‚           |
                 â”‚id_territorio â”‚ â”‚id_sector  PK â”‚ â”‚           |
                 â”‚       PK     â”‚ â”‚nombre_sector â”‚ â”‚           |
                 â”‚nombre_territ.â”‚ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â”‚           |
                 â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜                  â”‚           |
                        |__________________________â”‚           |
                                                               |
                                  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”             |
                                  â”‚ tipo_medida  â”‚             |
                                  â”‚â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”‚             |
                                  â”‚id_medida  PK â”‚_____________|
                                  â”‚nombre_medida â”‚
                                  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

## Fuente de datos

[API JSON del INE](https://www.ine.es/dyngs/ODE/es/index.htm) â€” TABLA_76136 (IPC), TABLA_13913 (constituidas), TABLA_13915 (disueltas).

## Licencia

MIT
