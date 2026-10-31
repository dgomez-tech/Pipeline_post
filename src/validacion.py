"""Módulo de validación: reglas de calidad que los datos DEBEN cumplir."""
import pandas as pd
import logging

logger = logging.getLogger('pipeline.validacion')

class ValidacionError(Exception):
    """Los datos no pasan las reglas de calidad."""
    pass

def validar_posts(df: pd.DataFrame) -> None:
    """Valida el DataFrame de posts contra reglas de calidad."""
    errores = []

    # Regla 1: No vacio
    if df.empty:
        errores.append("El DataFrame está vacío.")

    # Regla 2: Columnas requeridas
    columnas_requeridas = {'post_id', 'user_id', 'title', 'body', 'autor_nombre'}
    faltantes = columnas_requeridas - set(df.columns)
    if faltantes:
        errores.append(f"Faltan columnas requeridas: {faltantes}")

    # si faltan columnas las reglas siguientes no se pueden aplicar
    if errores:
        msg = "Validación fallida:\n" + "\n".join(f"  - {e}" for e in errores)
        logger.error(msg)
        raise ValidacionError(msg)

    # A partir de aquí, asumimos que las columnas existen
    # Regla 3: Sin duplicados en post_id
    duplicados = df['post_id'].duplicated().sum()
    if duplicados > 0:
        errores.append(f"Existen {duplicados} post_id duplicados.")

    # Regla 4: Titulo no vacío
    titulos_vacios = df['title'].str.strip().eq('').sum()
    if titulos_vacios > 0:
        errores.append(f"Existen {titulos_vacios} títulos vacíos.")

    # Regla 5: body_length razonable (>0)
    if 'body_length' in df.columns:
        bodies_vacios = (df['body_length'] == 0).sum()
        if bodies_vacios > 0:
            errores.append(f"Existen {bodies_vacios} posts con body_length = 0.")

    if errores:
        msg = "Validación fallida:\n" + "\n".join(f"  - {e}" for e in errores)
        logger.error(msg)
        raise ValidacionError(msg)

    logger.info("Validación exitosa: todos los checks pasaron.")


