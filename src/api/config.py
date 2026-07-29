"""Configuración de endpoints de la API del INE.

Define las URLs base y los endpoints específicos para las tablas
de IPC, sociedades constituidas y disueltas.
"""

INE_BASE_URL = "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA"
 
API_URLS = {

    "ipc": f"{INE_BASE_URL}/76136?nlast=60&det=2",

    "constituidas": f"{INE_BASE_URL}/13913",

    "disueltas": f"{INE_BASE_URL}/13915",

}