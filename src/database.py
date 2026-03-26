import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models.base import Base
from .logger import logger

load_dotenv('config/online/.env')

DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
logger.info(f"Nueva sesión de DB iniciada, en el host y puerto: {os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}")

def get_db():
    """Generador para manejar la sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()