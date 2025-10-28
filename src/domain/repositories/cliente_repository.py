# src/domain/repositories/cliente_repository.py
#
# Define la interfaz (el "contrato") para el repositorio de clientes.
# La Capa de Dominio depende de esta abstracción, no de la
# implementación concreta de la base de datos.

from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.models.cliente import Cliente

class IClienteRepository(ABC):
    """
    Interfaz abstracta para el Repositorio de Clientes.
    Define las operaciones de datos (CRUD) que se pueden realizar
    sobre la entidad Cliente.
    """

    @abstractmethod
    def get_all(self) -> List[Cliente]:
        """
        Recupera todos los clientes.
        Retorna:
            List[Cliente]: Una lista de objetos Cliente.
        """
        pass

    @abstractmethod
    def get_by_id(self, cliente_id: int) -> Optional[Cliente]:
        """
        Recupera un cliente por su ID.
        Args:
            cliente_id (int): El ID del cliente a buscar.
        Retorna:
            Optional[Cliente]: El objeto Cliente si se encuentra, None si no.
        """
        pass

    @abstractmethod
    def get_by_dni(self, dni: str) -> Optional[Cliente]:
        """
        Recupera un cliente por su DNI.
        Args:
            dni (str): El DNI del cliente a buscar.
        Retorna:
            Optional[Cliente]: El objeto Cliente si se encuentra, None si no.
        """
        pass
        
    @abstractmethod
    def search(self, term: str) -> List[Cliente]:
        """
        Busca clientes cuyo nombre, apellido o DNI coincida con el término.
        Args:
            term (str): El término de búsqueda.
        Retorna:
            List[Cliente]: Una lista de clientes que coinciden.
        """
        pass

    @abstractmethod
    def save(self, cliente: Cliente) -> Cliente:
        """
        Guarda (inserta o actualiza) un cliente.
        Si el cliente.id es None, inserta un nuevo cliente.
        Si el cliente.id tiene valor, actualiza el cliente existente.
        Args:
            cliente (Cliente): El objeto Cliente a guardar.
        Retorna:
            Cliente: El objeto Cliente guardado (puede incluir el nuevo ID).
        """
        pass

    @abstractmethod
    def delete(self, cliente_id: int) -> bool:
        """
        Elimina un cliente por su ID.
        Args:
            cliente_id (int): El ID del cliente a eliminar.
        Retorna:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """
        pass
