# Documentación Técnica: Spain Business Resilience Analytics

## Arquitectura general

El proyecto sigue un flujo ETL (Extract, Transform, Load):

1. **Extracción**: Datos de la API JSON del INE → CSVs en `files/data_raw/`
2. **EDA y Transformación**: Limpieza, normalización, modelo dimensional → CSVs en `files/data_processed/`
3. **Visualización y Análisis**: Gráficos, correlaciones
4. **Carga**: CSVs → MySQL con esquema estrella

---

## Módulos `src/`

### `api/connection_api.py`

Funciones para conectarse a la API del INE con sistema de caché.

#### `llamada_api(url: str) -> dict | list | None`

Realiza una llamada a la API del INE con caché local.

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `url` | `str` | URL completa del endpoint de la API |

**Retorno**: Datos JSON parseados o `None` en caso de error.

**Comportamiento**:
- Consulta caché en `files/cache/{table_id}.json`
- Si no existe, realiza petición HTTP
- Guarda resultado en caché para futuras llamadas

**Logging**:
- `INFO`: Inicio de llamada y código de estado
- `WARNING`: Caché corrupto o estado inesperado
- `ERROR`: Timeout o error de conexión

**Errores manejados**:
- `requests.exceptions.Timeout`
- `requests.exceptions.RequestException`

#### `_get_cache_path(url: str) -> str`

Extrae el ID de tabla de la URL y devuelve la ruta al archivo de caché.

---

### `api/config.py`

Constantes de configuración de la API.

```python
INE_BASE_URL = "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA"

API_URLS = {
    "ipc": f"{INE_BASE_URL}/76136?nlast=60&det=2",
    "constituidas": f"{INE_BASE_URL}/13913",
    "disueltas": f"{INE_BASE_URL}/13915",
}
```

---

### `transformation/trans_normal.py`

#### `normalizar_col(col: str) -> str`

Normaliza strings para nombres de columnas.

**Proceso**:
1. Elimina espacios al inicio/final, convierte a minúsculas
2. Elimina acentos (NFKD + ASCII)
3. Reemplaza espacios y guiones por guiones bajos
4. Elimina caracteres especiales

**Ejemplo**:
```python
normalizar_col("  Índice General - Variación  ")  # → "indice_general_variacion"
```

---

### `transformation/trans_str.py`

#### `int_a_str(df: pd.DataFrame, lista_columnas: list[str]) -> pd.DataFrame`

Convierte columnas especificadas a tipo string.

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `df` | `pd.DataFrame` | DataFrame de entrada |
| `lista_columnas` | `list[str]` | Nombres de columnas a convertir |

**Logging**:
- `INFO`: Columna convertida exitosamente
- `WARNING`: Columna no encontrada en el DataFrame

---

### `load/load_db.py`

Funciones para cargar datos en MySQL.

#### `get_connection_string(...) -> str`

Genera la URL de conexión a MySQL desde variables de entorno.

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `db_name` | `str \| None` | Nombre de la base de datos |
| `user` | `str \| None` | Usuario (default: `DB_USER` env) |
| `password` | `str \| None` | Password (default: `DB_PASSWORD` env) |
| `host` | `str \| None` | Host (default: `DB_HOST` env) |
| `port` | `str \| None` | Puerto (default: `3306`) |

#### `create_database_if_not_exists(db_name: str) -> None`

Crea la base de datos si no existe.

#### `load_dataframe_to_mysql(df, table_name, db_name, if_exists="replace") -> None`

Carga un DataFrame en una tabla MySQL.

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `df` | `pd.DataFrame` | Datos a cargar |
| `table_name` | `str` | Nombre de la tabla destino |
| `db_name` | `str` | Nombre de la base de datos |
| `if_exists` | `str` | `"replace"`, `"append"` o `"fail"` |

#### `set_primary_key(table_name, pk_column, db_name, data_type="INT") -> None`

Define una columna como clave primaria.

#### `set_foreign_keys(fact_table, relations, db_name) -> None`

Crea relaciones de clave foránea (modelo estrella).

```python
relations = [
    {"fk_column": "id_tiempo", "dimension_table": "tiempo"},
    {"fk_column": "id_territorio", "dimension_table": "territorio"},
]
```

#### `add_autoincrement_id(table_name, db_name) -> None`

Agrega columna autoincremental como PK.

#### `drop_all_tables(db_name, tables) -> None`

Elimina tablas en orden inverso para respetar FKs.

---

### `correlation/correlation.py`

Funciones de análisis de correlación.

#### `comparar_correlaciones(df, var1_name, var2_name, umbral_diferencia=0.1, mostrar_plot=True) -> dict`

Compara correlaciones Pearson y Spearman, recomienda la más adecuada.

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `df` | `pd.DataFrame` | DataFrame con las variables |
| `var1_name` | `str` | Nombre de la primera columna |
| `var2_name` | `str` | Nombre de la segunda columna |
| `umbral_diferencia` | `float` | Umbral para recomendar Spearman (default: 0.1) |
| `mostrar_plot` | `bool` | Mostrar scatter plot (default: True) |

**Retorno**: dict con `pearson`, `spearman`, `diferencia`, `recomendacion`, `interpretacion`.

**Lógica**:
- Si diferencia < umbral → Pearson (relación lineal)
- Si diferencia ≥ umbral → Spearman (outliers o no lineal)

#### `matriz_correlacion_visual(df, metodo='pearson', ...) -> pd.DataFrame`

Genera heatmap de matriz de correlación.

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `df` | `pd.DataFrame` | Variables numéricas |
| `metodo` | `str` | `'pearson'`, `'spearman'` o `'kendall'` |
| `solo_triangulo` | `bool` | Mostrar solo triángulo inferior (default: True) |

---

## Notebooks

### 01_extraction_ipc.ipynb — IPC (Tabla 76136)

**Fuente**: `https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/76136?nlast=60&det=2`

**Proceso ETL**:
1. Extrae series temporales de la API
2. Cada serie tiene `Nombre` compuesto: `Territorio.Sector.TipoMedida`
3. Construye dimensiones:
   - `tiempo` (PK: `CodigoPeriodo` formato YYYYMM)
   - `territorio` (IDs autoincrementales)
   - `sectores_ipc`
   - `tipo_medida`
4. Construye tabla de hechos `ipc` con valores del índice

**Archivos generados**: `tiempo.csv`, `territorio.csv`, `sectores_ipc.csv`, `tipo_medida.csv`, `ipc.csv`

---

### 02_extraction_constituidas.ipynb — Sociedades Constituidas (Tabla 13913)

**Fuente**: `https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/13913`

**Proceso**:
1. Extrae datos de sociedades mercantiles constituidas
2. Para cada serie, extrae nombre descriptivo y datos históricos
3. Genera CSV con: `Nombre`, `FK_TipoDato`, `FK_Periodo`, `Anyo`, `Valor`, `Fecha`

**Cobertura**: Enero 2002 – actualidad (mensual)

**Datos destacables**:
- Máximo: 16.165 (marzo 2007)
- Mínimo: 386 (abril 2020, COVID-19)

**Archivo generado**: `empresas_constituidas.csv`

---

### 03_extraction_disueltas.ipynb — Sociedades Disueltas (Tabla 13915)

**Fuente**: `https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/13915`

**Proceso**:
1. Extrae datos de sociedades mercantiles disueltas
2. 80 series disponibles por comunidad autónoma y tipo

**Cobertura**: Enero 2002 – actualidad (mensual)

**Datos destacables**:
- Máximo: 4.157 (enero 2019)
- Mínimo: 482 (mayo 2020, COVID-19)

**Archivo generado**: `empresas_disueltas.csv`

---

### 04_eda.ipynb — Análisis Exploratorio de Datos

Análisis estadístico descriptivo de los datasets:
- Estadísticas básicas (media, mediana, desviación)
- Distribuciones y histogramas
- Detección de valores nulos y outliers
- Análisis temporal de tendencias

---

### 05_transformation.ipynb — Transformación

Proceso de limpieza y transformación:
- Normalización de columnas con `normalizar_col()`
- Conversión de tipos con `int_a_str()`
- Unión de datasets
- Creación del modelo dimensional

---

### 06_visualizations.ipynb — Visualizaciones

Análisis visual:
- Series temporales de IPC por territorio
- Evolución de sociedades constituidas/disueltas
- Comparativas entre comunidades autónomas
- Mapas coropléticos con GeoJSON

---

### 07_correlation.ipynb — Análisis de Correlación

Análisis de relaciones entre variables:
- Correlación IPC vs empresas constituidas/disueltas
- Comparación Pearson vs Spearman con `comparar_correlaciones()`
- Matrices de correlación con `matriz_correlacion_visual()`

---

### 08_load.ipynb — Carga a MySQL

Carga de datos transformados a base de datos:
- Creación de base de datos con `create_database_if_not_exists()`
- Carga de tablas con `load_dataframe_to_mysql()`
- Definición de PKs con `set_primary_key()`
- Creación de relaciones FK con `set_foreign_keys()`

---

## Modelo de datos

Esquema estrella con tabla de hechos principal `ipc`:

### Tabla de hechos: `ipc`

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `id_ipc` | INT AUTO_INCREMENT | PK |
| `id_tiempo` | INT | FK → tiempo |
| `id_territorio` | INT | FK → territorio |
| `id_sector` | INT | FK → sectores_ipc |
| `id_medida` | INT | FK → tipo_medida |
| `valor_ipc` | FLOAT | Valor del índice |

### Dimensiones

| Tabla | PK | Descripción |
|-------|-----|-------------|
| `tiempo` | `id_tiempo` | Periodos mensuales (YYYYMM) |
| `territorio` | `id_territorio` | Comunidades autónomas |
| `sectores_ipc` | `id_sector` | Sectores económicos del IPC |
| `tipo_medida` | `id_medida` | General, variación, etc. |

### Tablas de hechos adicionales

- `empresas_constituidas` — Creación de empresas por mes y territorio
- `empresas_disueltas` — Disolución de empresas por mes y territorio

### Relaciones FK

```
ipc.id_tiempo      → tiempo.id_tiempo
ipc.id_territorio  → territorio.id_territorio
ipc.id_sector      → sectores_ipc.id_sector
ipc.id_medida      → tipo_medida.id_medida
```

---

## Tests

Los tests se ejecutan con `pytest tests/ -v`. Los datos de prueba se generan automáticamente mediante:

```bash
python scripts/generate_test_data.py
```

Esto crea CSVs dummy en `files/data_processed/` sin necesidad de llamar a la API del INE ni tener MySQL instalado.

### `conftest.py`

Fixtures que cargan CSVs desde `files/data_processed/`:
- `df_tiempo`, `df_territorio`, `df_sectores_ipc`, `df_tipo_medida`
- `df_ipc`, `df_empr_const`, `df_empr_dis`

### Tests de validación

| Archivo | Descripción |
|---------|-------------|
| `test_types.py` | Valida tipos de datos de columnas |
| `test_ranges.py` | Valida rangos de valores numéricos |
| `test_duplicates.py` | Detecta duplicados en tablas |
| `test_fk_integrity.py` | Verifica integridad referencial |

### Tests unitarios

| Archivo | Función testada |
|---------|-----------------|
| `test_trans_normal.py` | `normalizar_col()` |
| `test_trans_str.py` | `int_a_str()` |
| `test_correlation.py` | `comparar_correlaciones()` |
| `test_connection_api.py` | `llamada_api()` (con mock) |

---

## Configuración

### Variables de entorno (`.env`)

```
DB_USER=root
DB_PASSWORD=tu_password
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=ipc_analisis_empresarial
```

### Caché de API

Las llamadas a la API se almacenan en `files/cache/` como archivos JSON. El nombre del archivo corresponde al ID de la tabla INE (ej: `76136.json`).

---

## CI/CD — Integración Continua

El proyecto utiliza **GitHub Actions** para ejecutar linting y tests automáticamente en cada push a `main` y cada pull request.

**Archivo**: `.github/workflows/ci.yml`

**Pasos del pipeline**:
1. Instala Python 3.12 y las dependencias del proyecto
2. Genera datos de prueba con `scripts/generate_test_data.py`
3. Ejecuta Ruff (linter) sobre `src/` y `tests/`
4. Ejecuta `pytest` con cobertura sobre `src/`

El badge de estado del CI se encuentra en la cabecera del `README.md`.

---

## Herramientas de desarrollo

### Ruff (linter y formateador)

Configurado en `pyproject.toml`. Detecta errores de estilo, imports sin usar, docstrings faltantes y sintaxis moderna.

```bash
ruff check src/ tests/          # Analiza el código
ruff check src/ tests/ --fix    # Corrige automáticamente
ruff format src/                # Formatea el código
```

### Pre-commit hooks

Configurado en `.pre-commit-config.yaml`. Ejecuta Ruff automáticamente antes de cada `git commit`:

```bash
pip install pre-commit
pre-commit install
```

### Script de datos de prueba

`scripts/generate_test_data.py` genera datos dummy deterministas en `files/data_processed/` para que los tests funcionen sin conexión a la API del INE ni a MySQL.

---

## Diccionario de datos

Para el diccionario completo de campos, consulta [dictionary.md](dictionary.md).

---

## Fuentes de datos

- **API JSON del INE**: `https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/`
- **Documentación API**: `https://www.ine.es/dyngs/ODE/es/index.htm`
- **Tabla 76136**: IPC por territorio y sector
- **Tabla 13913**: Sociedades mercantiles constituidas
- **Tabla 13915**: Sociedades mercantiles disueltas
