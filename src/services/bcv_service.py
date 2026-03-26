import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from src.utils import FormatDate
from src.models import TasaCambio
from src.repositories import TasaCambioRepository
from src.logger import logger

class BCVService:
    def __init__(self, repository: TasaCambioRepository):
        # Inyectamos el repositorio para no depender de la DB directamente
        self.repository = repository
        self.url = "https://www.bcv.org.ve/"
        self.cert = os.getenv('RUTA_CERTIFICADO')

    def _parse_date(self, soup):
        """Lógica interna para formatear la fecha del BCV"""
        # Aquí puedes usar tu función FormatDate o implementarla directamente
        fecha_str = FormatDate(soup.find('span', class_='date-display-single').text.strip())
        # Ejemplo rápido de conversión (ajustar según tu FormatDate original)
        return fecha_str 

    def fetch_and_save_rates(self):
        """Extrae USD y EUR y los guarda usando el repositorio"""
        try:
            response = requests.get(self.url, verify=self.cert, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            fecha_valor = self._parse_date(soup)
            
            # Definimos las monedas a extraer para evitar repetir código
            monedas = [
                {'id': 'dolar', 'iso': 'USD'},
                {'id': 'euro', 'iso': 'EUR'}
            ]

            for m in monedas:
                valor_texto = soup.find('div', id=m['id']).find('strong').text.strip()
                valor_float = float(valor_texto.replace(',', '.'))

                nueva_tasa = TasaCambio(
                    fch_valor=fecha_valor,
                    fch_proc=datetime.now(),
                    fuente="BCV",
                    moneda=m['iso'],
                    tasa=valor_float
                )
                
                # Delegamos la persistencia al repositorio
                self.repository.save(nueva_tasa)

            logger.info(f"Tasas BCV del {fecha_valor}, procesadas y guardadas correctamente.")

        except Exception as e:
            logger.error(f"Error en BCVService: {e}")
            # El rollback lo maneja el repositorio en su método .save()