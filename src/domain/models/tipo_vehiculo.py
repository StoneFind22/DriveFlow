# src/domain/models/tipo_vehiculo.py
from dataclasses import dataclass

@dataclass
class TipoVehiculo:
    """Modelo de Dominio para TipoVehiculo."""
    id: int
    nombre_tipo: str # <-- Nombre consistente
    garantia_base: float

