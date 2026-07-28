# Documentación del Proyecto: Spain Business Resilience Analytics

## Módulo: `conexion_api.py`

### Descripción

Módulo Python que encapsula las llamadas a la API JSON del INE. Proporciona una función única con logging y manejo de errores.

### Función: `llamada_api(url)`

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `url` | `str` | URL completa del endpoint de la API del INE |

**Retorno**: `dict | list | None` — Datos JSON parseados si la respuesta es 200, `None` en caso de error.

**Logging**:
- `INFO` — Inicio de llamada y código de estado recibido
- `DEBUG` — Primeros 300 caracteres del payload (solo en éxito)
- `WARNING` — Código de estado inesperado
- `ERROR` — Timeout o error de conexión

**Errores manejados**:
- `requests.exceptions.Timeout`
- `requests.exceptions.RequestException`

### Dependencias

- `requests`
- `logging` (stdlib)

---

## Notebook 01: `01_extraccion.ipynb` — IPC (Tabla 76136)

### Fuente de datos

```
https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/76136?nlast=60&det=2
```

### Proceso ETL

1. **Extracción**: Llama a la API del INE con el módulo `conexion_api` y obtiene una lista de series temporales. Cada serie tiene un `Nombre` compuesto por tres partes separadas por punto: `Territorio.Sector.TipoMedida`.

2. **Construcción de dimensiones**:
   - **`tiempo`**: Extrae `CodigoPeriodo`, `Anyo`, `Mes_inicio` y `Nombre_largo` del mes desde cada punto de datos. Usa `CodigoPeriodo` como clave primaria (formato `YYYYMM`).
   - **`territorio`**: Toma la primera parte del nombre de la serie (ej: `Total Nacional`, `Andalucía`). Asigna IDs autoincrementales.
   - **`sectores_ipc`**: Toma la segunda parte del nombre (ej: `Índice General`, `Alimentos`). Asigna IDs autoincrementales.
   - **`tipo_medida`**: Toma la tercera parte del nombre (ej: `General`, `Variación anual`). Asigna IDs autoincrementales.

3. **Construcción de la tabla de hechos `ipc`**:
   - Para cada serie, recorre todos sus puntos `Data`.
   - Mapea el nombre del territorio a su ID (con corrección: `Nacional` → `Total Nacional`).
   - Combina `id_tiempo`, `id_territorio`, `id_sector`, `id_medida` y `valor_ipc`.


### Archivos generados

| Archivo | Descripción |
|---------|-------------|
| `tiempo.csv` | Dimensión temporal (periodos mensuales) |
| `territorio.csv` | Dimensión geográfica (comunidades autónomas + total nacional) |
| `sectores_ipc.csv` | Dimensión de sectores económicos del IPC |
| `tipo_medida.csv` | Dimensión de tipos de medida (general, variación, etc.) |
| `ipc.csv` | Tabla de hechos con valores del IPC |

---

## Notebook 02: `02_extracion.ipynb` — Sociedades Constituidas (Tabla 13913)

### Fuente de datos

```
https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/13913
```

### Proceso

1. Llama a la API del INE para obtener datos de **sociedades mercantiles constituidas** (creadas).
2. Para cada serie, extrae el nombre descriptivo (territorio y tipo) y recorre todos los datos históricos.
3. Genera el archivo `empresas_constituidas.csv` con estructura:
   - `Nombre` — descripción de la serie (ej: `Andalucía. Sociedades Constituídas. Mercantiles. Número de Sociedades.`)
   - `FK_TipoDato` — tipo de dato (1: provisional, 2: estimación)
   - `FK_Periodo` — número de mes
   - `Anyo` — año
   - `Valor` — número de sociedades constituidas
   - `Fecha` — timestamp UNIX en milisegundos

### Cobertura temporal

Desde **enero de 2002** hasta la actualidad (2026), con datos mensuales.

### Datos destacables

- Máximo histórico en marzo de 2007: **16.165** sociedades constituidas en un mes
- Mínimo en abril de 2020 (COVID-19): **386** sociedades constituidas
- Promedio mensual aprox. 8.000–10.000 sociedades

### Archivos generados

| Archivo | Descripción |
|---------|-------------|
| `empresas_constituidas.csv` | Creación de empresas por mes y territorio

---

## Notebook 03: `03_extraccion.ipynb` — Sociedades Disueltas (Tabla 13915)

### Fuente de datos

```
https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/13915
```

### Proceso

1. Llama a la API del INE para obtener datos de **sociedades mercantiles disueltas**.
2. Para cada serie (80 series disponibles por comunidad autónoma y tipo), extrae los datos y los imprime en formato estructurado.
3. **Estructura de los datos**: `Nombre, FK_TipoDato, FK_Periodo, Anyo, Valor`
   - Ejemplo: `Total. Disueltas. Número de Sociedades. Mercantiles. Total Nacional., 1, 4, 2026, 2064.0`

### Cobertura temporal

Desde **enero de 2002** hasta la actualidad (2026), con datos mensuales.

### Datos destacables

- Máximo en enero de 2019: **4.157** sociedades disueltas
- Mínimo en mayo de 2020 (COVID-19): **482** sociedades disueltas (anomalía a la baja por restricciones)
- Tendencia general: 1.500–2.500 disoluciones mensuales en los últimos años

### Archivos generados

| Archivo | Descripción |
|---------|-------------|
| `empresas_disueltas.csv` |Disolución de empresas por mes y territorio

---
## Stack Tecnológico

| Componente | Versión |
|------------|---------|
| Python | 3.12 |
| pandas | Última estable |
| requests | Última estable |
| Jupyter Notebook | Última estable |
| API INE | REST JSON (wstempus) |

## Instalación

```bash
pip install pandas requests jupyter
```

## Uso

Ejecutar los notebooks en orden secuencial:

```bash
jupyter notebook 01_extraccion.ipynb      # IPC - modelo dimensional
jupyter notebook 02_extracion.ipynb       # Sociedades constituidas
jupyter notebook 03_extraccion.ipynb      # Sociedades disueltas
jupyter notebook 04_eda.ipynb             # Realización EDA
jupyter notebook 05_transformation.ipynb  # Transformación datasets
jupyter notebook 06_visualizations.ipynb  # Análisis de visualizaciones
jupyter notebook 07_correlation.ipynb     # Análisis correlación
jupyter notebook 08_load.ipynb            # Carga datasets a MySQL
```

Los archivos CSV se generan automáticamente en el directorio raíz del proyecto.

## Fuentes de Datos

- **API JSON del INE**: https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/
- **Tabla 76136**: Índice de Precios al Consumo (IPC) — series por territorio y sector
- **Tabla 13913**: Sociedades mercantiles constituidas
- **Tabla 13915**: Sociedades mercantiles disueltas
- **Documentación API**: https://www.ine.es/dyngs/ODE/es/index.htm
