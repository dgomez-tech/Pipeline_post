"""Módulo de ingesta: extrae datos de APIs externas."""
import requests
import pandas as pd
import logging
import time

logger = logging.getLogger('pipeline.ingesta')

def pedir_con_reintentos(url, max_intentos: int = 3) -> list:
    """Petición GET robusta con reintentos y backoff exponencial."""
    for intento in range(max_intentos):
        try:
            response = requests.get(url, timeout=10)  # Timeout de 10 segundos
            response.raise_for_status()  # Lanza un error para códigos de estado 4xx/5xx
            return response.json()
        except (requests.exceptions.RequestException) as e:
            if intento < max_intentos - 1:
                espera = 2 ** intento  # Backoff exponencial
                logger.warning(f"Intento {intento+1} fallido: {e}. Esperando {espera}s...")
                time.sleep(espera)
            else:
                logger.error(f"Todos los intentos fallaron para la URL: {url}")
                raise


def ingerir_usuarios() -> pd.DataFrame:
    """Ingiere usuarios de JSONPlaceholder."""
    logger.info("Iniciando ingesta de usuarios...")
    data = pedir_con_reintentos("https://jsonplaceholder.typicode.com/users")
    df = pd.json_normalize(data, sep='_')
    df = df[['id', 'name', 'username', 'email', 'address_city', 'company_name']].rename(columns={
        'id': 'user_id',
        'name': 'autor_nombre',
        'address_city': 'autor_ciudad',
        'company_name': 'autor_empresa'
    })
    logger.info(f"Ingesta de usuarios completada. Total registros: {len(df)}")
    return df

def ingerir_posts() -> pd.DataFrame:
    """Ingiere posts de JSONPlaceholder."""
    logger.info("Iniciando ingesta de posts...")
    data = pedir_con_reintentos("https://jsonplaceholder.typicode.com/posts")
    df = pd.DataFrame(data)
    df = df.rename(columns={'userId': 'user_id', 'id': 'post_id'})
    logger.info(f"Ingesta de posts completada. Total registros: {len(df)}")
    return df