import logging

logger = logging.getLogger(__name__)


def int_a_str(df, lista_columnas):
    """
    Transforma múltiples columnas a str en un solo DataFrame.
    """
    for columna in lista_columnas:
        if columna in df.columns:
            df[columna] = df[columna].astype(str)
            logger.info(f"Columna '{columna}' convertida a str.")
        else:
            logger.warning(f"La columna '{columna}' no existe en este DataFrame.")
    return df