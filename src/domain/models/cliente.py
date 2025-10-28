# src/domain/models/cliente.py
#
# Define la entidad de negocio 'Cliente'.
# Es una estructura de datos pura (dataclass) que representa
# un cliente en nuestro dominio, independiente de la base de datos o la UI.

from dataclasses import dataclass, field
from typing import Optional
import re

@dataclass
class Cliente:
    """
    Modelo de Dominio para la entidad Cliente.
    
    Esta clase representa un Cliente válido dentro de nuestro sistema.
    Utiliza __post_init__ para realizar validaciones y normalización
    de datos en el momento de la creación.
    """
    nombre: str
    apellido: str
    dni: str
    licencia: str
    id: Optional[int] = None  # El ID es opcional, puede ser None al crear
    telefono: Optional[str] = None
    email: Optional[str] = None
    direccion: Optional[str] = None
    distrito: Optional[str] = None

    def __post_init__(self):
        """
        Se ejecuta después de que __init__ haya inicializado los campos.
        Usado para validación y normalización.
        """
        # Validación de campos obligatorios
        if not self.nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")
        if not self.apellido.strip():
            raise ValueError("El apellido no puede estar vacío.")
        if not self.dni.strip():
            raise ValueError("El DNI no puede estar vacío.")
        if not self.licencia.strip():
            raise ValueError("La licencia no puede estar vacía.")

        # Validación de formato (ejemplo para email)
        if self.email:
            self.email = self.email.strip()
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.email):
                raise ValueError(f"El email '{self.email}' no tiene un formato válido.")
        
        # Normalización de datos (ejemplo: capitalizar nombres)
        self.nombre = self.nombre.strip().title()
        self.apellido = self.apellido.strip().title()
        self.dni = self.dni.strip()
        self.licencia = self.licencia.strip()
        
        if self.distrito:
            self.distrito = self.distrito.strip().title()

    @property
    def nombre_completo(self) -> str:
        """Retorna el nombre completo del cliente."""
        return f"{self.nombre} {self.apellido}"
