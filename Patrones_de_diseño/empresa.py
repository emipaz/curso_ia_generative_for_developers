"""
empresa.py

Este módulo define la clase Empresa, que representa una entidad
con su información y series temporales. Contiene métodos para calcular
bandas de Bollinger y asignar una calificación.
"""

import pandas as pd
import numpy as np

# Parámetros globales para el análisis
VENTANA_MEDIA = 20
AMPLITUD_BANDA = 2

class Empresa:
    """
    Representa una empresa con información básica y análisis financiero.
    """

    def __init__(self, empresa_id, ticker, nombre):
        self.empresa_id = empresa_id
        self.ticker = ticker
        self.nombre = nombre
        self.serie_temporal = None
        self.media_movil = None
        self.banda_superior = None
        self.banda_inferior = None
        self.calificacion = None

    def cargar_serie_temporal(self, conexion):
        """
        Carga los datos históricos de la empresa desde la base de datos.
        """
        consulta = '''
        SELECT  fecha, valor
        FROM SerieTemporal
        WHERE empresa_id = ?
        ORDER BY fecha
        '''
        self.serie_temporal = pd.read_sql_query(consulta, conexion, params=(self.empresa_id,))
        self.serie_temporal['fecha'] = pd.to_datetime(self.serie_temporal['fecha'])

    def calcular_bandas_bollinger(self):
        """
        Calcula la media móvil y las bandas de Bollinger.
        """
        valores = self.serie_temporal['valor']
        self.media_movil = valores.rolling(VENTANA_MEDIA).mean()
        desviacion = valores.rolling(VENTANA_MEDIA).std()
        self.banda_superior = self.media_movil + (desviacion * AMPLITUD_BANDA)
        self.banda_inferior = self.media_movil - (desviacion * AMPLITUD_BANDA)

    def asignar_calificacion(self):
        """
        Asigna una calificación a la empresa según el último valor registrado.
        """
        ultimo_valor = self.serie_temporal['valor'].iloc[-1]
        if ultimo_valor > self.banda_superior.iloc[-1]:
            self.calificacion = 'A'
        elif ultimo_valor < self.banda_inferior.iloc[-1]:
            self.calificacion = 'C'
        else:
            self.calificacion = 'B'

    def mostrar_informacion(self):
        """
        Muestra en consola la información y análisis de la empresa.
        """
        print(f'Empresa: {self.nombre} ({self.ticker})')
        print(f'Calificación: {self.calificacion}')
        print('Últimos valores de la serie temporal:')
        print(self.serie_temporal.tail())
        print('Media móvil:')
        print(self.media_movil.tail())
        print('Banda superior:')
        print(self.banda_superior.tail())
        print('Banda inferior:')
        print(self.banda_inferior.tail())
