"""Fixtures compartidos para tests de validación de datos.

Proporciona DataFrames cargados desde los CSVs procesados
para ser utilizados en los tests de tipos, rangos,
duplicados e integridad referencial.
"""

import pytest
import pandas as pd

DATA_DIR = "files/data_processed"


@pytest.fixture
def df_tiempo() -> pd.DataFrame:
    """Carga la dimensión temporal desde tiempo.csv."""
    return pd.read_csv(f"{DATA_DIR}/tiempo.csv")


@pytest.fixture
def df_territorio() -> pd.DataFrame:
    """Carga la dimensión geográfica desde territorio.csv."""
    return pd.read_csv(f"{DATA_DIR}/territorio.csv")


@pytest.fixture
def df_sectores_ipc() -> pd.DataFrame:
    """Carga la dimensión de sectores del IPC desde sectores_ipc.csv."""
    return pd.read_csv(f"{DATA_DIR}/sectores_ipc.csv")


@pytest.fixture
def df_tipo_medida() -> pd.DataFrame:
    """Carga la dimensión de tipos de medida desde tipo_medida.csv."""
    return pd.read_csv(f"{DATA_DIR}/tipo_medida.csv")


@pytest.fixture
def df_ipc() -> pd.DataFrame:
    """Carga la tabla de hechos del IPC desde ipc.csv."""
    return pd.read_csv(f"{DATA_DIR}/ipc.csv")


@pytest.fixture
def df_empr_const() -> pd.DataFrame:
    """Carga la tabla de empresas constituidas desde empresas_constituidas.csv."""
    return pd.read_csv(f"{DATA_DIR}/empresas_constituidas.csv")


@pytest.fixture
def df_empr_dis() -> pd.DataFrame:
    """Carga la tabla de empresas disueltas desde empresas_disueltas.csv."""
    return pd.read_csv(f"{DATA_DIR}/empresas_disueltas.csv")
