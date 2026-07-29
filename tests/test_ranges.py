"""Tests de rangos y valores válidos en columnas numéricas y temporales.

Valida que meses, años, ids y valores numéricos estén dentro
de los límites esperados.
"""


import numpy as np
 
 
def test_mes_range(df_tiempo):

    assert df_tiempo["mes"].between(1, 12).all(), "mes fuera de rango 1-12"
 
 
def test_anio_range(df_tiempo):

    anio_actual = 2026

    assert df_tiempo["anio"].between(2000, anio_actual).all(), f"anio fuera de rango 2000-{anio_actual}"
 
 
def test_numero_sociedades_constituidas(df_empr_const):

    assert (df_empr_const["numero_sociedades"] >= 0).all(), "numero_sociedades negativo en constituidas"
 
 
def test_numero_sociedades_disueltas(df_empr_dis):

    assert (df_empr_dis["numero_sociedades"] >= 0).all(), "numero_sociedades negativo en disueltas"
 
 
def test_capital_non_negative(df_empr_const):

    assert (df_empr_const["capital"] >= 0).all(), "capital negativo en constituidas"
 
 
def test_id_tiempo_format(df_tiempo):

    assert df_tiempo["id_tiempo"].astype(str).str.match(r"^\d{6}$").all(), "id_tiempo no tiene formato YYYYMM"
 
 
def test_id_territorio_range(df_territorio):

    assert df_territorio["id_territorio"].between(1, 20).all(), "id_territorio fuera de rango 1-20"
 
 
def test_id_sector_range(df_sectores_ipc):

    assert df_sectores_ipc["id_sector"].between(1, 14).all(), "id_sector fuera de rango 1-14"
 
 
def test_id_medida_range(df_tipo_medida):

    assert df_tipo_medida["id_medida"].between(1, 4).all(), "id_medida fuera de rango 1-4"
 
 
def test_valor_ipc_no_nulos(df_ipc):

    assert not df_ipc["valor_ipc"].isna().any(), "valor_ipc tiene nulos"

    assert np.isfinite(df_ipc["valor_ipc"]).all(), "valor_ipc tiene infinitos"