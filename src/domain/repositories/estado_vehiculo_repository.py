# src/domain/repositories/estado_vehiculo_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.models.estado_vehiculo import EstadoVehiculo

class IEstadoVehiculoRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[EstadoVehiculo]: pass
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[EstadoVehiculo]: pass

