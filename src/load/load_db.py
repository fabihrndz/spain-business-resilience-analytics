"""Módulo de carga de datos a MySQL.

Proporciona funciones para crear bases de datos, cargar DataFrames,
definir claves primarias y foráneas, y gestionar tablas en MySQL
usando SQLAlchemy.
"""

import os
import logging

import pandas as pd
from sqlalchemy import create_engine, text

logger = logging.getLogger(__name__)


def get_connection_string(
    db_name: str | None = None,
    user: str | None = None,
    password: str | None = None,
    host: str | None = None,
    port: str | None = None,
) -> str:
    """Construye la URL de conexión a MySQL de forma dinámica.

    Si no se proporcionan parámetros, los busca en las variables de entorno.

    Args:
        db_name: Nombre de la base de datos. Si es None, conecta sin DB.
        user: Usuario de MySQL. Si es None, usa DB_USER del entorno.
        password: Contraseña de MySQL. Si es None, usa DB_PASSWORD del entorno.
        host: Host de MySQL. Si es None, usa DB_HOST del entorno.
        port: Puerto de MySQL. Si es None, usa DB_PORT (por defecto 3306).

    Returns:
        URL de conexión en formato SQLAlchemy.
    """
    user = user or os.getenv("DB_USER")
    password = password or os.getenv("DB_PASSWORD")
    host = host or os.getenv("DB_HOST")
    port = port or os.getenv("DB_PORT", "3306")

    if db_name:
        return f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/"


def create_database_if_not_exists(db_name: str) -> None:
    """Crea la base de datos si no existe usando la conexión por defecto.

    Args:
        db_name: Nombre de la base de datos a crear.
    """
    connection_url = get_connection_string()
    engine_server = create_engine(connection_url)

    try:
        with engine_server.begin() as con:
            con.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
            logger.info(f"Base de datos '{db_name}' verificada/creada con éxito.")
    finally:
        engine_server.dispose()


def load_dataframe_to_mysql(
    df: pd.DataFrame,
    table_name: str,
    db_name: str,
    if_exists: str = "replace",
) -> None:
    """Carga un DataFrame en una tabla de MySQL.

    Args:
        df: DataFrame con los datos a cargar.
        table_name: Nombre de la tabla destino en MySQL.
        db_name: Nombre de la base de datos.
        if_exists: Comportamiento si la tabla ya existe
                   ('replace', 'append', 'fail').
    """
    connection_url = get_connection_string(db_name=db_name)
    engine = create_engine(connection_url)

    try:
        df.to_sql(table_name, con=engine, if_exists=if_exists, index=False)
        logger.info(f"Datos cargados exitosamente en la tabla '{table_name}'.")
    finally:
        engine.dispose()


def set_primary_key(
    table_name: str,
    pk_column: str,
    db_name: str,
    data_type: str = "INT",
) -> None:
    """Asigna una clave primaria a una columna existente.

    Modifica la columna para que no acepte nulos y le asigna
    la restricción PRIMARY KEY.

    Args:
        table_name: Nombre de la tabla.
        pk_column: Columna que será clave primaria.
        db_name: Nombre de la base de datos.
        data_type: Tipo de dato de la columna (por defecto 'INT').
    """
    connection_url = get_connection_string(db_name=db_name)
    engine = create_engine(connection_url)

    try:
        with engine.begin() as con:
            con.execute(text(
                f"ALTER TABLE {table_name} MODIFY {pk_column} {data_type} NOT NULL"
            ))
            con.execute(text(
                f"ALTER TABLE {table_name} ADD PRIMARY KEY ({pk_column})"
            ))
            logger.info(
                f"Clave primaria '{pk_column}' ({data_type}) asignada en '{table_name}'."
            )
    finally:
        engine.dispose()


def set_foreign_keys(
    fact_table: str,
    relations: list[dict[str, str]],
    db_name: str,
) -> None:
    """Crea relaciones de clave foránea entre una tabla de hechos y dimensiones.

    Diseñado para modelo estrella: una tabla de hechos con múltiples
    tablas de dimensión.

    Args:
        fact_table: Tabla que contiene las FKs (tabla de hechos).
        relations: Lista de relaciones, cada una con:
            - fk_column: Columna FK en la tabla de hechos.
            - dimension_table: Tabla de dimensión referenciada.
            - pk_column (opcional): Columna PK en la dimensión
              (por defecto = fk_column).
            - data_type (opcional): Tipo de dato de la columna FK
              (por defecto 'INT').
        db_name: Nombre de la base de datos.

    Ejemplo:
        relations = [
            {"fk_column": "id_producto", "dimension_table": "productos"},
            {"fk_column": "id_tiempo", "dimension_table": "tiempo"},
        ]
    """
    connection_url = get_connection_string(db_name=db_name)
    engine = create_engine(connection_url)

    try:
        with engine.begin() as con:
            for rel in relations:
                fk_column = rel["fk_column"]
                dimension_table = rel["dimension_table"]
                pk_column = rel.get("pk_column", fk_column)
                data_type = rel.get("data_type", "INT")

                constraint_name = f"fk_{fact_table}_{dimension_table}_{fk_column}"

                try:
                    con.execute(text(
                        f"ALTER TABLE {fact_table} MODIFY {fk_column} {data_type} NOT NULL"
                    ))

                    query = f"""
                        ALTER TABLE {fact_table}
                        ADD CONSTRAINT {constraint_name}
                        FOREIGN KEY ({fk_column})
                        REFERENCES {dimension_table}({pk_column})
                        ON DELETE CASCADE
                        ON UPDATE CASCADE
                    """
                    con.execute(text(query))
                    logger.info(
                        f"Relación creada: {fact_table}.{fk_column} -> "
                        f"{dimension_table}.{pk_column}"
                    )

                except Exception as e:
                    logger.error(
                        f"Error al asignar la clave foránea '{fk_column}' "
                        f"en {fact_table}: {e}"
                    )
                    raise
    finally:
        engine.dispose()


def add_autoincrement_id(table_name: str, db_name: str) -> None:
    """Agrega una columna autoincremental como PRIMARY KEY.

    Genera el nombre de la columna como 'id_{table_name}'.
    Si la tabla ya tiene una PK, la elimina antes de asignar la nueva.

    Args:
        table_name: Nombre de la tabla.
        db_name: Nombre de la base de datos.
    """
    column_name = f"id_{table_name}"
    connection_url = get_connection_string(db_name=db_name)
    engine = create_engine(connection_url)

    try:
        with engine.begin() as con:
            # Verificamos si ya existe una PRIMARY KEY
            result = con.execute(text(f"""
                SELECT COUNT(*)
                FROM information_schema.KEY_COLUMN_USAGE
                WHERE TABLE_NAME = '{table_name}'
                  AND CONSTRAINT_NAME = 'PRIMARY'
                  AND TABLE_SCHEMA = '{db_name}'
            """))
            tiene_pk = result.scalar() > 0

            if tiene_pk:
                con.execute(text(f"ALTER TABLE {table_name} DROP PRIMARY KEY"))
                logger.warning(f"Se eliminó la PK anterior de '{table_name}'.")

            con.execute(text(f"""
                ALTER TABLE {table_name}
                ADD COLUMN {column_name} INT AUTO_INCREMENT PRIMARY KEY FIRST
            """))
            logger.info(
                f"Columna '{column_name}' autoincremental asignada como PK en '{table_name}'."
            )
    finally:
        engine.dispose()


def drop_all_tables(db_name: str, tables: list[str]) -> None:
    """Elimina todas las tablas indicadas en orden inverso de dependencias.

    Respeta las claves foráneas desactivando temporalmente las FK checks.
    Si la base de datos no existe, no falla.

    Args:
        db_name: Nombre de la base de datos.
        tables: Lista de nombres de tablas a eliminar.
    """
    connection_url = get_connection_string(db_name=db_name)

    try:
        engine = create_engine(connection_url)
        con = engine.connect()
    except Exception as e:
        # Error 1049 = "Unknown database"
        if "1049" in str(e):
            logger.info(f"La base de datos {db_name} no existe. No hay tablas que eliminar.")
            return
        else:
            raise e

    try:
        with con:
            con.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
            for table in tables:
                con.execute(text(f"DROP TABLE IF EXISTS {table}"))
            con.execute(text("SET FOREIGN_KEY_CHECKS = 1"))

            con.commit()
            logger.info(f"Tablas eliminadas en {db_name}: {', '.join(tables)}")
    finally:
        engine.dispose()
