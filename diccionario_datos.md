# Diccionario de Datos — Spain Business Resilience Analytics

Descripción detallada de cada columna en los archivos CSV generados por el proyecto.

---

## Modelo dimensional del IPC (esquema estrella)

### `tiempo.csv` — Dimensión temporal

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `id_tiempo` | int (PK) | Clave primaria. Código de periodo en formato `YYYYMM` (ej: `202605` = mayo 2026) |
| `anio` | int | Año del periodo (ej: `2026`) |
| `mes` | int | Número de mes (1–12) |
| `nombre_mes` | str | Nombre completo del mes en español (ej: `Mayo`) |

### `territorio.csv` — Dimensión geográfica

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `id_territorio` | int (PK) | Identificador autoincremental del territorio |
| `nombre_territorio` | str | Nombre del ámbito geográfico: `Nacional` o comunidad autónoma (ej: `Andalucía`, `Cataluña`) |

### `sectores_ipc.csv` — Dimensión de sectores del IPC

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `id_sector` | int (PK) | Identificador autoincremental del sector |
| `nombre_sector` | str | Nombre del sector o grupo de consumo (ej: `Índice general`, `Alimentos y bebidas no alcohólicas`, `Transporte`) |

### `tipo_medida.csv` — Dimensión de tipo de medida

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `id_medida` | int (PK) | Identificador autoincremental del tipo de medida |
| `nombre_medida` | str | Tipo de indicador (ej: `Índice`, `Variación mensual`, `Variación anual`) |

### `ipc.csv` — Tabla de hechos del IPC

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `id_tiempo` | int (FK) → `tiempo.id_tiempo` | Periodo al que corresponde el valor |
| `id_territorio` | int (FK) → `territorio.id_territorio` | Ámbito geográfico del valor |
| `id_sector` | int (FK) → `sectores_ipc.id_sector` | Sector económico del IPC |
| `id_medida` | int (FK) → `tipo_medida.id_medida` | Tipo de medida (índice, variación mensual, etc.) |
| `valor_ipc` | float | Valor numérico del IPC para la combinación de dimensiones |

---

## Datos de sociedades mercantiles

### `empresas_constituidas.csv` — Sociedades constituidas (Tabla INE 13913)

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `id_const` | int (PK) | Identificador único autoincremental del registro |
| `territorio` | str | Ámbito geográfico (ej: `Andalucía`, `Cataluña`, `Total Nacional`) |
| `id_tiempo` | int | Periodo en formato `YYYYMM` (ej: `202604` = abril 2026) |
| `tipo` | str | Tipo de sociedad mercantil (ej: `Mercantiles`, `Sociedades Anónimas`, `Sociedades Limitadas`) |
| `numero_sociedades` | int | Número de sociedades constituidas en ese periodo y territorio |
| `capital` | int | Capital social total suscrito en euros (ej: `53774000`) |

### `empresas_disueltas.csv` — Sociedades disueltas (Tabla INE 13915)

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `id_dis` | int (PK) | Identificador único autoincremental del registro |
| `territorio` | str | Ámbito geográfico (ej: `Andalucía`, `Total Nacional`) |
| `id_tiempo` | int | Periodo en formato `YYYYMM` (ej: `202604` = abril 2026) |
| `razon` | str | Causa o tipo de disolución (ej: `Voluntaria`, `Fusión`, `Otras causas`) |
| `numero_sociedades` | int | Número de sociedades disueltas en ese periodo, territorio y causa |

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

empresas_constituidas.csv  (independiente, usa id_tiempo como referencia)
empresas_disueltas.csv     (independiente, usa id_tiempo como referencia)
```

- `id_tiempo` en los archivos de empresas referencia a `tiempo.csv` para vincular con fecha.
- `id_tiempo` sigue el formato `YYYYMM` en todos los archivos donde aparece.
