# src/domain/models/estado_vehiculo.py
from dataclasses import dataclass

@dataclass
class EstadoVehiculo:
    """Modelo de Dominio para EstadoVehiculo."""
    id: int
    nombre_estado: str # <-- Nombre consistente

