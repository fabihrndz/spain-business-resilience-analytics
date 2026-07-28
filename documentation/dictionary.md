# Diccionario de Datos — Spain Business Resilience Analytics

Descripción detallada de cada columna en los archivos CSV generados por el proyecto.

> **Nota**: Este diccionario describe los CSVs en `files/data_processed/` (resultado del notebook 05), que son los archivos que se cargan en la base de datos y se validan con tests.

---

## Modelo dimensional del IPC (esquema estrella)

### `tiempo.csv` — Dimensión temporal

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `id_tiempo` | str (PK) | Clave primaria. Código de periodo en formato `YYYYMM` (ej: `202605` = mayo 2026) |
| `anio` | str | Año del periodo (ej: `2026`) |
| `mes` | str | Número de mes (1–12) |
| `nombre_mes` | str | Nombre del mes normalizado en minúsculas sin acentos (ej: `mayo`, `junio`) |

### `territorio.csv` — Dimensión geográfica

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `id_territorio` | str (PK) | Identificador  del territorio (1–20) |
| `nombre_territorio` | str | Nombre del ámbito geográfico normalizado en minúsculas sin acentos (ej: `nacional`, `andalucia`, `cataluna`) |

### `sectores_ipc.csv` — Dimensión de sectores del IPC

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `id_sector` | str (PK) | Identificador  del sector (1–14) |
| `nombre_sector` | str | Nombre del sector normalizado en minúsculas sin acentos (ej: `indice_general`, `alimentos_y_bebidas_no_alcoholicas`) |

### `tipo_medida.csv` — Dimensión de tipo de medida

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `id_medida` | str (PK) | Identificador del tipo de medida (1–4) |
| `nombre_medida` | str | Tipo de indicador normalizado en minúsculas sin acentos (ej: `indice`, `variacion_mensual`, `variacion_anual`) |

### `ipc.csv` — Tabla de hechos del IPC

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `id_tiempo` | str (FK) → `tiempo.id_tiempo` | Periodo al que corresponde el valor |
| `id_territorio` | str (FK) → `territorio.id_territorio` | Ámbito geográfico del valor |
| `id_sector` | str (FK) → `sectores_ipc.id_sector` | Sector económico del IPC |
| `id_medida` | str (FK) → `tipo_medida.id_medida` | Tipo de medida (índice, variación mensual, etc.) |
| `valor_ipc` | float | Valor numérico del IPC para la combinación de dimensiones |

---

## Datos de sociedades mercantiles

### `empresas_constituidas.csv` — Sociedades constituidas (Tabla INE 13913)

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `id_const` | str (PK) | Identificador único del registro |
| `id_tiempo` | str (FK) → `tiempo.id_tiempo` | Periodo en formato `YYYYMM` (ej: `202604` = abril 2026) |
| `tipo` | str | Tipo de sociedad mercantil en formato siglas: `S.A.`, `S.L.`, `S.Com./S.C.` |
| `numero_sociedades` | int | Número de sociedades constituidas en ese periodo y territorio |
| `capital` | int | Capital social total suscrito en euros |
| `id_territorio` | int (FK) → `territorio.id_territorio` | Identificador del territorio |

> **Nota**: Se eliminaron las filas con `tipo = Mercantiles` ya que son sumatorias del resto de tipos.

### `empresas_disueltas.csv` — Sociedades disueltas (Tabla INE 13915)

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `id_dis` | str (PK) | Identificador único del registro |
| `id_tiempo` | str (FK) → `tiempo.id_tiempo` | Periodo en formato `YYYYMM` (ej: `202604` = abril 2026) |
| `razon` | str | Causa de disolución normalizada en minúsculas sin acentos: `voluntaria`, `por_fusion`, `otras` |
| `numero_sociedades` | int | Número de sociedades disueltas en ese periodo, territorio y causa |
| `id_territorio` | int (FK) → `territorio.id_territorio` | Identificador del territorio |

---

## Transformaciones aplicadas

El notebook `05_transformation.ipynb` aplica las siguientes transformaciones a los CSVs raw:

1. **Conversión de tipos**: IDs numéricos se convierten a `str`
2. **Mapeo de territorios**: Se agrega `id_territorio` desde la dimensión y se elimina la columna `territorio`
3. **Normalización de texto**: Nombres se convierten a minúsculas, se eliminan acentos, espacios se reemplazan por guiones bajos
4. **Eliminación de duplicados**: Filas "Mercantiles" en constituidas (agregan información ya presente)
5. **Abreviaturas**: Tipos societarios se convierten a siglas (S.A., S.L., S.Com./S.C.)

---

## Relaciones entre archivos

```
tiempo.csv ──────────┐
                     ├──→ ipc.csv
territorio.csv ──────┤
                     │
sectores_ipc.csv ────┤
                     │
tipo_medida.csv ─────┘

territorio.csv ──────┐
                     ├──→ empresas_constituidas.csv
tiempo.csv ──────────┤
                     
territorio.csv ──────┤
                     ├──→ empresas_disueltas.csv
tiempo.csv ──────────┘
```

### Relaciones FK detalladas

| Tabla hechos | Columna FK | Tabla dimensión | Columna PK |
|--------------|------------|-----------------|------------|
| `ipc` | `id_tiempo` | `tiempo` | `id_tiempo` |
| `ipc` | `id_territorio` | `territorio` | `id_territorio` |
| `ipc` | `id_sector` | `sectores_ipc` | `id_sector` |
| `ipc` | `id_medida` | `tipo_medida` | `id_medida` |
| `empresas_constituidas` | `id_tiempo` | `tiempo` | `id_tiempo` |
| `empresas_constituidas` | `id_territorio` | `territorio` | `id_territorio` |
| `empresas_disueltas` | `id_tiempo` | `tiempo` | `id_tiempo` |
| `empresas_disueltas` | `id_territorio` | `territorio` | `id_territorio` |

---

## Cobertura temporal

| Dataset | Desde | Hasta | Frecuencia |
|---------|-------|-------|------------|
| IPC | ~2021 (últimos 60 meses) | 2026 | Mensual |
| Sociedades constituidas | Enero 2002 | 2026 | Mensual |
| Sociedades disueltas | Enero 2002 | 2026 | Mensual |

---

## Datos destacables

### Sociedades constituidas
- **Máximo histórico**: 16.165 (marzo 2007)
- **Mínimo**: 386 (abril 2020, COVID-19)
- **Promedio mensual**: ~8.000–10.000

### Sociedades disueltas
- **Máximo**: 4.157 (enero 2019)
- **Mínimo**: 482 (mayo 2020, COVID-19)
- **Tendencia**: 1.500–2.500 mensuales en últimos años
