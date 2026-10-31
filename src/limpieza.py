"""Módulo de limpieza: transforma datos crudos en datos usables."""
import pandas as pd
import logging

logger = logging.getLogger('pipeline.limpieza')

def merge_usuarios_posts(posts: pd.DataFrame, usuarios: pd.DataFrame) -> pd.DataFrame:
    """Combina los DataFrames de usuarios y posts en uno solo."""
    logger.info(f"Combinando {len(posts)} posts con {len(usuarios)} usuarios...")
    df = posts.merge(usuarios, on='user_id', how='left')
    sin_autor = df['autor_nombre'].isnull().sum()
    if sin_autor > 0:
        logger.warning(f"{sin_autor} posts sin autor asociado")
    return df


def limpiar_posts(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia el DataFrame de posts enriquecido."""
    df = df.copy()
    filas_antes = len(df)
    logger.info(f"Limpieza de posts: {filas_antes} registros antes de la limpieza.")

    # Eliminar duplicados
    df = df.drop_duplicates(subset=['post_id'], keep='first')
    logger.info(f"Después de eliminar duplicados: {len(df)} registros.")

    # Eliminar post sin título
    df = df.dropna(subset=['title'])
    logger.info(f"Después de eliminar posts sin título: {len(df)} registros.")

    # Normalizar texto
    df['title'] = df['title'].str.strip().str.capitalize()
    df['autor_nombre'] = df['autor_nombre'].str.strip().str.title()
    df['autor_ciudad'] = df['autor_ciudad'].fillna('Desconocida').str.strip().str.title()

    # Crear una columna de longitud del body
    df['body_length'] = df['body'].str.len()

    # Eliminar columna email (PII - no la necesitamos en el output)
    if 'email' in df.columns:
        df = df.drop(columns=['email'])
        logger.info("Columna 'email' eliminada por contener PII.")

    filas_despues = len(df)
    logger.info(f"Limpieza de posts completada: {filas_antes} -> {filas_despues} filas.")

    return df.reset_index(drop=True)

