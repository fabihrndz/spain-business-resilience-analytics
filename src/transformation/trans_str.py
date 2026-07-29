"""Conversión de columnas de DataFrame a tipo string.

Útil para estandarizar tipos de datos antes de la carga en base de datos.
"""

import logging

import pandas as pd

logger = logging.getLogger(__name__)


def int_a_str(df: pd.DataFrame, lista_columnas: list[str]) -> pd.DataFrame:
    """Transforma múltiples columnas a str en un solo DataFrame."""
    for columna in lista_columnas:
        if columna in df.columns:
            df[columna] = df[columna].astype(str)
            logger.info(f"Columna '{columna}' convertida a str.")
        else:
            logger.warning(f"La columna '{columna}' no existe en este DataFrame.")
    return df
