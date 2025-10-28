# src/data/repositories/cliente_repository_impl.py
#
# Capa de Datos (Implementación del Repositorio).
# Conecta la interfaz del dominio con el DataSource.

from typing import List, Optional
from src.domain.models.cliente import Cliente
from src.domain.repositories.cliente_repository import IClienteRepository
from src.data.datasources.sql_server_datasource import SQLServerDataSource

class ClienteRepositoryImpl(IClienteRepository):
    
    def __init__(self, datasource: SQLServerDataSource):
        """
        Constructor que recibe la inyección de dependencia del DataSource.
        
        Args:
            datasource (SQLServerDataSource): La instancia única del DataSource.
        """
        self.datasource = datasource

    def _mapear_a_cliente(self, row: tuple) -> Cliente:
        """
        Convierte una fila de la base de datos en un objeto Cliente.
        """
        return Cliente(
            id=row[0],
            nombre=row[1],
            apellido=row[2],
            dni=row[3],
            licencia=row[4],
            telefono=row[5],
            email=row[6],
            direccion=row[7],
            distrito=row[8]
        )

    def get_all(self) -> List[Cliente]:
        query = "SELECT ClienteID, Nombre, Apellido, DNI, Licencia, Telefono, Email, ISNULL(Direccion, ''), ISNULL(Distrito, '') FROM Clientes ORDER BY Apellido, Nombre"
        results = self.datasource.execute_query(query)
        return [self._mapear_a_cliente(row) for row in results]

    def get_by_id(self, id: int) -> Optional[Cliente]:
        query = "SELECT ClienteID, Nombre, Apellido, DNI, Licencia, Telefono, Email, ISNULL(Direccion, ''), ISNULL(Distrito, '') FROM Clientes WHERE ClienteID = ?"
        params = (id,)
        results = self.datasource.execute_query(query, params)
        if results:
            return self._mapear_a_cliente(results[0])
        return None

    # --- INICIO DE LA CORRECCIÓN (MÉTODO AÑADIDO) ---

    def get_by_dni(self, dni: str) -> Optional[Cliente]:
        """
        Busca un cliente por su DNI.
        """
        query = "SELECT ClienteID, Nombre, Apellido, DNI, Licencia, Telefono, Email, ISNULL(Direccion, ''), ISNULL(Distrito, '') FROM Clientes WHERE DNI = ?"
        params = (dni,)
        results = self.datasource.execute_query(query, params)
        if results:
            return self._mapear_a_cliente(results[0])
        return None


    def save(self, cliente: Cliente) -> bool:
        if cliente.id:
            # Actualizar (UPDATE)
            query = """
            UPDATE Clientes 
            SET Nombre=?, Apellido=?, DNI=?, Licencia=?, Telefono=?, Email=?, Direccion=?, Distrito=?
            WHERE ClienteID=?
            """
            params = (
                cliente.nombre, cliente.apellido, cliente.dni, cliente.licencia,
                cliente.telefono, cliente.email, cliente.direccion, cliente.distrito,
                cliente.id
            )
        else:
            # Insertar (INSERT)
            query = """
            INSERT INTO Clientes (Nombre, Apellido, DNI, Licencia, Telefono, Email, Direccion, Distrito)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (
                cliente.nombre, cliente.apellido, cliente.dni, cliente.licencia,
                cliente.telefono, cliente.email, cliente.direccion, cliente.distrito
            )
        
        return self.datasource.execute_non_query(query, params)

    
    def delete(self, id: int) -> bool:
        """
        Elimina un cliente por su ID.
        """
        query = "DELETE FROM Clientes WHERE ClienteID = ?"
        params = (id,)
        return self.datasource.execute_non_query(query, params)

    # --- FIN DE LA CORRECCIÓN ---

    def search(self, term: str) -> List[Cliente]:
        search_text = f"%{term.lower()}%"
        query = """
        SELECT ClienteID, Nombre, Apellido, DNI, Licencia, Telefono, Email, ISNULL(Direccion, ''), ISNULL(Distrito, '')
        FROM Clientes 
        WHERE LOWER(Nombre) LIKE ? OR LOWER(Apellido) LIKE ? OR DNI LIKE ? OR LOWER(ISNULL(Distrito, '')) LIKE ?
        ORDER BY Apellido, Nombre
        """
        params = (search_text, search_text, search_text, search_text)
        results = self.datasource.execute_query(query, params)
        return [self._mapear_a_cliente(row) for row in results]

