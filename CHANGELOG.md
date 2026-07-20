# Changelog

Todos los cambios notables en este proyecto se documentan en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es/1.1.0/).

## [1.0.0] - 2026-07-13

### Added

- Pipeline ETL completo con 8 notebooks en orden secuencial
- Extracción de datos del INE (IPC, sociedades constituidas y disueltas)
- Modelo dimensional en esquema estrella (tabla de hechos + 4 dimensiones)
- Módulo `connection_api.py` con caché de respuestas y logging
- Transformaciones: conversión de tipos y normalización de texto
- Carga a MySQL con SQLAlchemy
- Tests de validación (tipos, rangos, duplicados, integridad referencial)
- Ejecutor de pipeline `run_pipeline.py`
- Dashboard interactivo en Power BI
- GeoJSON de provincias para mapas coropléticos
- Documentación técnica completa
- Diccionario de datos
