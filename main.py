from src.database import SessionLocal, engine
from src.models import Base
from src.repositories import TasaCambioRepository
from src.services.bcv_service import BCVService
from src.services.binance_service import BinanceService
from src.logger import logger

# Asegurar que las tablas existan
Base.metadata.create_all(bind=engine)

def job_actualizacion_tasas():
    db = SessionLocal()
    try:
        # 1. Instanciar el repositorio una sola vez
        repo = TasaCambioRepository(db)
        
        # 2. Instanciar los servicios inyectando el repositorio
        bcv = BCVService(repo)
        binance = BinanceService(repo)
        
        # 3. Ejecutar actualizaciones
        logger.info("Iniciando actualización de tasas...")
        bcv.fetch_and_save_rates()
        binance.fetch_and_save_p2p()
        
    finally:
        db.close()

if __name__ == "__main__":
    job_actualizacion_tasas()