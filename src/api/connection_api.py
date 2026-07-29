"""Módulo de conexión a la API del INE con caché y logging.

Proporciona funciones para realizar llamadas a la API REST del Instituto
Nacional de Estadística, con sistema de caché local para evitar
solicitudes repetidas.
"""

import json
import logging
import os
import re
from typing import Any

import requests

logger = logging.getLogger(__name__)

CACHE_DIR: str = os.path.join(os.path.dirname(__file__), "..", "..", "files", "cache")


def _get_cache_path(url: str) -> str:
    """Extrae el ID de tabla de la URL para nombrar el archivo de caché.

    Args:
        url: URL del endpoint de la API del INE.

    Returns:
        Ruta completa al archivo JSON de caché.

    """
    match = re.search(r"/DATOS_TABLA/(\d+)", url)
    nombre = match.group(1) if match else "unknown"
    return os.path.join(CACHE_DIR, f"{nombre}.json")


def llamada_api(url: str) -> dict[str, Any] | list[Any] | None:
    """Realiza una llamada a la API del INE con sistema de caché.

    Consulta primero la caché local; si no existe o está corrupta,
    realiza la petición HTTP y almacena el resultado.

    Args:
        url: URL completa del endpoint de la API del INE.

    Returns:
        Datos JSON parseados (dict o list) si la respuesta es 200,
        None en caso de error o timeout.

    """
    cache_path = _get_cache_path(url)

    # Intentar leer de caché
    if os.path.exists(cache_path):
        logger.info(f"Usando caché: {cache_path}")
        try:
            with open(cache_path, encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError):
            logger.warning(f"Caché corrupto, se descargará de nuevo: {cache_path}")

    # Llamada real a la API
    logger.info(f"Iniciando llamada a API: {url}")

    try:
        response = requests.get(url)
        logger.info(f"Status code recibido: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            # Guardar en caché
            os.makedirs(CACHE_DIR, exist_ok=True)
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)
            logger.info(f"Guardado en caché: {cache_path}")
            return data

        logger.warning(f"Respuesta inesperada: {response.status_code} - {response.text}")
        return None

    except requests.exceptions.Timeout:
        logger.error("Timeout al conectar con la API")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error en la conexión: {e}")

    return None
