# src/domain/usecases/cliente_usecases.py
#
# Capa de Dominio (Casos de Uso).
# Contiene la lógica de negocio pura.

from typing import List, Optional, Tuple, Dict, Any
from src.domain.models.cliente import Cliente
from src.domain.repositories.cliente_repository import IClienteRepository
import re # Para validación de email

class ObtenerClientesUseCase:
    def __init__(self, repository: IClienteRepository):
        self.repository = repository
    
    def execute(self) -> List[Cliente]:
        return self.repository.get_all()

class GuardarClienteUseCase:
    def __init__(self, repository: IClienteRepository):
        self.repository = repository
        
    def execute(self, cliente: Cliente) -> bool:
        return self.repository.save(cliente)

class EliminarClienteUseCase:
    def __init__(self, repository: IClienteRepository):
        self.repository = repository
        
    def execute(self, id: int) -> bool:
        return self.repository.delete(id)

class ValidarClienteUseCase:
    """
    Valida los datos de un cliente antes de guardarlos.
    """
    def execute(self, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        nombre = data.get('nombre', '').strip()
        apellido = data.get('apellido', '').strip()
        dni = data.get('dni', '').strip()
        licencia = data.get('licencia', '').strip()
        email = data.get('email', '').strip()

        if not all([nombre, apellido, dni, licencia]):
            return False, "Nombre, Apellido, DNI y Licencia son obligatorios."
        
        if len(dni) != 8 or not dni.isdigit():
            return False, "El DNI debe tener 8 dígitos numéricos."

        if email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return False, "El formato del email no es válido."
            
        return True, None

class BuscarClientesUseCase:
    def __init__(self, repository: IClienteRepository):
        self.repository = repository
    
    def execute(self, term: str) -> List[Cliente]:
        return self.repository.search(term)

