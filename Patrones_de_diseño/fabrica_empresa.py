"""
fabrica_empresa.py

Este módulo define la clase FabricaEmpresa que implementa el patrón
Factory Method para crear objetos Empresa a partir de distintos criterios.
"""

from empresa import Empresa

class FabricaEmpresa:
    """
    Fábrica responsable de crear instancias de Empresa desde la base de datos.
    """

    @staticmethod
    def crear_por_ticker(ticker, conexion):
        """
        Crea una Empresa a partir de su ticker.
        """
        cursor = conexion.cursor()
        consulta = 'SELECT id, ticker, nombre FROM empresas WHERE ticker = ?'
        cursor.execute(consulta, (ticker,))
        fila = cursor.fetchone()
        if fila:
            return Empresa(fila[0], fila[1], fila[2])
        else:
            raise ValueError("Ticker no encontrado.")

    @staticmethod
    def crear_por_id(id_empresa, conexion):
        """
        Crea una Empresa a partir de su ID.
        """
        cursor = conexion.cursor()
        consulta = 'SELECT id, ticker, nombre FROM empresas WHERE id = ?'
        cursor.execute(consulta, (id_empresa,))
        fila = cursor.fetchone()
        if fila:
            return Empresa(fila[0], fila[1], fila[2])
        else:
            raise ValueError("ID de empresa no encontrado.")

    @staticmethod
    def crear(id_o_ticker, conexion):
        """
        Crea una Empresa según el tipo de identificador (ID o ticker).
        """
        cursor = conexion.cursor()
        if isinstance(id_o_ticker, int):
            consulta = 'SELECT id, ticker, nombre FROM empresas WHERE id = ?'
        else:
            consulta = 'SELECT id, ticker, nombre FROM empresas WHERE ticker = ?'
        cursor.execute(consulta, (id_o_ticker,))
        fila = cursor.fetchone()
        if fila:
            return Empresa(fila[0], fila[1], fila[2])
        else:
            raise ValueError("Identificador no válido o empresa no encontrada.")
