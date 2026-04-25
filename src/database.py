import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models.base import Base
from .logger import logger

load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
logger.info(f"Nueva sesión de DB iniciada")
logger.info(f"Host   → {os.getenv('DB_HOST')}")
logger.info(f"Puerto → {os.getenv('DB_PORT')}")
logger.info(f"BD     → {os.getenv('DB_NAME')}")

def get_db():
    """Generador para manejar la sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()