# Documentación del Proyecto: Spain Business Resilience Analytics

## Visión General

Proyecto de análisis de resiliencia empresarial en España que extrae, transforma y modela datos del **Instituto Nacional de Estadística (INE)** a través de su API REST pública. Los datos se estructuran en un modelo dimensional (esquema estrella) para facilitar el análisis de indicadores económicos y la evolución del tejido empresarial español.

El proyecto cubre tres áreas de datos:

1. **IPC (Índice de Precios al Consumo)** — Tabla INE 76136
2. **Sociedades Constituidas** — Tabla INE 13913
3. **Sociedades Disueltas** — Tabla INE 13915

---

## Estructura del Proyecto

```
spain-business-resilience-analytics/
├── conexion_api.py           # Módulo de conexión a la API del INE
├── 01_extraccion.ipynb        # ETL del IPC (modelo dimensional)
├── 02_extracion.ipynb         # ETL de sociedades constituidas
├── 03_extraccion.ipynb        # ETL de sociedades disueltas
├── documentacion.md           # Este documento
├── README.md                  # Resumen del proyecto
├── .gitignore                 # Archivos ignorados (__pycache__)
├── tiempo.csv                 # Dimensión: tiempo
├── territorio.csv             # Dimensión: territorio
├── sectores_ipc.csv           # Dimensión: sectores del IPC
├── tipo_medida.csv            # Dimensión: tipo de medida
├── ipc.csv                    # Tabla de hechos del IPC
├── empresas_constituidas.csv  # Datos de sociedades constituidas
└── empresas_disueltas.csv     # Datos de sociedades disueltas
```

---

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

### Esquema del modelo dimensional

```
┌──────────────┐     ┌─────────────┐
│   tiempo     │     │  territorio │
│──────────────│     │─────────────│
│ id_tiempo PK │────▶│ id_terr  PK │
│ anio         │     │ nombre_terr │
│ mes          │     └─────────────┘
│ nombre_mes   │
└──────────────┘
       │               ┌─────────────┐
       │               │ sectores_ipc│
       │               │─────────────│
       ▼               │ id_sector PK│
┌──────────────────┐   │ nombre_sec  │
│  ipc (hechos)    │   └─────────────┘
│──────────────────│
│ id_tiempo    FK  │   ┌─────────────┐
│ id_territorio FK │   │ tipo_medida │
│ id_sector    FK  │──▶│─────────────│
│ id_medida    FK  │   │ id_medida PK│
│ valor_ipc       │   │ nombre_med  │
└──────────────────┘   └─────────────┘
```

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

Desde **enero de 1995** hasta la actualidad (2026), con datos mensuales.

### Datos destacables

- Máximo histórico en marzo de 2007: **16.165** sociedades constituidas en un mes
- Mínimo en abril de 2020 (COVID-19): **386** sociedades constituidas
- Promedio mensual aprox. 8.000–10.000 sociedades

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

Desde **enero de 1995** hasta la actualidad (2026), con datos mensuales.

### Datos destacables

- Máximo en enero de 2019: **4.157** sociedades disueltas
- Mínimo en mayo de 2020 (COVID-19): **482** sociedades disueltas (anomalía a la baja por restricciones)
- Tendencia general: 1.500–2.500 disoluciones mensuales en los últimos años

---

## Notas sobre Disolución de Sociedades

### 1. El "apellido" obligatorio: "En Liquidación"

Cuando una S.A. o una S.L. decide disolverse, no desaparece de la noche a la mañana. Entra en un proceso llamado período de liquidación (donde se pagan deudas, se cobran facturas pendientes y se reparte lo que quede).

Por ley, para proteger a los terceros (proveedores, bancos, clientes) y que todo el mundo sepa que la empresa está cerrando, la sociedad está obligada a añadir la expresión **"en liquidación"** a su nombre.

- Si se llamaba: *Tecnología Avanzada, S.L.*
- Pasará a llamarse: *Tecnología Avanzada, S.L. **en liquidación***

Las siglas S.L. o S.A. se mantienen porque la naturaleza jurídica de la empresa sigue siendo la misma hasta que se extinga por completo en el Registro Mercantil.

### 2. ¿Qué pasa con el Capital Social en la disolución?

El capital varía según el tipo de empresa: para constituir una S.A. se necesita mucho más capital mínimo que para una S.L. Pero al disolverse, el capital social ya no importa como una cifra que debas mantener en el banco, sino como una regla de reparto.

**Proceso con el dinero y los bienes**:

```
[Patrimonio de la Empresa]
        │
        ▼
1. Pagar a los Acreedores (Bancos, Hacienda, Proveedores, Empleados)
        │
        ▼
2. ¿Sobra dinero/bienes? → Se reparte entre los Socios
```

**¿Cómo afecta el Capital Social a los socios al final?**

- **Medida de reparto**: Si sobra dinero después de pagar todas las deudas, ese dinero se reparte entre los socios en proporción al capital que cada uno aportó al principio (o según las acciones/participaciones que tengan).
- **Límite de responsabilidad**: Si la empresa se disuelve porque está en quiebra y no hay dinero para pagar las deudas, los acreedores no pueden ir contra los bienes personales de los socios. La responsabilidad estaba limitada, precisamente, al capital aportado en la S.A. o S.L. (salvo negligencia grave o fraude).

**En resumen**: Las siglas S.A. o S.L. se quedan hasta el último respiro de la empresa, pero arrastrando el cartel de "en liquidación", y el capital social pasa de ser un "requisito de entrada" a ser la "medida de reparto" (si queda algo) o la barrera que protege tu colchón personal frente a las deudas.

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
jupyter notebook 01_extraccion.ipynb   # IPC - modelo dimensional
jupyter notebook 02_extracion.ipynb    # Sociedades constituidas
jupyter notebook 03_extraccion.ipynb   # Sociedades disueltas
```

Los archivos CSV se generan automáticamente en el directorio raíz del proyecto.

## Fuentes de Datos

- **API JSON del INE**: https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/
- **Tabla 76136**: Índice de Precios al Consumo (IPC) — series por territorio y sector
- **Tabla 13913**: Sociedades mercantiles constituidas
- **Tabla 13915**: Sociedades mercantiles disueltas
- **Documentación API**: https://www.ine.es/dyngs/ODE/es/index.htm
