"""Normalización de nombres de columna en DataFrames.

Convierte texto a minúsculas, elimina acentos, reemplaza espacios
por guiones bajos y remueve caracteres especiales.
"""

import re
import unicodedata


def normalizar_col(col: str) -> str:
    """Normaliza un string para usar como nombre de columna.

    Aplica limpieza secuencial: minúsculas, eliminación de acentos,
    espacios a guiones bajos y caracteres especiales.

    Args:
        col: Nombre de columna original.

    Returns:
        String normalizado, limpio y sin acentos.

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
