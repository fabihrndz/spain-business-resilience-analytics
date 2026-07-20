"""Funciones de normalización de texto.

Proporciona utilidades para estandarizar strings: eliminar acentos,
convertir a minúsculas, reemplazar espacios por guiones bajos
y limpiar caracteres especiales.
"""

import re
import unicodedata

import pandas as pd


def normalizar_col(col: str) -> str:
    """Normaliza un string aplicando transformaciones de limpieza.

    Aplica las siguientes transformaciones en orden:
    1. Elimina espacios al inicio/final y convierte a minúsculas.
    2. Elimina acentos y tildes (NFKD + ASCII).
    3. Reemplaza espacios y guiones por guiones bajos.
    4. Elimina caracteres especiales (comas, paréntesis, etc.).

    Args:
        col: String de entrada a normalizar.

    Returns:
        String normalizado sin acentos, en minúsculas y con guiones bajos.
    """
    # 1. Elimina espacios al inicio/final y pasa a minúsculas
    col = col.strip().lower()

    # 2. Elimina acentos automáticamente
    col = (
        unicodedata.normalize("NFKD", col)
        .encode("ascii", "ignore")
        .decode("utf-8")
    )

    # 3. Reemplaza espacios por guiones bajos
    col = re.sub(r"[\s\-]+", "_", col)

    # 4. Quita caracteres raros como comas o paréntesis
    col = re.sub(r"[^\w_]", "", col)

    return col
