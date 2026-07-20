"""Tests de validación de tipos de columna.

Verifica que cada DataFrame tiene los tipos de datos correctos
en cada columna según el esquema definido.
"""

import pandas as pd


def test_types_tiempo(df_tiempo: pd.DataFrame) -> None:
    """Valida los tipos de la dimensión tiempo: IDs y año/mes como int, nombre como str."""
    assert pd.api.types.is_integer_dtype(df_tiempo["id_tiempo"]) 
    assert pd.api.types.is_integer_dtype(df_tiempo["anio"])
    assert pd.api.types.is_integer_dtype(df_tiempo["mes"])
    assert pd.api.types.is_string_dtype(df_tiempo["nombre_mes"])


def test_types_territorio(df_territorio: pd.DataFrame) -> None:
    """Valida los tipos de la dimensión territorio: ID como int, nombre como str."""
    assert pd.api.types.is_integer_dtype(df_territorio["id_territorio"])
    assert pd.api.types.is_string_dtype(df_territorio["nombre_territorio"])


def test_types_sectores(df_sectores_ipc: pd.DataFrame) -> None:
    """Valida los tipos de la dimensión sectores_ipc: ID como int, nombre como str."""
    assert pd.api.types.is_integer_dtype(df_sectores_ipc["id_sector"])
    assert pd.api.types.is_string_dtype(df_sectores_ipc["nombre_sector"])


def test_types_tipo_medida(df_tipo_medida: pd.DataFrame) -> None:
    """Valida los tipos de la dimensión tipo_medida: ID como int, nombre como str."""
    assert pd.api.types.is_integer_dtype(df_tipo_medida["id_medida"])
    assert pd.api.types.is_string_dtype(df_tipo_medida["nombre_medida"])


def test_types_ipc(df_ipc: pd.DataFrame) -> None:
    """Valida los tipos de la tabla de hechos ipc: FKs como int, valor como float."""
    assert pd.api.types.is_integer_dtype(df_ipc["id_tiempo"])
    assert pd.api.types.is_integer_dtype(df_ipc["id_territorio"])
    assert pd.api.types.is_integer_dtype(df_ipc["id_sector"])
    assert pd.api.types.is_integer_dtype(df_ipc["id_medida"])
    assert pd.api.types.is_float_dtype(df_ipc["valor_ipc"])


def test_types_constituidas(df_empr_const: pd.DataFrame) -> None:
    """Valida los tipos de empresas constituidas: IDs como int, tipo como str."""
    assert pd.api.types.is_integer_dtype(df_empr_const["id_const"])
    assert pd.api.types.is_integer_dtype(df_empr_const["id_tiempo"])
    assert pd.api.types.is_string_dtype(df_empr_const["tipo"])
    assert pd.api.types.is_integer_dtype(df_empr_const["numero_sociedades"])
    assert pd.api.types.is_integer_dtype(df_empr_const["capital"])
    assert pd.api.types.is_integer_dtype(df_empr_const["id_territorio"])


def test_types_disueltas(df_empr_dis: pd.DataFrame) -> None:
    """Valida los tipos de empresas disueltas: IDs como int, razón como str."""
    assert pd.api.types.is_integer_dtype(df_empr_dis["id_dis"])
    assert pd.api.types.is_integer_dtype(df_empr_dis["id_tiempo"])
    assert pd.api.types.is_string_dtype(df_empr_dis["razon"])
    assert pd.api.types.is_integer_dtype(df_empr_dis["numero_sociedades"])
    assert pd.api.types.is_integer_dtype(df_empr_dis["id_territorio"])
