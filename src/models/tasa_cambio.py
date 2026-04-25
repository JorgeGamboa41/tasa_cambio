import os
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import Column, Date, DateTime, String, Float
from .base import Base # Importación relativa
from ..logger import logger

load_dotenv()
class TasaCambio(Base):
    logger.info(f"Definiendo modelo TasaCambio con el Schema ({os.getenv('SCHEMA')})")
    __tablename__ = 'bd_tasa_cambio'
    __table_args__ = {'schema': os.getenv('SCHEMA')}
    
    fch_valor = Column(Date, primary_key=True, nullable=False)
    fch_proc = Column(DateTime, default=datetime.now, nullable=False)
    fuente = Column(String, primary_key=True, nullable=False)
    moneda = Column(String, primary_key=True, nullable=False)
    tasa = Column(Float, nullable=False)