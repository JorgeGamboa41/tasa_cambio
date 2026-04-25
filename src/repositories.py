from sqlalchemy.orm import Session
from .models import TasaCambio
from datetime import date

class TasaCambioRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, tasa_obj: TasaCambio):
        """Guarda o actualiza una tasa."""
        self.db.add(tasa_obj)  # Agrega el objeto a la sesión
        self.db.commit()  # Confirma la transacción