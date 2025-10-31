# src/domain/repositories/vehiculo_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from src.domain.models.vehiculo import Vehiculo, TipoVehiculo, EstadoVehiculo

class IVehiculoRepository(ABC):
    @abstractmethod
    def get_all(self, mapa_tipos: Dict[int, TipoVehiculo], mapa_estados: Dict[int, EstadoVehiculo]) -> List[Vehiculo]: pass
    
    @abstractmethod
    def get_by_id(self, vehiculo_id: int, mapa_tipos: Dict[int, TipoVehiculo], mapa_estados: Dict[int, EstadoVehiculo]) -> Optional[Vehiculo]: pass
    
    @abstractmethod
    def save(self, vehiculo: Vehiculo) -> bool: pass
    
    @abstractmethod
    def delete(self, vehiculo_id: int) -> bool: pass
    
    @abstractmethod
    def search_and_filter(self, term: str, estado_id: Optional[int], mapa_tipos: Dict[int, TipoVehiculo], mapa_estados: Dict[int, EstadoVehiculo]) -> List[Vehiculo]: pass

