def int_a_str (df, lista_columnas):
    """
    Transforma múltiples columnas a str en un solo DataFrame.
    """
    # Recorremos la lista de columnas que le pasamos
    for columna in lista_columnas:
        if columna in df.columns:
            df[columna] = df[columna].astype(str)
            print(f"-> Columna '{columna}' convertida a str.")
        else:
            print(f"⚠️ Alerta: La columna '{columna}' no existe en este DataFrame.")
            
    return df