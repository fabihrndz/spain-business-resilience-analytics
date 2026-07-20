import os
import pandas as pd
from sqlalchemy import create_engine, text
import logging

logger = logging.getLogger(__name__)

def get_connection_string(db_name=None, user=None, password=None, host=None, port=None):
    """
    Centraliza la creación de la URL de forma dinámica.
    Resuelve problemas de importación y añade la barra de seguridad para SQLAlchemy.
    """
    # Evaluación dinámica: si es None, va a buscarlo al entorno en este instante
    user = user or os.getenv("DB_USER")
    password = password or os.getenv("DB_PASSWORD") # Asegúrate si tu .env usa DB_PASS o DB_PASSWORD
    host = host or os.getenv("DB_HOST")
    port = port or os.getenv("DB_PORT", "3306")
    
    if db_name:
        return f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/"


## 1️⃣ Crear Base de Datos
def create_database_if_not_exists(db_name):
    """Crea la base de datos si no existe usando la conexión por defecto."""
    connection_url = get_connection_string()
    engine_server = create_engine(connection_url)
    
    try:
        with engine_server.begin() as con:
            con.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
            logger.info(f"Base de datos '{db_name}' verificada/creada con éxito.")
    finally:
        engine_server.dispose()


## 2️⃣ Cargar el DataFrame
def load_dataframe_to_mysql(df, table_name, db_name, if_exists="replace"):
    """Carga un DataFrame pidiéndote solo los datos esenciales."""
    connection_url = get_connection_string(db_name=db_name)
    engine = create_engine(connection_url)
    
    try:
        df.to_sql(table_name, con=engine, if_exists=if_exists, index=False)
        logger.info(f"Datos cargados exitosamente en la tabla '{table_name}'.")
    finally:
        engine.dispose()


## 3️⃣ Definir la Clave Primaria
def set_primary_key(table_name, pk_column, db_name, data_type="INT"):
    """
    Asigna la PK en la tabla indicada. 
    Permite cambiar el tipo de dato (por defecto INT) por si tu clave es VARCHAR.
    """
    connection_url = get_connection_string(db_name=db_name)
    engine = create_engine(connection_url)
    
    try:
        with engine.begin() as con:
            # Primero modificamos la columna para asegurarnos que no acepte nulos
            con.execute(text(f"ALTER TABLE {table_name} MODIFY {pk_column} {data_type} NOT NULL"))
            con.execute(text(f"ALTER TABLE {table_name} ADD PRIMARY KEY ({pk_column})"))
            logger.info(f"Clave primaria '{pk_column}' ({data_type}) asignada en '{table_name}'.")
    finally:
        engine.dispose()

## 4️⃣ Función para definir Claves Foráneas (Foreign Keys) - modelo estrella
def set_foreign_keys(fact_table, relations, db_name):
    """
    Crea una o varias relaciones de clave foránea entre una tabla de hechos 
    y sus tablas de dimensión, típico de un modelo estrella.
    
    Parámetros:
        fact_table (str): tabla que contiene las FKs (tabla de hechos).
        relations (list[dict]): lista de relaciones, cada una con:
            - fk_column (str): columna FK en la tabla de hechos.
            - dimension_table (str): tabla de dimensión referenciada.
            - pk_column (str, opcional): columna PK en la dimensión (por defecto = fk_column).
            - data_type (str, opcional): tipo de dato de la columna FK (por defecto "INT").
        db_name (str): nombre de la base de datos.
    
    Ejemplo de 'relations':
        [
            {"fk_column": "id_producto", "dimension_table": "productos"},
            {"fk_column": "id_sucursal", "dimension_table": "sucursales"},
            {"fk_column": "id_tiempo", "dimension_table": "tiempo", "data_type": "INT"},
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
                    # El tipo de dato debe coincidir exactamente con el de la PK
                    con.execute(text(f"ALTER TABLE {fact_table} MODIFY {fk_column} {data_type} NOT NULL"))
                    
                    query = f"""
                        ALTER TABLE {fact_table}
                        ADD CONSTRAINT {constraint_name}
                        FOREIGN KEY ({fk_column})
                        REFERENCES {dimension_table}({pk_column})
                        ON DELETE CASCADE
                        ON UPDATE CASCADE
                    """
                    con.execute(text(query))
                    logger.info(f"Relación creada: {fact_table}.{fk_column} -> {dimension_table}.{pk_column}")

                except Exception as e:
                    logger.error(f"Error al asignar la clave foránea '{fk_column}' en {fact_table}: {e}")
                    raise
    finally:
        engine.dispose()
        


## 5️⃣ Agregar columna ID autoincremental
def add_autoincrement_id(table_name, db_name):
    """
    Agrega una columna autoincremental como PRIMARY KEY a una tabla existente.
    El nombre de la columna se genera automáticamente como 'id_{table_name}'.
    Si la tabla ya tiene una PK, la elimina antes de asignar la nueva.
    """
    column_name = f"id_{table_name}"
    connection_url = get_connection_string(db_name=db_name)
    engine = create_engine(connection_url)
    
    try:
        with engine.begin() as con:
            # Verificamos si ya existe una PRIMARY KEY en la tabla
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
            logger.info(f"Columna '{column_name}' autoincremental asignada como PK en '{table_name}'.")
    finally:
        engine.dispose()



# 6️⃣ Eliminar todas las tablas
def drop_all_tables(db_name, tables):
    """
    Elimina todas las tablas en orden inverso al de dependencias
    para respetar las FK. Si no existen, no falla.
    """
    connection_url = get_connection_string(db_name=db_name)
    
    # Capturamos el error si la base de datos completa no existe todavía
    try:
        engine = create_engine(connection_url)
        con = engine.connect()
    except Exception as e:
        # El error 1049 es "Unknown database". Si pasa, no hay tablas que borrar.
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