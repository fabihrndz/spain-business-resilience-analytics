"""Tests de validación de rangos numéricos.

Verifica que los valores de cada columna están dentro de rangos
lógicos y que no existen valores nulos o infinitos en columnas clave.
"""

import numpy as np
import pandas as pd


def test_mes_range(df_tiempo: pd.DataFrame) -> None:
    """Valida que el mes está en el rango 1-12."""
    assert df_tiempo["mes"].between(1, 12).all(), "mes fuera de rango 1-12"


def test_anio_range(df_tiempo: pd.DataFrame) -> None:
    """Valida que el año está entre 2000 y el año actual."""
    anio_actual = 2026
    assert df_tiempo["anio"].between(2000, anio_actual).all(), (
        f"anio fuera de rango 2000-{anio_actual}"
    )


def test_numero_sociedades_constituidas(df_empr_const: pd.DataFrame) -> None:
    """Valida que el número de sociedades constituidas no sea negativo."""
    assert (df_empr_const["numero_sociedades"] >= 0).all(), (
        "numero_sociedades negativo en constituidas"
    )


def test_numero_sociedades_disueltas(df_empr_dis: pd.DataFrame) -> None:
    """Valida que el número de sociedades disueltas no sea negativo."""
    assert (df_empr_dis["numero_sociedades"] >= 0).all(), (
        "numero_sociedades negativo en disueltas"
    )


def test_capital_non_negative(df_empr_const: pd.DataFrame) -> None:
    """Valida que el capital de empresas constituidas no sea negativo."""
    assert (df_empr_const["capital"] >= 0).all(), (
        "capital negativo en constituidas"
    )


def test_id_tiempo_format(df_tiempo: pd.DataFrame) -> None:
    """Valida que id_tiempo tiene formato YYYYMM (6 dígitos)."""
    assert df_tiempo["id_tiempo"].astype(str).str.match(r"^\d{6}$").all(), (
        "id_tiempo no tiene formato YYYYMM"
    )


def test_id_territorio_range(df_territorio: pd.DataFrame) -> None:
    """Valida que id_territorio está en el rango 1-20 (CCAA + Ceuta/Melilla)."""
    assert df_territorio["id_territorio"].between(1, 20).all(), (
        "id_territorio fuera de rango 1-20"
    )


def test_id_sector_range(df_sectores_ipc: pd.DataFrame) -> None:
    """Valida que id_sector está en el rango 1-14 (sectores del IPC)."""
    assert df_sectores_ipc["id_sector"].between(1, 14).all(), (
        "id_sector fuera de rango 1-14"
    )


def test_id_medida_range(df_tipo_medida: pd.DataFrame) -> None:
    """Valida que id_medida está en el rango 1-4 (tipos de medida IPC)."""
    assert df_tipo_medida["id_medida"].between(1, 4).all(), (
        "id_medida fuera de rango 1-4"
    )


def test_valor_ipc_no_nulos(df_ipc: pd.DataFrame) -> None:
    """Valida que valor_ipc no tiene valores nulos ni infinitos."""
    assert not df_ipc["valor_ipc"].isna().any(), "valor_ipc tiene nulos"
    assert np.isfinite(df_ipc["valor_ipc"]).all(), "valor_ipc tiene infinitos"

