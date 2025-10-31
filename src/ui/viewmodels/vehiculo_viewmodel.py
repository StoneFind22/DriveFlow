# src/ui/viewmodels/vehiculo_viewmodel.py
import tkinter as tk
from tkinter import messagebox
from typing import List, Optional, Callable, Tuple, Dict, Any
from src.domain.models.vehiculo import Vehiculo, TipoVehiculo, EstadoVehiculo
from src.domain.usecases.vehiculo_usecases import (
    ObtenerVehiculosUseCase, ObtenerTiposVehiculoUseCase, ObtenerEstadosVehiculoUseCase,
    GuardarVehiculoUseCase, EliminarVehiculoUseCase, ValidarVehiculoUseCase,
    BuscarYFiltrarVehiculosUseCase
)

class VehiculoViewModel:
    def __init__(
        self,
        obtener_vehiculos_usecase: ObtenerVehiculosUseCase,
        obtener_tipos_usecase: ObtenerTiposVehiculoUseCase,
        obtener_estados_usecase: ObtenerEstadosVehiculoUseCase,
        guardar_vehiculo_usecase: GuardarVehiculoUseCase,
        eliminar_vehiculo_usecase: EliminarVehiculoUseCase,
        validar_vehiculo_usecase: ValidarVehiculoUseCase,
        buscar_y_filtrar_usecase: BuscarYFiltrarVehiculosUseCase
    ):
        self.obtener_vehiculos_usecase = obtener_vehiculos_usecase
        self.obtener_tipos_usecase = obtener_tipos_usecase
        self.obtener_estados_usecase = obtener_estados_usecase
        self.guardar_vehiculo_usecase = guardar_vehiculo_usecase
        self.eliminar_vehiculo_usecase = eliminar_vehiculo_usecase
        self.validar_vehiculo_usecase = validar_vehiculo_usecase
        self.buscar_y_filtrar_usecase = buscar_y_filtrar_usecase

        # Estado
        self.vehiculos: List[Vehiculo] = []
        self.tipos: List[TipoVehiculo] = []
        self.estados: List[EstadoVehiculo] = []
        self.mapa_tipos: Dict[int, TipoVehiculo] = {}
        self.mapa_estados: Dict[int, EstadoVehiculo] = {}
        self.vehiculo_seleccionado: Optional[Vehiculo] = None
        self.filter_term: str = ""
        self.filter_estado_nombre: str = "Todos"
        self._observers: List[Callable[[], None]] = []

    def bind_to_updates(self, callback: Callable[[], None]):
        if callback not in self._observers: self._observers.append(callback)

    def remove_observer(self, callback: Callable[[], None]):
        if callback in self._observers: self._observers.remove(callback)

    def _notify_observers(self):
        print("ViewModel: Notificando observadores...")
        for callback in self._observers[:]:
            try: callback()
            except tk.TclError as e:
                print(f"Error (tk.TclError) al notificar: {e}. Eliminando observador.")
                if callback in self._observers: self._observers.remove(callback)
            except Exception as e:
                print(f"Error (inesperado) al notificar: {e}")

    def cargar_datos_iniciales(self):
        print("ViewModel: Iniciando carga de datos iniciales...")
        error_parcial = False
        try:
            self.tipos = self.obtener_tipos_usecase.execute()
            self.mapa_tipos = {tipo.id: tipo for tipo in self.tipos}
            print(f"ViewModel: {len(self.tipos)} tipos cargados.")
        except Exception as e:
            print(f"Error crítico al cargar tipos: {e}"); error_parcial = True
            self.tipos, self.mapa_tipos = [], {}

        try:
            self.estados = self.obtener_estados_usecase.execute()
            self.mapa_estados = {estado.id: estado for estado in self.estados}
            print(f"ViewModel: {len(self.estados)} estados cargados.")
        except Exception as e:
            print(f"Error crítico al cargar estados: {e}"); error_parcial = True
            self.estados, self.mapa_estados = [], {}

        try:
            # CORRECCIÓN: Los mapas deben existir antes de llamar a esto
            if not error_parcial:
                self.vehiculos = self.obtener_vehiculos_usecase.execute(self.mapa_tipos, self.mapa_estados)
                print(f"ViewModel: {len(self.vehiculos)} vehículos cargados.")
            else:
                self.vehiculos = []
        except Exception as e:
            print(f"Error crítico al cargar vehículos: {e}"); error_parcial = True
            self.vehiculos = []

        print("ViewModel: Carga inicial completada. Notificando...")
        self._notify_observers()
        if error_parcial: messagebox.showwarning("Error de Carga", "No se pudieron cargar todos los datos.")

    def buscar_y_filtrar_vehiculos(self, termino: str, estado_nombre: str):
        self.filter_term = termino.strip()
        self.filter_estado_nombre = estado_nombre
        print(f"ViewModel: Buscando/Filtrando - Termino: '{self.filter_term}', Estado: '{estado_nombre}'")

        estado_id: Optional[int] = None
        if estado_nombre != "Todos":
            estado_obj = next((e for e in self.estados if e.nombre_estado == estado_nombre), None)
            if estado_obj: estado_id = estado_obj.id
            else: self.filter_estado_nombre = "Todos"

        try:
            self.vehiculos = self.buscar_y_filtrar_usecase.execute(self.filter_term, estado_id, self.mapa_tipos, self.mapa_estados)
        except Exception as e:
            print(f"Error al buscar/filtrar: {e}"); self.vehiculos = []
        self._notify_observers()

    def seleccionar_vehiculo(self, vehiculo: Optional[Vehiculo]):
        # vvv CORRECCIÓN AQUÍ vvv
        # Si la selección es la misma que ya tenemos, no hacemos nada.
        # Esto rompe el bucle infinito de notificación (View -> VM -> View).
        if self.vehiculo_seleccionado == vehiculo:
            print(f"ViewModel: Selección redundante ignorada ({vehiculo.placa if vehiculo else 'None'}).")
            return
        # ^^^ FIN DE LA CORRECCIÓN ^^^
        
        self.vehiculo_seleccionado = vehiculo
        print(f"ViewModel: Vehículo seleccionado: {vehiculo.placa if vehiculo else 'None'}")
        self._notify_observers()

    def guardar_vehiculo(self, id: Optional[int], data_dict: Dict[str, Any]) -> Tuple[bool, str]:
        is_valid, error_message = self.validar_vehiculo_usecase.execute(data_dict)
        if not is_valid: return False, error_message

        tipo_obj = next((t for t in self.tipos if t.nombre_tipo == data_dict.get('tipo_nombre')), None)
        estado_obj = next((e for e in self.estados if e.nombre_estado == data_dict.get('estado_nombre')), None)
        if not tipo_obj or not estado_obj: return False, "Tipo o Estado inválido."

        try:
            vehiculo = Vehiculo(
                id=id,
                marca=data_dict['marca'], modelo=data_dict['modelo'],
                anio=int(data_dict['anio']), placa=data_dict['placa'],
                tipo=tipo_obj, estado=estado_obj,
                precio_por_dia=float(data_dict['precio_por_dia']),
                kilometraje=int(km_str) if (km_str := data_dict.get('kilometraje', '').strip()) else None,
                imagen_path=data_dict.get('imagen_path') or None
            )
            success = self.guardar_vehiculo_usecase.execute(vehiculo)
            if success:
                self.cargar_datos_iniciales(); return True, "Vehículo guardado."
            return False, "Error al guardar en BD."
        except ValueError as e: return False, f"Datos inválidos: {e}"
        except Exception as e: print(f"Error inesperado al guardar: {e}"); return False, f"Error: {e}"

    def eliminar_vehiculo(self, id: Optional[int]) -> bool:
        if id is None: return False
        try:
            success = self.eliminar_vehiculo_usecase.execute(id)
            if success:
                if self.vehiculo_seleccionado and self.vehiculo_seleccionado.id == id:
                    self.vehiculo_seleccionado = None
                self.cargar_datos_iniciales()
            return success
        except Exception as e:
            print(f"Error al eliminar: {e}"); return False

