"""Unit tests para la funcion normalizar_col de trans_normal.py."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from transformation.trans_normal import normalizar_col


class TestNormalizarCol:
    """Tests de la funcion normalizar_col."""

    def test_minusculas(self):
        assert normalizar_col("HOLA MUNDO") == "hola_mundo"

    def test_espacios_a_guiones(self):
        assert normalizar_col("Madrid Comunidad") == "madrid_comunidad"

    def test_elimina_acentos(self):
        assert normalizar_col("Coruña") == "coruna"
        assert normalizar_col("Málaga") == "malaga"
        assert normalizar_col("Almería") == "almeria"
        assert normalizar_col("Gipuzkoa") == "gipuzkoa"

    def test_elimina_acentos_mayusculas(self):
        assert normalizar_col("ANDALUCÍA") == "andalucia"
        assert normalizar_col("MÚLTIPLE") == "multiple"

    def test_espacios_extra_al_inicio_y_final(self):
        assert normalizar_col("  Madrid  ") == "madrid"

    def test_guiones_se_convierten_en_guiones_bajos(self):
        assert normalizar_col("Castilla-La Mancha") == "castilla_la_mancha"

    def test_elimina_parentesis_y_comas(self):
        assert normalizar_col("Madrid (capital)") == "madrid_capital"
        assert normalizar_col("Valencia, Valencia") == "valencia_valencia"

    def test_elimina_puntos(self):
        assert normalizar_col("S.L.") == "sl"
        assert normalizar_col("S.A.") == "sa"

    def test_texto_limpio_sin_cambios(self):
        assert normalizar_col("industria") == "industria"

    def test_string_vacio(self):
        assert normalizar_col("") == ""

    def test_solo_espacios(self):
        assert normalizar_col("   ") == ""

    def test_guiones_multiples_se_colapsan(self):
        assert normalizar_col("a---b") == "a_b"

    def test_espacios_y_guiones_mezclados(self):
        assert normalizar_col("a - b - c") == "a_b_c"

    def test_retorna_str(self):
        resultado = normalizar_col("test")
        assert isinstance(resultado, str)

    def test_numeros_se_mantienen(self):
        assert normalizar_col("2024") == "2024"
        assert normalizar_col("sector_42") == "sector_42"
