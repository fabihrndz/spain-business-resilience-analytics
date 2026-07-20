import pytest
 
 
def test_duplicates_tiempo(df_tiempo):

    assert df_tiempo["id_tiempo"].is_unique, "id_tiempo duplicado en tiempo"
 
 
def test_duplicates_territorio(df_territorio):

    assert df_territorio["id_territorio"].is_unique, "id_territorio duplicado en territorio"
 
 
def test_duplicates_sectores(df_sectores_ipc):

    assert df_sectores_ipc["id_sector"].is_unique, "id_sector duplicado en sectores_ipc"
 
 
def test_duplicates_tipo_medida(df_tipo_medida):

    assert df_tipo_medida["id_medida"].is_unique, "id_medida duplicado en tipo_medida"
 
 
def test_duplicates_ipc_combination(df_ipc):

    cols = ["id_tiempo", "id_territorio", "id_sector", "id_medida"]

    assert not df_ipc.duplicated(subset=cols).any(), f"Combinación {cols} duplicada en ipc"
 
 
def test_duplicates_constituidas(df_empr_const):

    assert df_empr_const["id_const"].is_unique, "id_const duplicado en empresas_constituidas"
 
 
def test_duplicates_disueltas(df_empr_dis):

    assert df_empr_dis["id_dis"].is_unique, "id_dis duplicado en empresas_disueltas"
 