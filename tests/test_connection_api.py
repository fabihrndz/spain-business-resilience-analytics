"""Unit tests para las funciones del modulo connection_api.py."""

import sys
import os
import json
import tempfile
import pytest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from api.connection_api import _get_cache_path, llamada_api, CACHE_DIR


class TestGetCachePath:
    """Tests de la funcion _get_cache_path."""

    def test_extrae_tabla_76136(self):
        url = "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/76136?nlast=60"
        resultado = _get_cache_path(url)
        assert "76136.json" in resultado

    def test_extrae_tabla_13913(self):
        url = "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/13913?nlast=12"
        resultado = _get_cache_path(url)
        assert "13913.json" in resultado

    def test_url_sin_tabla_devuelve_unknown(self):
        url = "https://servicios.ine.es/wstempus/js/ES/OTRA_COSA"
        resultado = _get_cache_path(url)
        assert "unknown.json" in resultado

    def test_ruta_contiene_cache_dir(self):
        url = "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/76136"
        resultado = _get_cache_path(url)
        assert CACHE_DIR in resultado


class TestLlamadaApi:
    """Tests de la funcion llamada_api."""

    @patch("api.connection_api.requests.get")
    def test_llamada_exitosa(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"Nombre": "test", "Data": []}]
        mock_get.return_value = mock_response

        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("api.connection_api.CACHE_DIR", tmpdir):
                resultado = llamada_api(
                    "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/76136"
                )
                assert resultado is not None
                assert isinstance(resultado, list)

    @patch("api.connection_api.requests.get")
    def test_llamada_guarda_en_cache(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        datos = [{"Nombre": "test"}]
        mock_response.json.return_value = datos
        mock_get.return_value = mock_response

        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("api.connection_api.CACHE_DIR", tmpdir):
                llamada_api(
                    "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/99999"
                )
                cache_file = os.path.join(tmpdir, "99999.json")
                assert os.path.exists(cache_file)
                with open(cache_file, "r", encoding="utf-8") as f:
                    contenido = json.load(f)
                assert contenido == datos

    @patch("api.connection_api.requests.get")
    def test_cache_evita_llamada_http(self, mock_get):
        datos = [{"Nombre": "cached"}]
        url = "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/11111"

        with tempfile.TemporaryDirectory() as tmpdir:
            cache_file = os.path.join(tmpdir, "11111.json")
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(datos, f)

            with patch("api.connection_api.CACHE_DIR", tmpdir):
                resultado = llamada_api(url)
                mock_get.assert_not_called()
                assert resultado == datos

    @patch("api.connection_api.requests.get")
    def test_status_no_200_devuelve_none(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_get.return_value = mock_response

        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("api.connection_api.CACHE_DIR", tmpdir):
                resultado = llamada_api(
                    "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/76136"
                )
                assert resultado is None

    @patch("api.connection_api.requests.get")
    def test_timeout_devuelve_none(self, mock_get):
        import requests
        mock_get.side_effect = requests.exceptions.Timeout()

        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("api.connection_api.CACHE_DIR", tmpdir):
                resultado = llamada_api(
                    "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/76136"
                )
                assert resultado is None

    @patch("api.connection_api.requests.get")
    def test_errorconexion_devuelve_none(self, mock_get):
        import requests
        mock_get.side_effect = requests.exceptions.ConnectionError()

        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("api.connection_api.CACHE_DIR", tmpdir):
                resultado = llamada_api(
                    "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/76136"
                )
                assert resultado is None

    @patch("api.connection_api.requests.get")
    def test_cache_corrupto_descarga_de_nuevo(self, mock_get):
        url = "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/22222"

        with tempfile.TemporaryDirectory() as tmpdir:
            cache_file = os.path.join(tmpdir, "22222.json")
            with open(cache_file, "w", encoding="utf-8") as f:
                f.write("esto no es json valido {{{")

            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = [{"Datos": "nuevos"}]
            mock_get.return_value = mock_response

            with patch("api.connection_api.CACHE_DIR", tmpdir):
                resultado = llamada_api(url)
                assert resultado is not None
                mock_get.assert_called_once()
