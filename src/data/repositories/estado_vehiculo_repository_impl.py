# src/data/repositories/estado_vehiculo_repository_impl.py
from typing import List, Optional
from src.domain.models.estado_vehiculo import EstadoVehiculo
from src.domain.repositories.estado_vehiculo_repository import IEstadoVehiculoRepository
from src.data.datasources.sql_server_datasource import SQLServerDataSource

class EstadoVehiculoRepositoryImpl(IEstadoVehiculoRepository):
    def __init__(self, datasource: SQLServerDataSource):
        self.datasource = datasource

    def _mapear_a_estado(self, row: tuple) -> EstadoVehiculo:
        return EstadoVehiculo(
            id=row[0],
            nombre_estado=row[1] or "Desconocido" # <-- Keyword 'nombre_estado'
        )

    def get_all(self) -> List[EstadoVehiculo]:
        query = "SELECT EstadoID, NombreEstado FROM EstadosVehiculo ORDER BY NombreEstado"
        results = self.datasource.execute_query(query)
        estados = []
        if results:
            for row in results:
                try: estados.append(self._mapear_a_estado(row))
                except Exception as e: print(f"Error al mapear EstadoVehiculo (fila: {row}): {e}")
        return estados

    def get_by_id(self, id: int) -> Optional[EstadoVehiculo]:
        query = "SELECT EstadoID, NombreEstado FROM EstadosVehiculo WHERE EstadoID = ?"
        results = self.datasource.execute_query(query, (id,))
        if results:
            try: return self._mapear_a_estado(results[0])
            except Exception as e: print(f"Error al mapear EstadoVehiculo ID {id}: {e}")
        return None

