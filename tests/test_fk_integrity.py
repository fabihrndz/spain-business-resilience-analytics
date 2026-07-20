"""Tests de integridad referencial (claves foráneas).

Verifica que todas las claves foráneas en las tablas de hechos
y empresas apuntan a registros existentes en las tablas de dimensión.
"""

import pandas as pd


def test_fk_ipc_tiempo(df_ipc: pd.DataFrame, df_tiempo: pd.DataFrame) -> None:
    """Valida que todos los id_tiempo en ipc existen en tiempo."""
    ids_ipc = set(df_ipc["id_tiempo"].unique())
    ids_tiempo = set(df_tiempo["id_tiempo"].unique())
    ids_faltantes = ids_ipc - ids_tiempo
    assert not ids_faltantes, f"id_tiempo en ipc sin referencia en tiempo: {ids_faltantes}"


def test_fk_ipc_territorio(df_ipc: pd.DataFrame, df_territorio: pd.DataFrame) -> None:
    """Valida que todos los id_territorio en ipc existen en territorio."""
    ids_ipc = set(df_ipc["id_territorio"].unique())
    ids_territorio = set(df_territorio["id_territorio"].unique())
    ids_faltantes = ids_ipc - ids_territorio
    assert not ids_faltantes, (
        f"id_territorio en ipc sin referencia en territorio: {ids_faltantes}"
    )


def test_fk_ipc_sector(df_ipc: pd.DataFrame, df_sectores_ipc: pd.DataFrame) -> None:
    """Valida que todos los id_sector en ipc existen en sectores_ipc."""
    ids_ipc = set(df_ipc["id_sector"].unique())
    ids_sector = set(df_sectores_ipc["id_sector"].unique())
    ids_faltantes = ids_ipc - ids_sector
    assert not ids_faltantes, (
        f"id_sector en ipc sin referencia en sectores_ipc: {ids_faltantes}"
    )


def test_fk_ipc_medida(df_ipc: pd.DataFrame, df_tipo_medida: pd.DataFrame) -> None:
    """Valida que todos los id_medida en ipc existen en tipo_medida."""
    ids_ipc = set(df_ipc["id_medida"].unique())
    ids_medida = set(df_tipo_medida["id_medida"].unique())
    ids_faltantes = ids_ipc - ids_medida
    assert not ids_faltantes, (
        f"id_medida en ipc sin referencia en tipo_medida: {ids_faltantes}"
    )


def test_fk_constituidas_tiempo(
    df_empr_const: pd.DataFrame, df_tiempo: pd.DataFrame
) -> None:
    """Valida que todos los id_tiempo en empresas_constituidas existen en tiempo."""
    ids_emp = set(df_empr_const["id_tiempo"].unique())
    ids_tiempo = set(df_tiempo["id_tiempo"].unique())
    assert not (ids_emp - ids_tiempo), (
        "id_tiempo en empresas_constituidas sin referencia en tiempo"
    )


def test_fk_constituidas_territorio(
    df_empr_const: pd.DataFrame, df_territorio: pd.DataFrame
) -> None:
    """Valida que todos los id_territorio en empresas_constituidas existen en territorio."""
    ids_emp = set(df_empr_const["id_territorio"].unique())
    ids_territorio = set(df_territorio["id_territorio"].unique())
    assert not (ids_emp - ids_territorio), (
        "id_territorio en empresas_constituidas sin referencia en territorio"
    )


def test_fk_disueltas_tiempo(
    df_empr_dis: pd.DataFrame, df_tiempo: pd.DataFrame
) -> None:
    """Valida que todos los id_tiempo en empresas_disueltas existen en tiempo."""
    ids_emp = set(df_empr_dis["id_tiempo"].unique())
    ids_tiempo = set(df_tiempo["id_tiempo"].unique())
    assert not (ids_emp - ids_tiempo), (
        "id_tiempo en empresas_disueltas sin referencia en tiempo"
    )


def test_fk_disueltas_territorio(
    df_empr_dis: pd.DataFrame, df_territorio: pd.DataFrame
) -> None:
    """Valida que todos los id_territorio en empresas_disueltas existen en territorio."""
    ids_emp = set(df_empr_dis["id_territorio"].unique())
    ids_territorio = set(df_territorio["id_territorio"].unique())
    assert not (ids_emp - ids_territorio), (
        "id_territorio en empresas_disueltas sin referencia en territorio"
    )
