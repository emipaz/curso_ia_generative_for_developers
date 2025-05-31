"""
singleton_db.py

Este módulo implementa el patrón Singleton para gestionar una única conexión
a la base de datos SQLite en toda la aplicación. 
Permite reutilizar la misma conexión en distintas partes del código.
"""

import sqlite3

class ConexionDB:
    """
    Clase Singleton para manejar una única conexión a la base de datos SQLite.
    """

    _instancia = None  # Almacena la única instancia de la clase

    def __init__(self, nombre_bd='empresa.db'):
        """
        Constructor que inicializa la conexión si aún no existe.
        """
        if ConexionDB._instancia is not None:
            raise Exception("Esta clase es un Singleton. Usá get_instancia().")
        self.nombre_bd = nombre_bd
        self.conexion = sqlite3.connect(nombre_bd)
        ConexionDB._instancia = self

    @staticmethod
    def get_instancia(nombre_bd='empresa.db'):
        """
        Método estático para obtener la instancia única del Singleton.
        """
        if ConexionDB._instancia is None:
            ConexionDB(nombre_bd)
        return ConexionDB._instancia

    def obtener_conexion(self):
        """
        Devuelve el objeto de conexión SQLite.
        """
        return self.conexion

    def cerrar_conexion(self):
        """
        Cierra la conexión a la base de datos.
        """
        if self.conexion:
            self.conexion.close()
            ConexionDB._instancia = None
