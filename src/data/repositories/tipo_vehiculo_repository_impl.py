# src/data/repositories/tipo_vehiculo_repository_impl.py
from typing import List, Optional
from src.domain.models.tipo_vehiculo import TipoVehiculo
from src.domain.repositories.tipo_vehiculo_repository import ITipoVehiculoRepository
from src.data.datasources.sql_server_datasource import SQLServerDataSource

class TipoVehiculoRepositoryImpl(ITipoVehiculoRepository):
    def __init__(self, datasource: SQLServerDataSource):
        self.datasource = datasource

    def _mapear_a_tipo(self, row: tuple) -> TipoVehiculo:
        try:
            garantia = float(row[2]) if row[2] is not None else 0.0
        except (ValueError, TypeError):
            garantia = 0.0
        
        return TipoVehiculo(
            id=row[0],
            nombre_tipo=row[1] or "Desconocido", # <-- Keyword 'nombre_tipo'
            garantia_base=garantia
        )

    def get_all(self) -> List[TipoVehiculo]:
        query = "SELECT TipoID, NombreTipo, GarantiaBase FROM TiposVehiculo ORDER BY NombreTipo"
        results = self.datasource.execute_query(query)
        tipos = []
        if results:
            for row in results:
                try: tipos.append(self._mapear_a_tipo(row))
                except Exception as e: print(f"Error al mapear TipoVehiculo (fila: {row}): {e}")
        return tipos

    def get_by_id(self, id: int) -> Optional[TipoVehiculo]:
        query = "SELECT TipoID, NombreTipo, GarantiaBase FROM TiposVehiculo WHERE TipoID = ?"
        results = self.datasource.execute_query(query, (id,))
        if results:
            try: return self._mapear_a_tipo(results[0])
            except Exception as e: print(f"Error al mapear TipoVehiculo ID {id}: {e}")
        return None

