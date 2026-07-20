"""Unit tests para la funcion int_a_str de trans_str.py."""

import sys
import os
import pytest
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from transformation.trans_str import int_a_str


class TestIntAStr:
    """Tests de la funcion int_a_str."""

    def test_convierte_int_a_str(self):
        df = pd.DataFrame({"id": [1, 2, 3], "nombre": ["a", "b", "c"]})
        resultado = int_a_str(df, ["id"])
        assert pd.api.types.is_string_dtype(resultado["id"])
        assert resultado["id"].iloc[0] == "1"

    def test_convierte_multiple_columnas(self):
        df = pd.DataFrame({"id": [1, 2], "code": [10, 20]})
        resultado = int_a_str(df, ["id", "code"])
        assert pd.api.types.is_string_dtype(resultado["id"])
        assert pd.api.types.is_string_dtype(resultado["code"])

    def test_no_modifica_columnas_no_listadas(self):
        df = pd.DataFrame({"id": [1, 2], "nombre": ["a", "b"]})
        resultado = int_a_str(df, ["id"])
        assert pd.api.types.is_string_dtype(resultado["nombre"])
        assert resultado["nombre"].iloc[0] == "a"

    def test_columna_no_existente_no_causa_error(self):
        df = pd.DataFrame({"id": [1, 2]})
        resultado = int_a_str(df, ["no_existe"])
        assert len(resultado) == 2

    def test_dataframe_vacio(self):
        df = pd.DataFrame({"id": pd.Series([], dtype=int)})
        resultado = int_a_str(df, ["id"])
        assert len(resultado) == 0

    def test_mantiene_otras_columnas_intactas(self):
        df = pd.DataFrame({"id": [1, 2], "valor": [10.5, 20.3]})
        resultado = int_a_str(df, ["id"])
        assert resultado["valor"].iloc[0] == 10.5

    def test_retorna_mismo_dataframe(self):
        df = pd.DataFrame({"id": [1, 2]})
        resultado = int_a_str(df, ["id"])
        assert resultado is df

    def test_lista_vacia_de_columnas(self):
        df = pd.DataFrame({"id": [1, 2], "nombre": ["a", "b"]})
        resultado = int_a_str(df, [])
        assert not pd.api.types.is_string_dtype(resultado["id"])

    def test_valores_mixtos_en_columna(self):
        df = pd.DataFrame({"col": [1, "dos", 3.0]})
        resultado = int_a_str(df, ["col"])
        assert pd.api.types.is_string_dtype(resultado["col"])
        assert resultado["col"].iloc[0] == "1"
        assert resultado["col"].iloc[1] == "dos"

    def test_nan_se_convierte_a_str_nan(self):
        df = pd.DataFrame({"id": [1, np.nan, 3]})
        resultado = int_a_str(df, ["id"])
        assert pd.api.types.is_string_dtype(resultado["id"])
