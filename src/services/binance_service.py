import requests
from datetime import datetime
from src.models import TasaCambio
from src.repositories import TasaCambioRepository
from src.logger import logger
class BinanceService:
    def __init__(self, repository: TasaCambioRepository):
        self.repository = repository
        self.url_api = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

    def fetch_and_save_p2p(self):
        """Obtiene el promedio de los primeros 10 anuncios y guarda en DB"""
        payload = {
            "asset": "USDT",
            "fiat": "VES",
            "merchantCheck": True,
            "page": 1,
            "publisherType": "merchant",
            "rows": 10,
            "tradeType": "BUY"
        }

        try:
            response = requests.post(self.url_api, json=payload, timeout=15)
            response.raise_for_status()
            data = response.json()

            if not data.get('data'):
                logger.warning("No se obtuvieron datos de Binance.")
                return

            # Cálculo del promedio
            precios = [float(adv['adv']['price']) for adv in data['data']]
            promedio_p2p = sum(precios) / len(precios)

            # Crear objeto del modelo
            nueva_tasa = TasaCambio(
                fch_valor=datetime.now().date(),
                fch_proc=datetime.now(),
                fuente="Binance P2P",
                moneda="USD",
                tasa=round(promedio_p2p, 2)
            )

            # Guardar usando el repositorio existente
            self.repository.save(nueva_tasa)
            logger.info(f"Promedio Binance P2P {round(promedio_p2p, 2)} procesado y guardado correctamente.")

        except Exception as e:
            logger.error(f"❌ Error en BinanceService: {e}")