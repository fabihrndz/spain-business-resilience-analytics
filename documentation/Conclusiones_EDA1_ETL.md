# Documentación del Modelo de Datos

## Empresas constituidas

Consta de **16720 filas y 6 columnas**:

| # | Columna | Tipo | Descripción |
|---|---------|------|--------------|
| 0 | `id_const` | Int | Id de la tabla, autoincremental |
| 1 | `territorio` | String | Nombra las 19 comunidades autónomas |
| 2 | `id_tiempo` | Int | Muestra año y mes, el mes en dígito de 2 números (AAAAMM) |
| 3 | `tipo` | String | Categórica con 4 opciones: Mercantiles (suma de S.A. y S.L.), Sociedades anónimas, Sociedades de responsabilidad limitada, S. Comanditarias y S. Colectivas. Cada categoría tiene 4180 filas (una fila por fecha, haya o no disueltas) |
| 4 | `numero_sociedades` | Int | Número de sociedades creadas |
| 5 | `capital` | Int | Capital con el que se constituye la empresa |

## Empresas disueltas

Consta de **12539 filas y 5 columnas**:

| # | Columna | Tipo | Descripción |
|---|---------|------|--------------|
| 0 | `id_dis` | Int | Id de la tabla, autoincremental |
| 1 | `territorio` | String | Nombra las 19 comunidades autónomas |
| 2 | `id_tiempo` | Int | Año y mes, siempre con dos cifras (AAAAMM) |
| 3 | `razon` | String | Motivo de la disolución, categórica: Voluntaria (4180), Por fusión (4180), Otras (4180). *En la API existe además la categoría "Total", que se elimina de la llamada porque es solo una suma de las demás y da resultados falseados* |
| 4 | `numero_sociedades` | Int | Cantidad de sociedades disueltas |

## Sectores IPC

Consta de **14 filas y 2 columnas**:

| # | Columna | Tipo | Descripción |
|---|---------|------|--------------|
| 0 | `id_sector` | Int | Id que representa la actividad económica |
| 1 | `Nombre` | String | Nombre del sector económico |

**Valores de `id_sector`:**

| id | Sector |
|----|--------|
| 1 | Índice general |
| 2 | Alimentos y bebidas no alcohólicas |
| 3 | Bebidas alcohólicas y tabaco |
| 4 | Vestido y calzado |
| 5 | Vivienda, agua, electricidad, gas y otros combustibles |
| 6 | Muebles, artículos del hogar y artículos para el mantenimiento corriente del hogar |
| 7 | Sanidad |
| 8 | Transporte |
| 9 | Información y comunicaciones |
| 10 | Actividades recreativas, deporte y cultura |
| 11 | Enseñanza |
| 12 | Restaurantes y servicios de alojamiento |
| 13 | Seguros y servicios financieros |
| 14 | Cuidado personal, protección social, y bienes y servicios diversos |

## Territorio

Consta de **20 filas y 2 columnas**:

| # | Columna | Tipo | Descripción |
|---|---------|------|--------------|
| 0 | `id_territorio` | Int | Número que representa cada comunidad autónoma, además del 1 que es nacional |
| 1 | `Nombre` | String | Nombre de cada comunidad autónoma, más el total del cómputo que es nacional |

**Valores de `id_territorio`:**

| id | Territorio |
|----|------------|
| 1 | Nacional |
| 2 | Andalucía |
| 3 | Aragón |
| 4 | Asturias, Principado de |
| 5 | Balears, Illes |
| 6 | Canarias |
| 7 | Cantabria |
| 8 | Castilla y León |
| 9 | Castilla - La Mancha |
| 10 | Cataluña |
| 11 | Comunitat Valenciana |
| 12 | Extremadura |
| 13 | Galicia |
| 14 | Madrid, Comunidad de |
| 15 | Murcia, Región de |
| 16 | Navarra, Comunidad Foral de |
| 17 | País Vasco |
| 18 | Rioja, La |
| 19 | Ceuta |
| 20 | Melilla |

## Tiempo

Consta de **294 filas y 4 columnas**. Representa el periodo de tiempo:

| # | Columna | Tipo | Descripción |
|---|---------|------|--------------|
| 0 | `id_tiempo` | Int | Id de la tabla, autoincremental |
| 1 | `anio` | Int | AAAA |
| 2 | `mes` | Int | MM |
| 3 | `nombre_mes` | String | Nombre del mes |

## Tipo medida

Consta de **4 filas y 2 columnas**:

| # | Columna | Tipo | Descripción |
|---|---------|------|--------------|
| 0 | `id_tipo_medida` | Int | Id de la tabla, autoincremental |
| 1 | `nombre_medida` | String | Categórica que representa el tipo de comparativa |

**Valores de `nombre_medida`:**
- Índice
- Variación mensual
- Variación anual
- Variación en lo que va de año

## IPC

Consta de **311752 filas y 5 columnas**:

| # | Columna | Tipo | Descripción |
|---|---------|------|--------------|
| 0 | `id_tiempo` | Int | FK a `tiempo`, autoincremental |
| 1 | `id_territorio` | Int | FK a `territorio`, id de las 19 comunidades autónomas |
| 2 | `id_sector` | Int | FK a `sectores_ipc`, representa el sector económico de la actividad |
| 3 | `id_medida` | Int | FK a `tipo_medida`, categórica con 4 categorías: 1-Índice, 2-Variación mensual, 3-Variación anual, 4-Variación en lo que va de año |
| 4 | `numero_sociedades` | Int | Cantidad de número de sociedades disueltas |

---

## Transformaciones

### 1. `TRANS_STRING`

Pasamos los ids (`id_const`, `id_tiempo`, etc.) a tipo `string`, ya que no se usan para operaciones matemáticas y tiene más sentido tratarlos como categóricos.

Se implementa mediante una función en un archivo `.py` (`trans_str`), dentro de `src/transformation`.

Columnas afectadas por tabla:

- `df_empr_const`: `id_const`, `id_tiempo`
- `df_empr_dis`: `id_dis`, `id_tiempo`
- `df_ipc`: `id_tiempo`, `id_territorio`, `id_sector`, `id_medida`
- `df_sectores_ipc`: `id_sector`
- `df_territorio`: `id_territorio`
- `df_tiempo`: `id_tiempo`, `anio`, `mes`
- `df_tipo_medida`: `id_medida`

### 2. Normalización en texto

Cambiar el nombre de las comunidades: cambiar orden, sin acento, en minúscula y con separación por guion bajo. Se implementa mediante un `replace` en una función `.py` (`trans_normal`), dentro de `src/transformation`.

Tablas afectadas:

- `empresas constituidas` → columna `territorio`
- `empresas disueltas` → columna `territorio`
- `territorio` → columna `nombre`

### 3. Eliminar tipo `Mercantil`

Es la suma del resto de categorías y daría resultados falseados. Con esto se eliminan 4180 filas.

### 4. Sustitución del nombre de tipo de empresa

| Nombre original | Sustituido por |
|---|---|
| Sociedad Limitada | S.L. |
| Sociedad Anónima | S.A. |
| S. Comanditarias y S. Colectivas | S.Com/S.C. |

### 5. Normalización de comunidades

Poner el nombre de todas las comunidades autónomas en castellano.

### 6. Guardado de CSV transformados

Los nuevos CSV transformados se guardan en `Files/data_processed`.

### 7. Creación de la base de datos

Se crea la base de datos con **SQLAlchemy**, invocada desde un archivo `.py` (`load.py`).

### 8. Archivo `.env`

Se crea un archivo `.env` con los datos y claves de acceso a MySQL desde Python (no es visible ya que está en `.gitignore`).

Para que la base de datos funcione, debe crearse un archivo `.env` con la siguiente base:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_NAME=nombre_de_tu_base_de_datos
```

### 9. `.gitignore`

Se crea un `.gitignore` para proteger los datos sensibles, incluyendo en él el archivo `.env`.