"""Pipeline principal de ejecución de notebooks ETL.

Ejecuta secuencialmente los notebooks del pipeline de extracción,
transformación y carga de datos del proyecto Spain Business Resilience Analytics.

Uso:
    python run_pipeline.py
"""

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
    "06_visualizations.ipynb",
    "07_correlation.ipynb",
    "08_load.ipynb",
]


def ejecutar_notebook(nb_path: Path) -> None:
    """Ejecuta un notebook Jupyter y sobreescribe el archivo con los outputs.

    Args:
        nb_path: Ruta al archivo .ipynb a ejecutar.

    Raises:
        Exception: Si la ejecución del notebook falla (timeout, error en celda, etc.).
    """
    with open(nb_path, encoding="utf-8") as f:
        nb = read(f, as_version=4)

    ep = ExecutePreprocessor(timeout=TIMEOUT, kernel_name=KERNEL_NAME)
    ep.preprocess(nb, {"metadata": {"path": NOTEBOOKS_DIR}})

    with open(nb_path, "w", encoding="utf-8") as f:
        write(nb, f)


def main() -> None:
    """Ejecuta todos los notebooks del pipeline en orden secuencial.

    Registra el tiempo total de ejecución y reporta éxitos/fallos.
    Termina con código de salida no-cero si algún notebook falla.
    """
    inicio = time.time()
    ok = 0
    fallidos: list[str] = []

    for nb_name in NOTEBOOKS:
        nb_path = NOTEBOOKS_DIR / nb_name
        if not nb_path.exists():
            logging.error(f"No encontrado: {nb_path}")
            fallidos.append(nb_name)
            continue

        logging.info(f"Ejecutando {nb_name} ...")
        try:
            ejecutar_notebook(nb_path)
            ok += 1
            logging.info(f"{nb_name} OK")
        except Exception as e:
            logging.error(f"{nb_name} FALLO: {e}")
            fallidos.append(nb_name)

    total = time.time() - inicio

    if fallidos:
        logging.error(
            f"Pipeline completado con errores: "
            f"{ok}/{len(NOTEBOOKS)} notebooks OK, "
            f"{len(fallidos)} fallaron ({', '.join(fallidos)}) "
            f"en {total:.1f}s"
        )
        sys.exit(1)
    else:
        logging.info(
            f"Pipeline completo: {ok}/{len(NOTEBOOKS)} notebooks en {total:.1f}s"
        )


if __name__ == "__main__":
    main()
