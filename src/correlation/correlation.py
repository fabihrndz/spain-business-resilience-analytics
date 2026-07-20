"""Módulo de análisis de correlación entre variables.

Proporciona funciones para calcular y visualizar correlaciones
Pearson y Spearman, incluyendo comparación y recomendación
del método más adecuado.
"""

from typing import Any

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def comparar_correlaciones(
    df: pd.DataFrame,
    var1_name: str,
    var2_name: str,
    umbral_diferencia: float = 0.1,
    mostrar_plot: bool = True,
) -> dict[str, Any]:
    """Calcula correlaciones Pearson y Spearman, las compara y recomienda cuál usar.

    Pandas maneja automáticamente los valores NaN.

    Args:
        df: DataFrame que contiene las variables.
        var1_name: Nombre de la primera columna.
        var2_name: Nombre de la segunda columna.
        umbral_diferencia: Diferencia mínima entre coeficientes para
            considerar que hay discrepancia (por defecto 0.1).
        mostrar_plot: Si True, muestra un scatter plot de las variables.

    Returns:
        Diccionario con:
            - pearson: coeficiente de Pearson
            - spearman: coeficiente de Spearman
            - diferencia: diferencia absoluta entre ambos
            - recomendacion: 'pearson' o 'spearman'
            - valor_recomendado: el valor del coeficiente recomendado
            - fuerza: fuerza de la relación (muy débil, débil, moderada, etc.)
            - direccion: 'positiva' o 'negativa'
            - n_validos: número de pares válidos
            - n_total: número total de filas
            - interpretacion: texto explicativo

    Raises:
        ValueError: Si las columnas no existen en el DataFrame.
    """
    # Verificar que las columnas existen
    if var1_name not in df.columns or var2_name not in df.columns:
        raise ValueError(
            f"Las columnas '{var1_name}' y/o '{var2_name}' no existen en el DataFrame"
        )

    # Calcular correlaciones (pandas maneja NaN automáticamente)
    pearson_r = df[var1_name].corr(df[var2_name], method="pearson")
    spearman_r = df[var1_name].corr(df[var2_name], method="spearman")

    # Calcular diferencia absoluta
    diferencia = abs(pearson_r - spearman_r)

    # Contar valores válidos (sin NaN en ambas columnas)
    datos_validos = df[[var1_name, var2_name]].dropna()
    n_validos = len(datos_validos)
    n_total = len(df)

    # Decidir cuál recomendar
    if diferencia < umbral_diferencia:
        recomendacion = "pearson"
        valor_recomendado = pearson_r
        interpretacion = (
            f"USAR PEARSON (r = {pearson_r:.3f})\n"
            f"  La diferencia entre Pearson y Spearman es pequeña ({diferencia:.3f})."
            f" Relación aproximadamente lineal sin outliers significativos."
        )
    else:
        recomendacion = "spearman"
        valor_recomendado = spearman_r
        interpretacion = (
            f"USAR SPEARMAN (r = {spearman_r:.3f})\n"
            f"  Diferencia notable entre Pearson y Spearman ({diferencia:.3f})."
            f" Posible presencia de outliers o relación no lineal."
        )

    # Interpretación de la fuerza
    fuerza_abs = abs(valor_recomendado)
    if fuerza_abs < 0.2:
        fuerza = "muy débil"
    elif fuerza_abs < 0.4:
        fuerza = "débil"
    elif fuerza_abs < 0.6:
        fuerza = "moderada"
    elif fuerza_abs < 0.8:
        fuerza = "fuerte"
    else:
        fuerza = "muy fuerte"

    direccion = "positiva" if valor_recomendado > 0 else "negativa"

    interpretacion += f"\n  Fuerza de la relación: {fuerza} {direccion}"

    # Mostrar scatter plot si se solicita
    if mostrar_plot:
        plt.figure(figsize=(10, 6))
        plt.scatter(
            datos_validos[var1_name],
            datos_validos[var2_name],
            alpha=0.5,
            edgecolors="k",
            linewidth=0.5,
        )
        plt.xlabel(var1_name, fontsize=12)
        plt.ylabel(var2_name, fontsize=12)
        plt.title(
            f"Scatter Plot: {var1_name} vs {var2_name}\n"
            f"Pearson: {pearson_r:.3f} | Spearman: {spearman_r:.3f} | "
            f"Recomendado: {recomendacion.upper()}",
            fontsize=14,
            fontweight="bold",
        )
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

    return {
        "pearson": pearson_r,
        "spearman": spearman_r,
        "diferencia": diferencia,
        "recomendacion": recomendacion,
        "valor_recomendado": valor_recomendado,
        "fuerza": fuerza,
        "direccion": direccion,
        "n_validos": n_validos,
        "n_total": n_total,
        "interpretacion": interpretacion,
    }


def matriz_correlacion_visual(
    df: pd.DataFrame,
    metodo: str = "pearson",
    figsize: tuple[int, int] = (15, 15),
    cmap: str = "mako",
    annot: bool = True,
    fmt: str = ".2f",
    solo_triangulo: bool = True,
) -> pd.DataFrame:
    """Crea un heatmap visual de la matriz de correlación de un DataFrame.

    Args:
        df: DataFrame con las variables numéricas a correlacionar.
        metodo: Método de correlación ('pearson', 'spearman' o 'kendall').
        figsize: Tamaño de la figura (ancho, alto).
        cmap: Paleta de colores (ej: 'mako', 'coolwarm', 'viridis').
        annot: Si True, muestra los valores numéricos en cada celda.
        fmt: Formato de los números (ej: '.2f' = 2 decimales).
        solo_triangulo: Si True, muestra solo el triángulo inferior.

    Returns:
        Matriz de correlación calculada como DataFrame.
    """
    # Calcular la matriz de correlación
    df_correlaciones = df.corr(method=metodo, numeric_only=True)

    # Crear la figura
    plt.figure(figsize=figsize)

    # Crear máscara para el triángulo superior (si se solicita)
    if solo_triangulo:
        mask = np.triu(np.ones_like(df_correlaciones, dtype=bool))
    else:
        mask = None

    # Crear el heatmap
    sns.heatmap(
        df_correlaciones,
        annot=annot,
        fmt=fmt,
        cmap=cmap,
        vmax=1,
        vmin=-1,
        mask=mask,
        square=True,
        linewidths=0.5,
        cbar_kws={"shrink": 0.8},
    )

    plt.title(
        f"Matriz de Correlación ({metodo.capitalize()})",
        fontsize=16,
        fontweight="bold",
        pad=20,
    )

    plt.tight_layout()
    plt.show()

    return df_correlaciones
