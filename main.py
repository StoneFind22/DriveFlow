# main.py

import tkinter as tk
from tkinter import ttk, messagebox
import os
from functools import partial
from dotenv import load_dotenv
from typing import Optional, Dict, Any, Tuple # <-- Imports de typing añadidos

# --- Cargar Variables de Entorno ---
load_dotenv()

# --- Importaciones de la Arquitectura ---

# Capa de Datos
from src.data.datasources.sql_server_datasource import SQLServerDataSource
from src.data.repositories.cliente_repository_impl import ClienteRepositoryImpl
# Importaciones de Vehículo
from src.data.repositories.tipo_vehiculo_repository_impl import TipoVehiculoRepositoryImpl
from src.data.repositories.estado_vehiculo_repository_impl import EstadoVehiculoRepositoryImpl
from src.data.repositories.vehiculo_repository_impl import VehiculoRepositoryImpl

# Capa de Dominio (Casos de Uso)
from src.domain.usecases.cliente_usecases import (
    ObtenerClientesUseCase, GuardarClienteUseCase, EliminarClienteUseCase,
    ValidarClienteUseCase, BuscarClientesUseCase
)
# Importaciones de Vehículo
from src.domain.usecases.vehiculo_usecases import (
    ObtenerVehiculosUseCase, ObtenerTiposVehiculoUseCase, ObtenerEstadosVehiculoUseCase,
    GuardarVehiculoUseCase, EliminarVehiculoUseCase, ValidarVehiculoUseCase,
    BuscarYFiltrarVehiculosUseCase
)

# Capa de IU
from src.ui.viewmodels.cliente_viewmodel import ClienteViewModel
from src.ui.viewmodels.vehiculo_viewmodel import VehiculoViewModel
from src.ui.views.cliente_view import ClienteView # <-- Importar la Vista refactorizada
from src.ui.views.vehiculo_view import VehiculoView
from src.ui.theme import setup_theme, PALETTE

# --- Ensamblador de Dependencias (DI) ---

def setup_dependencies() -> Optional[Dict[str, Any]]:
    """
    Inicializa y conecta todas las dependencias de la aplicación.
    """
    try:
        # 1. Leer Configuración
        server = os.environ.get('DB_SERVER', 'localhost')
        database = os.environ.get('DB_NAME', 'AlquilerAutos')
        username = os.environ.get('DB_USERNAME')
        password = os.environ.get('DB_PASSWORD')
        
        if not server or not database:
            raise ValueError("Las variables de entorno DB_SERVER y DB_NAME deben estar definidas en .env")

        # 2. Inicializar DataSource (Única)
        datasource = SQLServerDataSource.get_instance(
            server=server, database=database,
            username=username, password=password
        )
        
        # 3. Inicializar Repositorios
        cliente_repo = ClienteRepositoryImpl(datasource)
        tipo_repo = TipoVehiculoRepositoryImpl(datasource)
        estado_repo = EstadoVehiculoRepositoryImpl(datasource)
        vehiculo_repo = VehiculoRepositoryImpl(datasource, tipo_repo, estado_repo)
        
        # 4. Inicializar ViewModel de Cliente
        cliente_viewmodel = ClienteViewModel(
            obtener_clientes_usecase=ObtenerClientesUseCase(cliente_repo),
            guardar_cliente_usecase=GuardarClienteUseCase(cliente_repo),
            eliminar_cliente_usecase=EliminarClienteUseCase(cliente_repo),
            validar_cliente_usecase=ValidarClienteUseCase(),
            buscar_clientes_usecase=BuscarClientesUseCase(cliente_repo)
        )
        
        # 5. Inicializar ViewModel de Vehículo
        vehiculo_viewmodel = VehiculoViewModel(
            obtener_vehiculos_usecase=ObtenerVehiculosUseCase(vehiculo_repo),
            obtener_tipos_usecase=ObtenerTiposVehiculoUseCase(tipo_repo),
            obtener_estados_usecase=ObtenerEstadosVehiculoUseCase(estado_repo),
            guardar_vehiculo_usecase=GuardarVehiculoUseCase(vehiculo_repo),
            eliminar_vehiculo_usecase=EliminarVehiculoUseCase(vehiculo_repo),
            validar_vehiculo_usecase=ValidarVehiculoUseCase(),
            buscar_y_filtrar_usecase=BuscarYFiltrarVehiculosUseCase(vehiculo_repo)
        )
        
        # 6. Retornar todas las dependencias en un diccionario
        return {
            "datasource": datasource,
            "viewmodels": {
                "cliente": cliente_viewmodel,
                "vehiculo": vehiculo_viewmodel
            }
        }

    except (ValueError, Exception) as e:
        messagebox.showerror(
            "Error Crítico de Inicio",
            f"No se pudo iniciar la aplicación:\n{e}\n\nRevise su archivo .env y la conexión a la base de datos."
        )
        return None

# --- Clase Principal de la Aplicación (Vista Principal) ---

class MainApplication(ttk.Frame):
    def __init__(self, master, viewmodels: Dict[str, Any], datasource: SQLServerDataSource):
        
        super().__init__(master, style="TFrame")
        self.master = master
        self.master.title("DriveFlow - Sistema de Gestión de Alquiler")
        self.master.geometry("900x600")
        
        self.viewmodels = viewmodels
        self.datasource = datasource
        self.open_windows = {} # Diccionario para rastrear ventanas abiertas
        
        self.dashboard_modules = [
            {
                "title": "Gestionar Clientes",
                "command": lambda: self._open_toplevel_window(
                    ViewClass=ClienteView,
                    viewmodel=self.viewmodels["cliente"],
                    key="cliente",
                    title="Gestión de Clientes",
                    geometry="900x600"
                )
            },
            {
                "title": "Gestionar Vehículos",
                "command": lambda: self._open_toplevel_window(
                    ViewClass=VehiculoView,
                    viewmodel=self.viewmodels["vehiculo"],
                    key="vehiculo",
                    title="Gestión de Vehículos",
                    geometry="1100x700"
                )
            },
            { "title": "Gestionar Reservas", "command": partial(self.open_dummy, "Reservas") },
            { "title": "Gestionar Contratos", "command": partial(self.open_dummy, "Contratos") },
            { "title": "Gestionar Entregas", "command": partial(self.open_dummy, "Entregas") },
            { "title": "Gestionar Devoluciones", "command": partial(self.open_dummy, "Devoluciones") }
        ]
        
        self._create_widgets()
        self.master.protocol("WM_DELETE_WINDOW", self.on_close_app)

    def on_close_app(self):
        """Maneja el cierre de la ventana principal."""
        print("Cerrando aplicación...")
        try:
            if self.datasource:
                self.datasource.close()
                print("Conexión a base de datos cerrada.")
        except Exception as e:
            print(f"Error al cerrar datasource: {e}")
        finally:
            self.master.quit()
            self.master.destroy()

    def _create_widgets(self):
        self.pack(fill="both", expand=True)
        
        title_frame = ttk.Frame(self, style="TFrame")
        title_frame.pack(pady=(20, 30))
        
        try:
            ttk.Label(title_frame, text="Dashboard Principal", style="Heading.TLabel").pack()
        except tk.TclError:
            print("Advertencia: Estilo 'Heading.TLabel' no encontrado. Usando estilo por defecto.")
            ttk.Label(title_frame, text="Dashboard Principal", font=("Arial", 24, "bold"), foreground=PALETTE["primary"]).pack()
        
        buttons_frame = ttk.Frame(self, style="TFrame")
        buttons_frame.pack(pady=20, padx=20, fill="both", expand=True)
        buttons_frame.columnconfigure((0, 1, 2), weight=1)

        for i, module in enumerate(self.dashboard_modules):
            row, col = divmod(i, 3)
            btn = ttk.Button(buttons_frame, text=module["title"], command=module["command"])
            btn.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
            buttons_frame.rowconfigure(row, weight=1)
    
    def _open_toplevel_window(self, ViewClass, viewmodel, key: str, title: str, geometry: str):
        """
        Función genérica y robusta para abrir ventanas Toplevel modulares.
        ASUNCIÓN: ViewClass (ClienteView, VehiculoView) hereda de ttk.Frame.
        """
        try:
            # 1. Comprobar si la ventana ya existe
            if key in self.open_windows:
                window = self.open_windows[key]
                if window and window.winfo_exists():
                    window.lift() # Traer al frente
                    print(f"Ventana '{title}' ya existe. Trayendo al frente.")
                    return
                else:
                    # La referencia es inválida (ventana cerrada), la eliminamos
                    del self.open_windows[key]
                    
            # 2. Crear la ventana (Toplevel)
            window = tk.Toplevel(self.master)
            window.title(title)
            window.geometry(geometry)
            window.configure(bg=PALETTE["bg"])
            window.transient(self.master)
            window.grab_set()

            # 3. Crear la Vista (el Frame) y empaquetarla
            view_frame = ViewClass(window, viewmodel)
            view_frame.pack(fill="both", expand=True)
            
            # 4. Guardar referencia y manejar su cierre
            self.open_windows[key] = window
            # Cuando la ventana se cierre (por la 'X' o .destroy()),
            # la eliminamos del diccionario
            window.protocol("WM_DELETE_WINDOW", lambda: self.on_window_close(window, key))

        except Exception as e:
            print(f"Error fatal al abrir ventana {ViewClass.__name__}: {e}")
            messagebox.showerror("Error", f"No se pudo abrir la ventana:\n{e}")
            if 'window' in locals() and window.winfo_exists():
                window.destroy()
                if key in self.open_windows: del self.open_windows[key]

    def on_window_close(self, window: tk.Toplevel, key: str):
        """Maneja el cierre de una ventana Toplevel."""
        print(f"Cerrando ventana '{key}'...")
        if key in self.open_windows:
            del self.open_windows[key]
        if window and window.winfo_exists():
            window.destroy()

    def open_dummy(self, module_name: str):
        messagebox.showinfo("En Desarrollo", f"Módulo '{module_name}' no implementado.")

# --- Punto de Entrada ---

if __name__ == "__main__":
    
    dependencies = setup_dependencies()
    
    if dependencies:
        root = tk.Tk()
        setup_theme(root)
        
        app = MainApplication(
            root,
            viewmodels=dependencies["viewmodels"], # Pasar el diccionario de ViewModels
            datasource=dependencies["datasource"]
        )
        
        root.mainloop()

