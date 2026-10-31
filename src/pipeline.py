"""Pipeline principal: orquesta todos los pasos."""
import logging
import time
import os
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler('pipeline.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('pipeline')

from ingesta import ingerir_usuarios, ingerir_posts
from limpieza import limpiar_posts, merge_usuarios_posts
from validacion import validar_posts

def ejecutar():
    """Ejecuta el pipeline completo."""
    inicio = time.time()
    logger.info("=" * 50)
    logger.info("Iniciando pipeline...")
    logger.info("=" * 50)

    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)

    try:
        #1. Ingesta
        usuarios = ingerir_usuarios()
        posts = ingerir_posts()
        logger.info("Ingesta completada.")

        #2. Merge
        df = merge_usuarios_posts(posts, usuarios)
        logger.info("Merge completado.")

        #3. Limpieza
        df = limpiar_posts(df)
        logger.info("Limpieza completada.")

        #4. Validación
        validar_posts(df)
        logger.info("Validación completada.")

        #5. Exportación
        parquet_path = output_dir / 'posts_enriquecidos.parquet'
        csv_path = output_dir / 'posts_enriquecidos.csv'

        df.to_parquet(parquet_path, index=False)
        df.to_csv(csv_path, index=False)    

        duration = time.time() - inicio
        logger.info(f"Pipeline completado en {duration:.2f} segundos.")
        logger.info(f"Archivos exportados a: {output_dir.resolve()}")
        logger.info(f" - Parquet: {parquet_path.resolve()}")
        logger.info(f" - CSV: {csv_path.resolve()}")
        logger.info("=" * 50)

        return df  # Devuelve el DataFrame final para posibles usos posteriores

    except Exception as e:
        duration = time.time() - inicio
        logger.critical(f"Pipeline falló después de {duration:.2f} segundos. {type(e).__name__}: {e}", exc_info=True)

if __name__ == "__main__":
    ejecutar()