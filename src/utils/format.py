from datetime import datetime
import locale
    
def FormatDate(date):
    
    try:
        # Configurar locale a español para reconocer días de semana y meses
        # Nota: En Windows puede ser 'spanish' o 'es-ES'
        try:
            locale.setlocale(locale.LC_TIME, 'es_ES')
        except locale.Error:
            locale.setlocale(locale.LC_TIME, 'spanish')

        # strptime convierte cadena a datetime.
        # %A: Día completo, %d: Día, %B: Mes completo, %Y: Año
        return datetime.strptime(date, "%A, %d %B %Y").date()
    except Exception as e:
        return datetime.now().date() # Fallback a hoy si falla