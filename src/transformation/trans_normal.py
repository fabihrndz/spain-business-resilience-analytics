import re
import unicodedata
import pandas as pd


def normalizar_col(col: str) -> str:
    # 1. Elimina espacios al inicio/final y pasa a minusculas
    col = col.strip().lower()

    # 2. TIP EXTRA: Elimina acentos automaticamente
    col = (
        unicodedata.normalize("NFKD", col)
        .encode("ascii", "ignore")
        .decode("utf-8")
    )

    # 3. Reemplaza espacios por guiones bajos
    col = re.sub(r"[\s\-]+", "_", col)

    # 4. Quita caracteres raros como comas o parentesis
    col = re.sub(r"[^\w_]", "", col)

    return col
