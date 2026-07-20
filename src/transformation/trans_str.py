"""Funciones de conversión de tipos de datos.

Proporciona utilidades para convertir columnas de un DataFrame
de un tipo a otro, útil para tratar IDs como categóricos.
"""

import logging

import pandas as pd

logger = logging.getLogger(__name__)


def int_a_str(df: pd.DataFrame, lista_columnas: list[str]) -> pd.DataFrame:
    """Transforma múltiples columnas de integer a string en un solo DataFrame.

    Args:
        df: DataFrame de entrada.
        lista_columnas: Nombres de las columnas a convertir.

    Returns:
        DataFrame con las columnas convertidas a tipo str.
    """
    for columna in lista_columnas:
        if columna in df.columns:
            df[columna] = df[columna].astype(str)
            logger.info(f"Columna '{columna}' convertida a str.")
        else:
            logger.warning(f"La columna '{columna}' no existe en este DataFrame.")
    return df
