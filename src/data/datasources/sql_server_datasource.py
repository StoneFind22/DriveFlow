# src/data/datasources/sql_server_datasource.py
#
# Capa de Datos (DataSource).
# Implementación concreta del acceso a la base de datos (SQL Server).
# Implementa el patrón Singleton para asegurar una única conexión.

import pyodbc
from tkinter import messagebox

class SQLServerDataSource:
    
    _instance = None
    
    @classmethod
    def get_instance(cls, server: str, database: str, username: str = None, password: str = None):
        """
        Método estático para obtener la instancia única (Singleton).
        """
        if cls._instance is None:
            # Si no existe instancia, crea una nueva pasándole los parámetros.
            cls._instance = cls(
                server=server,
                database=database,
                username=username,
                password=password
            )
        return cls._instance

    def __init__(self, server: str, database: str, username: str = None, password: str = None):
        """
        Constructor privado. Es llamado solo por get_instance() la primera vez.
        """
        if SQLServerDataSource._instance is not None:
            raise Exception("Esta clase es un Singleton. Use get_instance().")
        
        self.connection = None
        self.cursor = None
        self.sql_driver = None
        
        # Conectar usando los parámetros recibidos
        self._connect(server, database, username, password)

    def _connect(self, server: str, database: str, username: str, password: str):
        """
        Establece la conexión con la base de datos SQL Server.
        """
        try:
            available_drivers = pyodbc.drivers()
            preferred_drivers = [
                "ODBC Driver 18 for SQL Server",
                "ODBC Driver 17 for SQL Server", 
                "ODBC Driver 13 for SQL Server",
                "SQL Server"
            ]
            
            for driver in preferred_drivers:
                if driver in available_drivers:
                    self.sql_driver = driver
                    break
            
            if not self.sql_driver:
                raise Exception("No se encontró ningún driver SQL Server compatible (ej. ODBC Driver 17/18).")
            
            # Construir cadena de conexión
            if username and password:
                connection_string = (
                    f"DRIVER={{{self.sql_driver}}};"
                    f"SERVER={server};"
                    f"DATABASE={database};"
                    f"UID={username};"
                    f"PWD={password};"
                    f"TrustServerCertificate=yes;" 
                )
            else:
                # Autenticación de Windows
                connection_string = (
                    f"DRIVER={{{self.sql_driver}}};"
                    f"SERVER={server};"
                    f"DATABASE={database};"
                    f"Trusted_Connection=yes;"
                    f"TrustServerCertificate=yes;" 
                )
            
            self.connection = pyodbc.connect(connection_string)
            self.cursor = self.connection.cursor()
            print(f"Conectado exitosamente usando: {self.sql_driver}")
            
        except (pyodbc.Error, Exception) as e:
            # Relanzar la excepción para que main.py la capture
            raise Exception(f"Error al conectar a la DB: {e}")
    
    def execute_query(self, query, params=None):
        """
        Ejecuta una consulta SELECT y retorna todos los resultados.
        """
        try:
            if self.cursor:
                self.cursor.execute(query, params if params is not None else [])
                return self.cursor.fetchall()
            else:
                raise Exception("No hay conexión a la base de datos.")
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            messagebox.showerror("Error de Consulta", f"Error al ejecutar consulta:\nSQLSTATE: {sqlstate}\nMensaje: {ex.args[1]}")
            return None
        except Exception as e:
            messagebox.showerror("Error de Consulta", f"Ocurrió un error inesperado al ejecutar consulta:\n{str(e)}")
            return None
    
    def execute_non_query(self, query, params=None):
        """
        Ejecuta una consulta INSERT, UPDATE o DELETE y confirma los cambios.
        """
        try:
            if self.cursor:
                self.cursor.execute(query, params if params is not None else [])
                self.connection.commit()
                return True
            else:
                raise Exception("No hay conexión a la base de datos.")
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            messagebox.showerror("Error de Operación", f"Error al ejecutar operación:\nSQLSTATE: {sqlstate}\nMensaje: {ex.args[1]}")
            self.connection.rollback()
            return False
        except Exception as e:
            messagebox.showerror("Error de Operación", f"Ocurrió un error inesperado al ejecutar operación:\n{str(e)}")
            self.connection.rollback()
            return False
            
    def close(self):
        """Cierra la conexión y el cursor de la base de datos."""
        if self.cursor:
            self.cursor.close()
            self.cursor = None
        if self.connection:
            self.connection.close()
            self.connection = None

