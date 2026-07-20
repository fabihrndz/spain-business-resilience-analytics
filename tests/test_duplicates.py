"""Tests de detección de duplicados.

Verifica que las claves primarias son únicas y que las combinaciones
de claves foráneas en la tabla de hechos no tienen filas duplicadas.
"""

import pandas as pd


def test_duplicates_tiempo(df_tiempo: pd.DataFrame) -> None:
    """Valida que id_tiempo es único en la dimensión tiempo."""
    assert df_tiempo["id_tiempo"].is_unique, "id_tiempo duplicado en tiempo"


def test_duplicates_territorio(df_territorio: pd.DataFrame) -> None:
    """Valida que id_territorio es único en la dimensión territorio."""
    assert df_territorio["id_territorio"].is_unique, "id_territorio duplicado en territorio"


def test_duplicates_sectores(df_sectores_ipc: pd.DataFrame) -> None:
    """Valida que id_sector es único en la dimensión sectores_ipc."""
    assert df_sectores_ipc["id_sector"].is_unique, "id_sector duplicado en sectores_ipc"


def test_duplicates_tipo_medida(df_tipo_medida: pd.DataFrame) -> None:
    """Valida que id_medida es único en la dimensión tipo_medida."""
    assert df_tipo_medida["id_medida"].is_unique, "id_medida duplicado en tipo_medida"


def test_duplicates_ipc_combination(df_ipc: pd.DataFrame) -> None:
    """Valida que la combinación de FKs en ipc es única (sin filas duplicadas)."""
    cols = ["id_tiempo", "id_territorio", "id_sector", "id_medida"]
    assert not df_ipc.duplicated(subset=cols).any(), (
        f"Combinación {cols} duplicada en ipc"
    )


def test_duplicates_constituidas(df_empr_const: pd.DataFrame) -> None:
    """Valida que id_const es único en empresas_constituidas."""
    assert df_empr_const["id_const"].is_unique, (
        "id_const duplicado en empresas_constituidas"
    )


def test_duplicates_disueltas(df_empr_dis: pd.DataFrame) -> None:
    """Valida que id_dis es único en empresas_disueltas."""
    assert df_empr_dis["id_dis"].is_unique, "id_dis duplicado en empresas_disueltas"
