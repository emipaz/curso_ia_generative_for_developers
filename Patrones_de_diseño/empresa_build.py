import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime

# Parámetros globales para el cálculo de las bandas de Bollinger
ANCHO_BANDA = 2
VENTANA_MOVIL = 20

class Empresa:
    """
    Representa una empresa con series temporales y análisis técnico.
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

    def mostrar(self):
        """
        Muestra por pantalla la información de la empresa y los cálculos.
        """
        print(f'Empresa: {self.nombre} ({self.ticker})')
        print(f'Calificación: {self.calificacion}')
        print('Últimos valores de la serie temporal:')
        print(self.serie_temporal.tail())
        print('Media Móvil:')
        print(self.media_movil.tail())
        print('Banda Superior:')
        print(self.banda_superior.tail())
        print('Banda Inferior:')
        print(self.banda_inferior.tail())


class EmpresaBuilder:
    """
    Builder que permite construir objetos Empresa de forma modular.
    """
    def __init__(self, conexion):
        self.conexion = conexion
        self.empresa = None

    def obtener_por_ticker(self, ticker):
        """
        Busca una empresa por ticker y la inicializa en el builder.
        """
        cursor = self.conexion.cursor()
        cursor.execute('SELECT id, ticker, nombre FROM empresas WHERE ticker = ?', (ticker,))
        fila = cursor.fetchone()
        if fila:
            self.empresa = Empresa(fila[0], fila[1], fila[2])
        return self

    def con_serie_temporal(self):
        """
        Carga la serie temporal de la empresa desde la base de datos.
        """
        if self.empresa:
            consulta = '''
                SELECT fecha, valor
                FROM SerieTemporal
                WHERE empresa_id = ?
                ORDER BY fecha
            '''
            df = pd.read_sql_query(consulta, self.conexion, params=(self.empresa.empresa_id,))
            df['fecha'] = pd.to_datetime(df['fecha'])
            self.empresa.serie_temporal = df
        return self

    def con_bandas_bollinger(self):
        """
        Calcula las bandas de Bollinger para la serie temporal.
        """
        if self.empresa and self.empresa.serie_temporal is not None:
            valores = self.empresa.serie_temporal['valor']
            media = valores.rolling(VENTANA_MOVIL).mean()
            desviacion = valores.rolling(VENTANA_MOVIL).std()
            self.empresa.media_movil = media
            self.empresa.banda_superior = media + (desviacion * ANCHO_BANDA)
            self.empresa.banda_inferior = media - (desviacion * ANCHO_BANDA)
        return self

    def con_calificacion(self):
        """
        Asigna una calificación basada en la posición del último valor respecto a las bandas.
        """
        if self.empresa and self.empresa.serie_temporal is not None:
            ultimo_valor = self.empresa.serie_temporal['valor'].iloc[-1]
            banda_sup = self.empresa.banda_superior.iloc[-1]
            banda_inf = self.empresa.banda_inferior.iloc[-1]

            if ultimo_valor > banda_sup:
                self.empresa.calificacion = 'A'
            elif ultimo_valor < banda_inf:
                self.empresa.calificacion = 'C'
            else:
                self.empresa.calificacion = 'B'
        return self

    def build(self):
        """
        Devuelve el objeto Empresa finalizado.
        """
        return self.empresa
