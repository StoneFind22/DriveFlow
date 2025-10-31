# src/domain/repositories/tipo_vehiculo_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.models.tipo_vehiculo import TipoVehiculo

class ITipoVehiculoRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[TipoVehiculo]: pass
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[TipoVehiculo]: pass

