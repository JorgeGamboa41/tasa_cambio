from sqlalchemy.orm import Session
from .models import TasaCambio
from datetime import date

class TasaCambioRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, tasa_obj: TasaCambio):
        """Guarda o actualiza una tasa."""
        self.db.add(tasa_obj)  # Agrega el objeto a la sesión
        self.db.commit()

    def get_by_date(self, fecha: date, moneda: str = 'USD'):
        """Busca una tasa específica por fecha y moneda."""
        return self.db.query(TasaCambio).filter(
            TasaCambio.fch_valor == fecha,
            TasaCambio.moneda == moneda
        ).first()

    def get_latest_rate(self, moneda: str = 'USD'):
        """Obtiene la última tasa registrada (útil para el inventario)."""
        return self.db.query(TasaCambio)\
            .filter(TasaCambio.moneda == moneda)\
            .order_by(TasaCambio.fch_valor.desc())\
            .first()