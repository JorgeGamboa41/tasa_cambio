import logging
import os

def setup_logger():
    # Crear carpeta de logs si no existe
    if not os.path.exists('logs'):
        os.makedirs('logs')

    logger = logging.getLogger('AppTasas')
    logger.setLevel(logging.INFO)

    # Formato de los mensajes: Fecha - Nombre - Módulo - Nivel - Mensaje
    formatter = logging.Formatter('%(asctime)s | %(name)s | %(module)-15s | %(levelname)s | %(message)s')

    # Manejador para consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Manejador para archivo (se guarda en logs/app.log)
    file_handler = logging.FileHandler('logs/app.log')
    file_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger

# Instancia global para importar fácilmente
logger = setup_logger()