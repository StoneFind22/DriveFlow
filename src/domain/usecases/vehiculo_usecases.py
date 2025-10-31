# src/domain/usecases/vehiculo_usecases.py
from typing import List, Optional, Tuple, Dict, Any
from src.domain.models.vehiculo import Vehiculo, TipoVehiculo, EstadoVehiculo
from src.domain.repositories.vehiculo_repository import IVehiculoRepository
from src.domain.repositories.tipo_vehiculo_repository import ITipoVehiculoRepository
from src.domain.repositories.estado_vehiculo_repository import IEstadoVehiculoRepository

# --- Casos de Uso de Carga ---
class ObtenerVehiculosUseCase:
    def __init__(self, repository: IVehiculoRepository): self.repository = repository
    def execute(self, mapa_tipos: Dict[int, TipoVehiculo], mapa_estados: Dict[int, EstadoVehiculo]) -> List[Vehiculo]:
        return self.repository.get_all(mapa_tipos, mapa_estados)

class ObtenerTiposVehiculoUseCase:
    def __init__(self, repository: ITipoVehiculoRepository): self.repository = repository
    def execute(self) -> List[TipoVehiculo]: return self.repository.get_all()

class ObtenerEstadosVehiculoUseCase:
    def __init__(self, repository: IEstadoVehiculoRepository): self.repository = repository
    def execute(self) -> List[EstadoVehiculo]: return self.repository.get_all()

# --- Casos de Uso de Acción ---
class GuardarVehiculoUseCase:
    def __init__(self, repository: IVehiculoRepository): self.repository = repository
    def execute(self, vehiculo: Vehiculo) -> bool: return self.repository.save(vehiculo)

class EliminarVehiculoUseCase:
    def __init__(self, repository: IVehiculoRepository): self.repository = repository
    def execute(self, id: int) -> bool: return self.repository.delete(id)

# --- Caso de Uso de Búsqueda ---
class BuscarYFiltrarVehiculosUseCase:
    def __init__(self, repository: IVehiculoRepository): self.repository = repository
    def execute(self, term: str, estado_id: Optional[int], mapa_tipos: Dict[int, TipoVehiculo], mapa_estados: Dict[int, EstadoVehiculo]) -> List[Vehiculo]:
        return self.repository.search_and_filter(term, estado_id, mapa_tipos, mapa_estados)

# --- Caso de Uso de Validación ---
class ValidarVehiculoUseCase:
    """Valida los datos crudos que vienen de la Vista."""
    def execute(self, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        # Validar campos obligatorios de string
        obligatorios_str = ['marca', 'modelo', 'placa', 'tipo_nombre', 'estado_nombre', 'precio_por_dia', 'anio']
        for campo in obligatorios_str:
            if not data.get(campo, '').strip():
                return False, f"El campo '{campo.replace('_', ' ').title()}' es obligatorio."
        
        # Validar números
        try:
            anio = int(data['anio'])
            if anio < 1900 or anio > 2050: raise ValueError()
        except (ValueError, TypeError):
            return False, "El Año debe ser un número válido (ej. 2023)."
        
        try:
            precio = float(data['precio_por_dia'])
            if precio <= 0: raise ValueError()
        except (ValueError, TypeError):
            return False, "El Precio/Día debe ser un número positivo."

        # Validar opcional (Kilometraje)
        km_str = data.get('kilometraje', '').strip()
        if km_str:
            try:
                km = int(km_str)
                if km < 0: raise ValueError()
            except (ValueError, TypeError):
                return False, "El Kilometraje debe ser un número entero positivo."
                
        return True, None

