"""Configuración de URLs de la API del INE.

Define los endpoints de la API REST del Instituto Nacional de Estadística
para cada dataset utilizado en el proyecto.
"""

INE_BASE_URL = "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA"

API_URLS: dict[str, str] = {
    "ipc": f"{INE_BASE_URL}/76136?nlast=60&det=2",
    "constituidas": f"{INE_BASE_URL}/13913",
    "disueltas": f"{INE_BASE_URL}/13915",
}
