# src/ui/viewmodels/cliente_viewmodel.py
#
# Capa de IU (ViewModel).
# Intermediario entre la Vista y los Casos de Uso.

import tkinter as tk  # Importado solo para tk.TclError
from typing import List, Optional, Callable, Tuple
from src.domain.models.cliente import Cliente
from src.domain.usecases.cliente_usecases import (
    ObtenerClientesUseCase,
    GuardarClienteUseCase,
    EliminarClienteUseCase,
    ValidarClienteUseCase,
    BuscarClientesUseCase
)


class ClienteViewModel:
    def __init__(
        self,
        obtener_clientes_usecase: ObtenerClientesUseCase,
        guardar_cliente_usecase: GuardarClienteUseCase,
        eliminar_cliente_usecase: EliminarClienteUseCase,
        validar_cliente_usecase: ValidarClienteUseCase,
        buscar_clientes_usecase: BuscarClientesUseCase
    ):
        self.obtener_clientes_usecase = obtener_clientes_usecase
        self.guardar_cliente_usecase = guardar_cliente_usecase
        self.eliminar_cliente_usecase = eliminar_cliente_usecase
        self.validar_cliente_usecase = validar_cliente_usecase
        self.buscar_clientes_usecase = buscar_clientes_usecase
        
        # Estado de la UI
        self.clientes: List[Cliente] = []
        self.cliente_seleccionado: Optional[Cliente] = None
        
        # Lista de observadores (callbacks de la vista)
        self._observers: List[Callable[[], None]] = []

    def bind_to_updates(self, callback: Callable[[], None]) -> None:
        """
        La Vista se suscribe a las actualizaciones.
        """
        if callback not in self._observers:
            self._observers.append(callback)
    
    def remove_observer(self, callback: Callable[[], None]) -> None:
        """
        La Vista se da de baja de las actualizaciones.
        """
        if callback in self._observers:
            self._observers.remove(callback)

    def _notify_observers(self) -> None:
        """
        Notifica a todas las vistas suscritas que el estado ha cambiado.
        """
        # Iterar sobre una copia de la lista por si un observador se elimina a sí mismo
        for callback in self._observers[:]:
            try:
                callback()
            except tk.TclError as e:
                # Si el widget está destruido, eliminarlo de la lista
                print(f"Error al notificar observador (probablemente ventana cerrada): {e}")
                if callback in self._observers:
                    self._observers.remove(callback)

    def cargar_clientes(self) -> None:
        """
        Carga la lista de clientes desde el repositorio.
        """
        try:
            self.clientes = self.obtener_clientes_usecase.execute()
            self._notify_observers()
        except Exception as e:
            # Manejo de error (ej. loggear, mostrar mensaje)
            print(f"Error al cargar clientes: {e}")

    def buscar_clientes(self, termino: str) -> None:
        """
        Busca clientes según un término de búsqueda.
        """
        try:
            self.clientes = self.buscar_clientes_usecase.execute(termino)
            self._notify_observers()
        except Exception as e:
            print(f"Error al buscar clientes: {e}")

    def seleccionar_cliente(self, cliente: Optional[Cliente]) -> None:
        """
        Establece el cliente seleccionado (para el formulario).
        """
        self.cliente_seleccionado = cliente
        self._notify_observers()

    def guardar_cliente(
        self,
        id: Optional[int],
        nombre: str,
        apellido: str,
        dni: str,
        licencia: str,
        telefono: str,
        email: str,
        direccion: str,
        distrito: str
    ) -> Tuple[bool, str]:
        """
        Guarda (crea o actualiza) un cliente.
        Retorna: (éxito: bool, mensaje: str)
        """
        cliente_data = {
            'id': id,
            'nombre': nombre,
            'apellido': apellido,
            'dni': dni,
            'licencia': licencia,
            'telefono': telefono,
            'email': email,
            'direccion': direccion,
            'distrito': distrito
        }
        
        # 1. Validación
        is_valid, error_message = self.validar_cliente_usecase.execute(cliente_data)
        if not is_valid:
            return False, error_message  # Devuelve False y el mensaje de error

        # 2. Creación del modelo
        cliente = Cliente(**cliente_data)
        
        # 3. Guardado
        try:
            success = self.guardar_cliente_usecase.execute(cliente)
            if success:
                self.cargar_clientes()
            return success, "Cliente guardado exitosamente."
        except Exception as e:
            return False, f"Error al guardar: {e}"

    def eliminar_cliente(self, id: Optional[int]) -> bool:
        """
        Elimina un cliente.
        """
        if id is None:
            return False
            
        try:
            success = self.eliminar_cliente_usecase.execute(id)
            if success:
                self.cargar_clientes()  # Recargar la lista
                if self.cliente_seleccionado and self.cliente_seleccionado.id == id:
                    self.cliente_seleccionado = None
            self._notify_observers()
            return success
        except Exception as e:
            print(f"Error al eliminar cliente: {e}")
            return False