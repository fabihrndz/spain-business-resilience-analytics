import logging
import requests
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
 
def llamada_api(url):
    logger.info(f"Iniciando llamada a API: {url}")
 
    try:
        response = requests.get(url)
        logger.info(f"Status code recibido: {response.status_code}")
        if response.status_code == 200:
            logger.debug(f"Payload recibido: {response.text[:300]}")
            return response.json()
        logger.warning(f"Respuesta inesperada: {response.status_code} - {response.text}")
        return None
 
    except requests.exceptions.Timeout:
        logger.error("Timeout al conectar con la API")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error en la conexión: {e}")
    return None

 