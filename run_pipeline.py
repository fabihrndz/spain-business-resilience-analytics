import sys
import time
import logging
from pathlib import Path
from nbformat import read, write
from nbconvert.preprocessors import ExecutePreprocessor
 
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%H:%M:%S",
)
 
NOTEBOOKS_DIR = Path("notebooks")
KERNEL_NAME = "python3"
TIMEOUT = 600
 
NOTEBOOKS = [
    "01_extraction_ipc.ipynb",
    "02_extraction_constituidas.ipynb",
    "03_extraction_disueltas.ipynb",
    "04_eda.ipynb",
    "05_transformation.ipynb",
    "06_load.ipynb",
]
 
def ejecutar_notebook(nb_path):
    with open(nb_path, encoding="utf-8") as f:
        nb = read(f, as_version=4)
 
    ep = ExecutePreprocessor(timeout=TIMEOUT)
    ep.preprocess(nb, {"metadata": {"path": NOTEBOOKS_DIR}})
 
    with open(nb_path, "w", encoding="utf-8") as f:
        write(nb, f)
 
def main():
    inicio = time.time()
    ok = 0
 
    for nb_name in NOTEBOOKS:
        nb_path = NOTEBOOKS_DIR / nb_name
        if not nb_path.exists():
            logging.error(f"No encontrado: {nb_path}")
            sys.exit(1)
 
        logging.info(f"Ejecutando {nb_name} ...")
        try:
            ejecutar_notebook(nb_path)
            ok += 1
            logging.info(f"{nb_name} → OK")
        except Exception as e:
            logging.error(f"{nb_name} → FALLÓ: {e}")
            sys.exit(1)
 
    total = time.time() - inicio
    logging.info(f"Pipeline completo: {ok}/{len(NOTEBOOKS)} notebooks en {total:.1f}s")
 
if __name__ == "__main__":
    main()