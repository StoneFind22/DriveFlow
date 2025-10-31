# src/domain/models/vehiculo.py
from dataclasses import dataclass, field
from typing import Optional
from .tipo_vehiculo import TipoVehiculo
from .estado_vehiculo import EstadoVehiculo

@dataclass
class Vehiculo:
    """Modelo de Dominio para Vehiculo."""
    id: Optional[int]
    marca: str
    modelo: str
    anio: int
    placa: str
    tipo: TipoVehiculo      # <-- Acepta objeto
    estado: EstadoVehiculo  # <-- Acepta objeto
    precio_por_dia: float
    kilometraje: Optional[int] = field(default=None)
    imagen_path: Optional[str] = field(default=None)

    def __post_init__(self):
        # Normalización
        self.marca = self.marca.strip().title()
        self.modelo = self.modelo.strip()
        self.placa = self.placa.strip().upper()
        
        # Validación
        if not self.marca or not self.modelo or not self.placa:
            raise ValueError("Marca, Modelo y Placa son obligatorios.")
        if not isinstance(self.anio, int) or self.anio <= 1900:
            raise ValueError("Año inválido.")
        if not isinstance(self.precio_por_dia, (int, float)) or self.precio_por_dia <= 0:
            raise ValueError("Precio por día inválido.")
        if self.kilometraje is not None and (not isinstance(self.kilometraje, int) or self.kilometraje < 0):
             raise ValueError("Kilometraje inválido.")

