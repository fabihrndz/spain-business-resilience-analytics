"""Unit tests para las funciones del modulo correlation.py."""

import os
import sys

import matplotlib
import numpy as np
import pandas as pd
import pytest

matplotlib.use("Agg")
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from correlation.correlation import comparar_correlaciones, matriz_correlacion_visual


@pytest.fixture
def df_lineal():
    """DataFrame con relacion lineal perfecta."""
    return pd.DataFrame({"x": range(100), "y": range(100)})


@pytest.fixture
def df_no_lineal():
    """DataFrame con outliers que distorsionan Pearson pero no Spearman."""
    np.random.seed(42)
    x = np.random.normal(0, 1, 50)
    y = x + np.random.normal(0, 0.1, 50)
    x = np.append(x, [5, -5, 6, -6])
    y = np.append(y, [0.5, -0.5, 0.3, -0.3])
    return pd.DataFrame({"x": x, "y": y})


@pytest.fixture
def df_con_outliers():
    """DataFrame con outliers que distorsionan Pearson."""
    np.random.seed(42)
    x = np.random.normal(0, 1, 100)
    y = x + np.random.normal(0, 0.1, 100)
    # Agregar outliers extremos
    x = np.append(x, [10, -10, 15])
    y = np.append(y, [10, -10, 15])
    return pd.DataFrame({"x": x, "y": y})


class TestCompararCorrelaciones:
    """Tests de la funcion comparar_correlaciones."""

    @patch("correlation.correlation.plt.show")
    def test_retorna_dict_con_claves_esperadas(self, mock_show, df_lineal):
        resultado = comparar_correlaciones(df_lineal, "x", "y")
        assert isinstance(resultado, dict)
        assert "pearson" in resultado
        assert "spearman" in resultado
        assert "diferencia" in resultado
        assert "recomendacion" in resultado
        assert "fuerza" in resultado
        assert "direccion" in resultado
        assert "n_validos" in resultado
        assert "n_total" in resultado

    @patch("correlation.correlation.plt.show")
    def test_relacion_lineal_recomienda_pearson(self, mock_show, df_lineal):
        resultado = comparar_correlaciones(df_lineal, "x", "y")
        assert resultado["recomendacion"] == "pearson"
        assert resultado["pearson"] == pytest.approx(1.0, abs=0.01)

    @patch("correlation.correlation.plt.show")
    def test_relacion_lineal_diferencia_baja(self, mock_show, df_lineal):
        resultado = comparar_correlaciones(df_lineal, "x", "y")
        assert resultado["diferencia"] < 0.1

    @patch("correlation.correlation.plt.show")
    def test_relacion_no_lineal_recomienda_spearman(self, mock_show, df_no_lineal):
        resultado = comparar_correlaciones(df_no_lineal, "x", "y")
        assert resultado["recomendacion"] == "spearman"

    @patch("correlation.correlation.plt.show")
    def test_columnas_no_existentes_lanza_error(self, mock_show, df_lineal):
        with pytest.raises(ValueError, match="no existen"):
            comparar_correlaciones(df_lineal, "x", "z")

    @patch("correlation.correlation.plt.show")
    def test_con_nan_recalcula_correctamente(self, mock_show):
        df = pd.DataFrame({"x": [1, 2, 3, np.nan, 5], "y": [1, 2, 3, 4, 5]})
        resultado = comparar_correlaciones(df, "x", "y")
        assert resultado["n_validos"] == 4
        assert resultado["n_total"] == 5

    @patch("correlation.correlation.plt.show")
    def test_fuerza_muy_fuerte(self, mock_show, df_lineal):
        resultado = comparar_correlaciones(df_lineal, "x", "y")
        assert resultado["fuerza"] == "muy fuerte"

    @patch("correlation.correlation.plt.show")
    def test_direccion_positiva(self, mock_show, df_lineal):
        resultado = comparar_correlaciones(df_lineal, "x", "y")
        assert resultado["direccion"] == "positiva"

    @patch("correlation.correlation.plt.show")
    def test_direccion_negativa(self, mock_show):
        df = pd.DataFrame({"x": range(100), "y": range(100, 0, -1)})
        resultado = comparar_correlaciones(df, "x", "y")
        assert resultado["direccion"] == "negativa"

    @patch("correlation.correlation.plt.show")
    def test_sin_plot(self, mock_show, df_lineal):
        resultado = comparar_correlaciones(df_lineal, "x", "y", mostrar_plot=False)
        mock_show.assert_not_called()
        assert "pearson" in resultado


class TestMatrizCorrelacionVisual:
    """Tests de la funcion matriz_correlacion_visual."""

    @patch("correlation.correlation.plt.show")
    @patch("correlation.correlation.sns.heatmap")
    def test_retorna_dataframe(self, mock_heatmap, mock_show):
        df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9]})
        resultado = matriz_correlacion_visual(df)
        assert isinstance(resultado, pd.DataFrame)

    @patch("correlation.correlation.plt.show")
    @patch("correlation.correlation.sns.heatmap")
    def test_diagonal_es_uno(self, mock_heatmap, mock_show):
        df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        resultado = matriz_correlacion_visual(df)
        assert resultado.loc["a", "a"] == pytest.approx(1.0)
        assert resultado.loc["b", "b"] == pytest.approx(1.0)

    @patch("correlation.correlation.plt.show")
    @patch("correlation.correlation.sns.heatmap")
    def test_metodo_spearman(self, mock_heatmap, mock_show):
        df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        resultado = matriz_correlacion_visual(df, metodo="spearman")
        assert isinstance(resultado, pd.DataFrame)

    @patch("correlation.correlation.plt.show")
    @patch("correlation.correlation.sns.heatmap")
    def test_sin_triangulo_superior(self, mock_heatmap, mock_show):
        df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        resultado = matriz_correlacion_visual(df, solo_triangulo=False)
        assert isinstance(resultado, pd.DataFrame)
