# DocumentaciÃ³n del Proyecto: Spain Business Resilience Analytics

## VisiÃ³n General

Proyecto de anÃ¡lisis de resiliencia empresarial en EspaÃ±a que extrae, transforma y modela datos del **Instituto Nacional de EstadÃ­stica (INE)** a travÃ©s de su API REST pÃºblica. Los datos se estructuran en un modelo dimensional (esquema estrella) para facilitar el anÃ¡lisis de indicadores econÃ³micos y la evoluciÃ³n del tejido empresarial espaÃ±ol.

El proyecto cubre tres Ã¡reas de datos:

1. **IPC (Ãndice de Precios al Consumo)** â€” Tabla INE 76136
2. **Sociedades Constituidas** â€” Tabla INE 13913
3. **Sociedades Disueltas** â€” Tabla INE 13915

---

## Estructura del Proyecto

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
â”‚   â”œâ”€â”€ 06_visualizations.ipynb        # GrÃ¡ficos y visualizaciones
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
â”‚   â”œâ”€â”€ documentation.md               # Este documento
â”‚   â”œâ”€â”€ dictionary.md                  # Diccionario de datos
â”‚   â””â”€â”€ Conclusiones_EDA1_ETL.md       # Conclusiones del EDA y ETL
â”œâ”€â”€ dashboard_power_bi.pbix            # Dashboard interactivo en Power BI
â”œâ”€â”€ run_pipeline.py                    # Ejecutor del pipeline completo
â”œâ”€â”€ requirements.txt                   # Dependencias del proyecto
â”œâ”€â”€ .env.example                       # Plantilla de credenciales
â”œâ”€â”€ .env                               # Credenciales de base de datos (no versionado)
â””â”€â”€ .gitignore                         # Archivos ignorados
```

---

## MÃ³dulo: `src/api/connection_api.py`

### DescripciÃ³n

MÃ³dulo Python que encapsula las llamadas a la API JSON del INE. Proporciona una funciÃ³n Ãºnica con logging, cachÃ© de respuestas y manejo de errores.

### FunciÃ³n: `llamada_api(url)`

| ParÃ¡metro | Tipo | DescripciÃ³n |
|-----------|------|-------------|
| `url` | `str` | URL completa del endpoint de la API del INE |

**Retorno**: `dict | list | None` â€” Datos JSON parseados si la respuesta es 200, `None` en caso de error.

**CachÃ©**: Las respuestas se almacenan en `files/cache/` para evitar llamadas repetidas a la API.

**Logging**:
- `INFO` â€” Inicio de llamada y cÃ³digo de estado recibido
- `WARNING` â€” CÃ³digo de estado inesperado o cachÃ© corrupto
- `ERROR` â€” Timeout o error de conexiÃ³n

**Errores manejados**:
- `requests.exceptions.Timeout`
- `requests.exceptions.RequestException`

### Dependencias

- `requests`
- `logging` (stdlib)
- `json` (stdlib)
- `re` (stdlib)

---

## MÃ³dulo: `src/api/config.py`

Define las URLs de los endpoints de la API del INE para cada dataset (IPC, constituidas, disueltas).

---

## MÃ³dulo: `src/transformation/trans_str.py`

Funciones de conversiÃ³n de tipos de datos. Convierte columnas de IDs de integer a string para tratarlas como categÃ³ricas.

---

## MÃ³dulo: `src/transformation/trans_normal.py`

Funciones de normalizaciÃ³n de texto. Aplica transformationes como: eliminar acentos, convertir a minÃºsculas, reemplazar espacios por guiones bajos y estandarizar nombres de comunidades autÃ³nomas.

---

## MÃ³dulo: `src/correlation/correlation.py`

AnÃ¡lisis de correlaciÃ³n entre las variables del dataset. Genera matrices de correlaciÃ³n y visualizaciones de relaciones entre indicadores econÃ³micos.

---

## MÃ³dulo: `src/load/load_db.py`

Carga de DataFrames a MySQL usando SQLAlchemy. Maneja creaciÃ³n de tablas, claves primarias, claves forÃ¡neas y operaciones CRUD.

---

## Notebooks del Pipeline

### Notebook 01: `01_extraction_ipc.ipynb` â€” IPC (Tabla 76136)

#### Fuente de datos

```
https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/76136?nlast=60&det=2
```

#### Proceso ETL

1. **ExtracciÃ³n**: Llama a la API del INE con el mÃ³dulo `connection_api` y obtiene una lista de series temporales. Cada serie tiene un `Nombre` compuesto por tres partes separadas por punto: `Territorio.Sector.TipoMedida`.

2. **ConstrucciÃ³n de dimensiones**:
   - **`tiempo`**: Extrae `CodigoPeriodo`, `Anyo`, `Mes_inicio` y `Nombre_largo` del mes desde cada punto de datos. Usa `CodigoPeriodo` como clave primaria (formato `YYYYMM`).
   - **`territorio`**: Toma la primera parte del nombre de la serie (ej: `Total Nacional`, `AndalucÃ­a`). Asigna IDs autoincrementales.
   - **`sectores_ipc`**: Toma la segunda parte del nombre (ej: `Ãndice General`, `Alimentos`). Asigna IDs autoincrementales.
   - **`tipo_medida`**: Toma la tercera parte del nombre (ej: `General`, `VariaciÃ³n anual`). Asigna IDs autoincrementales.

3. **ConstrucciÃ³n de la tabla de hechos `ipc`**:
   - Para cada serie, recorre todos sus puntos `Data`.
   - Mapea el nombre del territorio a su ID (con correcciÃ³n: `Nacional` â†’ `Total Nacional`).
   - Combina `id_tiempo`, `id_territorio`, `id_sector`, `id_medida` y `valor_ipc`.

#### Archivos generados

| Archivo | DescripciÃ³n |
|---------|-------------|
| `tiempo.csv` | DimensiÃ³n temporal (periodos mensuales) |
| `territorio.csv` | DimensiÃ³n geogrÃ¡fica (comunidades autÃ³nomas + total nacional) |
| `sectores_ipc.csv` | DimensiÃ³n de sectores econÃ³micos del IPC |
| `tipo_medida.csv` | DimensiÃ³n de tipos de medida (general, variaciÃ³n, etc.) |
| `ipc.csv` | Tabla de hechos con valores del IPC |

---

### Notebook 02: `02_extraction_constituidas.ipynb` â€” Sociedades Constituidas (Tabla 13913)

#### Fuente de datos

```
https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/13913
```

#### Proceso

1. Llama a la API del INE para obtener datos de **sociedades mercantiles constituidas** (creadas).
2. Para cada serie, extrae el nombre descriptivo (territorio y tipo) y recorre todos los datos histÃ³ricos.
3. Genera el archivo `empresas_constituidas.csv`.

#### Cobertura temporal

Desde **enero de 1995** hasta la actualidad (2026), con datos mensuales.

---

### Notebook 03: `03_extraction_disueltas.ipynb` â€” Sociedades Disueltas (Tabla 13915)

#### Fuente de datos

```
https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/13915
```

#### Proceso

1. Llama a la API del INE para obtener datos de **sociedades mercantiles disueltas**.
2. Para cada serie (80 series disponibles por comunidad autÃ³noma y tipo), extrae los datos y los imprime en formato estructurado.

#### Cobertura temporal

Desde **enero de 1995** hasta la actualidad (2026), con datos mensuales.

---

### Notebook 04: `04_eda.ipynb` â€” AnÃ¡lisis Exploratorio de Datos

Realiza un anÃ¡lisis exploratorio de los datasets extraÃ­dos, incluyendo estadÃ­sticas descriptivas, distribuciones y patrones identificados.

---

### Notebook 05: `05_transformation.ipynb` â€” TransformaciÃ³n

Aplica las transformationes definidas en los mÃ³dulos `src/transformation/`:
- ConversiÃ³n de tipos (IDs a string)
- NormalizaciÃ³n de texto (acentos, guiones, nombres de comunidades)
- EliminaciÃ³n de categorÃ­as redundantes

---

### Notebook 06: `06_visualizations.ipynb` â€” Visualizaciones

Genera grÃ¡ficos y visualizaciones de los datos transformados para identificar tendencias y patrones.

---

### Notebook 07: `07_correlation.ipynb` â€” CorrelaciÃ³n

AnÃ¡lisis de correlaciÃ³n entre las variables del dataset usando los mÃ³dulos de `src/correlation/`.

---

### Notebook 08: `08_load.ipynb` â€” Carga a Base de Datos

Carga los datos finales a MySQL usando los mÃ³dulos de `src/load/`. Incluye creaciÃ³n de tablas, inserciÃ³n de datos y validaciÃ³n de integridad referencial.

---

## Base de Datos

### Archivo SQL

`data_base/BBDD_spanish_ipc_analitic2.sql` contiene el script de creaciÃ³n de la base de datos con todas las tablas, claves primarias y forÃ¡neas.

### Modelo de datos

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
               â–²                 â–²                 â–²
               â”‚                 â”‚                 â”‚
               â”‚                 â”‚                 â”‚
               â”‚        â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”         â”‚
               â”‚        â”‚                â”‚         â”‚
               â”‚        â–¼                â–¼         â”‚
               â”‚ â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”‚
               â””â”€â”‚  territorio  â”‚ â”‚sectores_ipc  â”‚ â”‚
                 â”‚â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”‚ â”‚â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”‚ â”‚
                 â”‚id_territorio â”‚ â”‚id_sector  PK â”‚ â”‚
                 â”‚       PK     â”‚ â”‚nombre_sector â”‚ â”‚
                 â”‚nombre_territ.â”‚ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â”‚
                 â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜                  â”‚
                                                   â”‚
                                         â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                                         â–¼
                                  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                                  â”‚ tipo_medida  â”‚
                                  â”‚â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”‚
                                  â”‚id_medida  PK â”‚
                                  â”‚nombre_medida â”‚
                                  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

## Dashboard

`dashboard_power_bi.pbix` contiene un dashboard interactivo en Power BI para visualizar los indicadores econÃ³micos de forma dinÃ¡mica.

---

## TopoJSON

`topojson/provincias_spain.geojson` contiene la geometrÃ­a de las provincias espaÃ±olas para generar mapas coroplÃ©ticos.

---

## Notas sobre DisoluciÃ³n de Sociedades

### 1. El "apellido" obligatorio: "En LiquidaciÃ³n"

Cuando una S.A. o una S.L. decide disolverse, no desaparece de la noche a la maÃ±ana. Entra en un proceso llamado perÃ­odo de liquidaciÃ³n (donde se pagan deudas, se cobran facturas pendientes y se reparte lo que quede).

Por ley, para proteger a los terceros (proveedores, bancos, clientes) y que todo el mundo sepa que la empresa estÃ¡ cerrando, la sociedad estÃ¡ obligada a aÃ±adir la expresiÃ³n **"en liquidaciÃ³n"** a su nombre.

- Si se llamaba: *TecnologÃ­a Avanzada, S.L.*
- PasarÃ¡ a llamarse: *TecnologÃ­a Avanzada, S.L. **en liquidaciÃ³n***

Las siglas S.L. o S.A. se mantienen porque la naturaleza jurÃ­dica de la empresa sigue siendo la misma hasta que se extinga por completo en el Registro Mercantil.

### 2. Â¿QuÃ© pasa con el Capital Social en la disoluciÃ³n?

El capital varÃ­a segÃºn el tipo de empresa: para constituir una S.A. se necesita mucho mÃ¡s capital mÃ­nimo que para una S.L. Pero al disolverse, el capital social ya no importa como una cifra que debas mantener en el banco, sino como una regla de reparto.

**Proceso con el dinero y los bienes**:

```
[Patrimonio de la Empresa]
        â”‚
        â–¼
1. Pagar a los Acreedores (Bancos, Hacienda, Proveedores, Empleados)
        â”‚
        â–¼
2. Â¿Sobra dinero/bienes? â†’ Se reparte entre los Socios
```

**Â¿CÃ³mo afecta el Capital Social a los socios al final?**

- **Medida de reparto**: Si sobra dinero despuÃ©s de pagar todas las deudas, ese dinero se reparte entre los socios en proporciÃ³n al capital que cada uno aportÃ³ al principio (o segÃºn las acciones/participaciones que tengan).
- **LÃ­mite de responsabilidad**: Si la empresa se disuelve porque estÃ¡ en quiebra y no hay dinero para pagar las deudas, los acreedores no pueden ir contra los bienes personales de los socios. La responsabilidad estaba limitada, precisamente, al capital aportado en la S.A. o S.L. (salvo negligencia grave o fraude).

**En resumen**: Las siglas S.A. o S.L. se quedan hasta el Ãºltimo respiro de la empresa, pero arrastrando el cartel de "en liquidaciÃ³n", y el capital social pasa de ser un "requisito de entrada" a ser la "medida de reparto" (si queda algo) o la barrera que protege tu colchÃ³n personal frente a las deudas.

---

## Stack TecnolÃ³gico

| Componente | VersiÃ³n |
|------------|---------|
| Python | 3.12 |
| pandas | Ãšltima estable |
| numpy | Ãšltima estable |
| matplotlib | Ãšltima estable |
| seaborn | Ãšltima estable |
| requests | Ãšltima estable |
| SQLAlchemy | Ãšltima estable |
| PyMySQL | Ãšltima estable |
| Jupyter Notebook | Ãšltima estable |
| API INE | REST JSON (wstempus) |

## InstalaciÃ³n

```bash
pip install -r requirements.txt
```

## Uso

Ejecutar los notebooks en orden secuencial:

```bash
jupyter notebook notebooks/01_extraction_ipc.ipynb   # IPC - modelo dimensional
jupyter notebook notebooks/02_extraction_constituidas.ipynb  # Sociedades constituidas
jupyter notebook notebooks/03_extraction_disueltas.ipynb  # Sociedades disueltas
jupyter notebook notebooks/04_eda.ipynb               # AnÃ¡lisis exploratorio
jupyter notebook notebooks/05_transformation.ipynb    # TransformaciÃ³n
jupyter notebook notebooks/06_visualizations.ipynb    # Visualizaciones
jupyter notebook notebooks/07_correlation.ipynb       # CorrelaciÃ³n
jupyter notebook notebooks/08_load.ipynb              # Carga a BD
```

O ejecutar el pipeline completo:

```bash
python run_pipeline.py
```

Los archivos CSV se generan automÃ¡ticamente en `files/data_raw/` y `files/data_processed/`.

## Fuentes de Datos

- **API JSON del INE**: https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/
- **Tabla 76136**: Ãndice de Precios al Consumo (IPC) â€” series por territorio y sector
- **Tabla 13913**: Sociedades mercantiles constituidas
- **Tabla 13915**: Sociedades mercantiles disueltas
- **DocumentaciÃ³n API**: https://www.ine.es/dyngs/ODE/es/index.htm
