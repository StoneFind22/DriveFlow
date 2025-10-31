# src/data/repositories/vehiculo_repository_impl.py
from typing import List, Optional, Dict
from src.domain.models.vehiculo import Vehiculo, TipoVehiculo, EstadoVehiculo
from src.domain.repositories.vehiculo_repository import IVehiculoRepository
from src.domain.repositories.tipo_vehiculo_repository import ITipoVehiculoRepository
from src.domain.repositories.estado_vehiculo_repository import IEstadoVehiculoRepository
from src.data.datasources.sql_server_datasource import SQLServerDataSource

class VehiculoRepositoryImpl(IVehiculoRepository):
    def __init__(self, datasource: SQLServerDataSource, tipo_repo: ITipoVehiculoRepository, estado_repo: IEstadoVehiculoRepository):
        self.datasource = datasource
        self.tipo_repo = tipo_repo
        self.estado_repo = estado_repo

    def _mapear_a_vehiculo(self, row: tuple, mapa_tipos: Dict[int, TipoVehiculo], mapa_estados: Dict[int, EstadoVehiculo]) -> Vehiculo:
        tipo_id, estado_id = row[5], row[6]
        
        tipo_obj = mapa_tipos.get(tipo_id)
        if not tipo_obj: tipo_obj = TipoVehiculo(id=tipo_id, nombre_tipo="Tipo Desconocido", garantia_base=0.0)
            
        estado_obj = mapa_estados.get(estado_id)
        if not estado_obj: estado_obj = EstadoVehiculo(id=estado_id, nombre_estado="Estado Desconocido")

        return Vehiculo(
            id=row[0],
            marca=row[1] or "",
            modelo=row[2] or "",
            anio=int(row[3]) if row[3] else 1900,
            placa=row[4] or "",
            tipo=tipo_obj,        # <-- Pasa el objeto
            estado=estado_obj,    # <-- Pasa el objeto
            precio_por_dia=float(row[7]) if row[7] else 0.0,
            kilometraje=int(row[8]) if row[8] else None,
            imagen_path=row[9] or None
        )

    def get_all(self, mapa_tipos: Dict[int, TipoVehiculo], mapa_estados: Dict[int, EstadoVehiculo]) -> List[Vehiculo]:
        query = "SELECT VehiculoID, Marca, Modelo, Anio, Placa, TipoID, EstadoID, PrecioPorDia, Kilometraje, ImagenPath FROM Vehiculos ORDER BY Marca, Modelo"
        results = self.datasource.execute_query(query)
        vehiculos = []
        if results:
            for row in results:
                try: vehiculos.append(self._mapear_a_vehiculo(row, mapa_tipos, mapa_estados))
                except Exception as e: print(f"Error al mapear vehículo: {row} - Error: {e}")
        return vehiculos

    def get_by_id(self, vehiculo_id: int, mapa_tipos: Dict[int, TipoVehiculo], mapa_estados: Dict[int, EstadoVehiculo]) -> Optional[Vehiculo]:
        # La consulta SQL debe ser genérica, el _mapear_a_vehiculo usa los índices
        query = "SELECT VehiculoID, Marca, Modelo, Anio, Placa, TipoID, EstadoID, PrecioPorDia, Kilometraje, ImagenPath FROM Vehiculos WHERE VehiculoID = ?"
        results = self.datasource.execute_query(query, (vehiculo_id,))
        if results:
            try: return self._mapear_a_vehiculo(results[0], mapa_tipos, mapa_estados)
            except Exception as e: print(f"Error al mapear vehículo ID {vehiculo_id}: {e}")
        return None

    def save(self, vehiculo: Vehiculo) -> bool:
        if vehiculo.id:
            query = "UPDATE Vehiculos SET Marca=?, Modelo=?, Anio=?, Placa=?, TipoID=?, EstadoID=?, PrecioPorDia=?, Kilometraje=?, ImagenPath=? WHERE VehiculoID=?"
            params = (vehiculo.marca, vehiculo.modelo, vehiculo.anio, vehiculo.placa, vehiculo.tipo.id, vehiculo.estado.id, vehiculo.precio_por_dia, vehiculo.kilometraje, vehiculo.imagen_path, vehiculo.id)
        else:
            query = "INSERT INTO Vehiculos (Marca, Modelo, Anio, Placa, TipoID, EstadoID, PrecioPorDia, Kilometraje, ImagenPath) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
            params = (vehiculo.marca, vehiculo.modelo, vehiculo.anio, vehiculo.placa, vehiculo.tipo.id, vehiculo.estado.id, vehiculo.precio_por_dia, vehiculo.kilometraje, vehiculo.imagen_path)
        return self.datasource.execute_non_query(query, params)

    def delete(self, vehiculo_id: int) -> bool:
        return self.datasource.execute_non_query("DELETE FROM Vehiculos WHERE VehiculoID = ?", (vehiculo_id,))

    def search_and_filter(self, term: str, estado_id: Optional[int], mapa_tipos: Dict[int, TipoVehiculo], mapa_estados: Dict[int, EstadoVehiculo]) -> List[Vehiculo]:
        base_query = "SELECT VehiculoID, Marca, Modelo, Anio, Placa, TipoID, EstadoID, PrecioPorDia, Kilometraje, ImagenPath FROM Vehiculos"
        conditions, params = [], []
        if term:
            term_like = f"%{term.lower()}%"
            conditions.append("(LOWER(Marca) LIKE ? OR LOWER(Modelo) LIKE ? OR LOWER(Placa) LIKE ?)")
            params.extend([term_like] * 3)
        if estado_id is not None:
            conditions.append("EstadoID = ?")
            params.append(estado_id)
        
        query = base_query + (" WHERE " + " AND ".join(conditions) if conditions else "") + " ORDER BY Marca, Modelo"
        results = self.datasource.execute_query(query, tuple(params)) # Asegurarse que params sea tupla
        vehiculos = []
        if results:
            for row in results:
                try: vehiculos.append(self._mapear_a_vehiculo(row, mapa_tipos, mapa_estados))
                except Exception as e: print(f"Error mapeando vehículo (búsqueda): {row} - Error: {e}")
        return vehiculos

