import pytest

import pandas as pd
 
DATA_DIR = "files/data_processed"
 
@pytest.fixture

def df_tiempo():

    return pd.read_csv(f"{DATA_DIR}/tiempo.csv")
 
@pytest.fixture

def df_territorio():

    return pd.read_csv(f"{DATA_DIR}/territorio.csv")
 
@pytest.fixture

def df_sectores_ipc():

    return pd.read_csv(f"{DATA_DIR}/sectores_ipc.csv")
 
@pytest.fixture

def df_tipo_medida():

    return pd.read_csv(f"{DATA_DIR}/tipo_medida.csv")
 
@pytest.fixture

def df_ipc():

    return pd.read_csv(f"{DATA_DIR}/ipc.csv")
 
@pytest.fixture

def df_empr_const():

    return pd.read_csv(f"{DATA_DIR}/empresas_constituidas.csv")
 
@pytest.fixture

def df_empr_dis():

    return pd.read_csv(f"{DATA_DIR}/empresas_disueltas.csv")
 