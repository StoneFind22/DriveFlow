# main.py
#
# Punto de entrada principal de la aplicación.
# Responsable de la Inyección de Dependencias (DI) y de iniciar la UI.

import tkinter as tk
from tkinter import ttk, messagebox
import os
from functools import partial
from dotenv import load_dotenv # <-- IMPORTAR dotenv

# --- Importaciones de la Arquitectura ---

# Capa de Datos
from src.data.datasources.sql_server_datasource import SQLServerDataSource
from src.data.repositories.cliente_repository_impl import ClienteRepositoryImpl

# Capa de Dominio
from src.domain.usecases.cliente_usecases import (
    ObtenerClientesUseCase,
    GuardarClienteUseCase,
    EliminarClienteUseCase,
    ValidarClienteUseCase,
    BuscarClientesUseCase
)

# Capa de IU
from src.ui.viewmodels.cliente_viewmodel import ClienteViewModel
from src.ui.views.cliente_view import ClienteView
from src.ui.theme import setup_theme, PALETTE

# --- Cargar Variables de Entorno ---
load_dotenv() # <-- Cargar el archivo .env

# --- Ensamblador de Dependencias (DI) ---

def setup_dependencies():
    """
    Inicializa y conecta todas las dependencias de la aplicación.
    """
    try:
        # 1. Leer Configuración desde variables de entorno
        server = os.environ.get('DB_SERVER', 'localhost')
        database = os.environ.get('DB_NAME', 'AlquilerAutos')
        username = os.environ.get('DB_USERNAME') # Dejar que sea None si no está
        password = os.environ.get('DB_PASSWORD') # Dejar que sea None si no está
        
        if not server or not database:
            raise ValueError("Las variables de entorno DB_SERVER y DB_NAME deben estar definidas en .env")

        # 3. Inicializar Capa de Datos
        datasource = SQLServerDataSource.get_instance(
            server=server,
            database=database,
            username=username,
            password=password
        )
        cliente_repo = ClienteRepositoryImpl(datasource)
        
        # 4. Inicializar Capa de Dominio
        cliente_usecases = {
            'obtener_clientes': ObtenerClientesUseCase(cliente_repo),
            'guardar_cliente': GuardarClienteUseCase(cliente_repo),
            'eliminar_cliente': EliminarClienteUseCase(cliente_repo),
            'validar_cliente': ValidarClienteUseCase(),
            'buscar_clientes': BuscarClientesUseCase(cliente_repo)
        }
        
        # 5. Inicializar Capa de IU
        cliente_viewmodel = ClienteViewModel(
            obtener_clientes_usecase=cliente_usecases['obtener_clientes'],
            guardar_cliente_usecase=cliente_usecases['guardar_cliente'],
            eliminar_cliente_usecase=cliente_usecases['eliminar_cliente'],
            validar_cliente_usecase=cliente_usecases['validar_cliente'],
            buscar_clientes_usecase=cliente_usecases['buscar_clientes']
        )
        
        return cliente_viewmodel

    except (ValueError, Exception) as e:
        messagebox.showerror(
            "Error Crítico de Inicio",
            f"No se pudo iniciar la aplicación:\n{e}\n\nRevise su archivo .env y la conexión a la base de datos."
        )
        return None

# --- Clase Principal de la Aplicación (Vista Principal) ---

class MainApplication(tk.Frame):
    def __init__(self, master, cliente_viewmodel: ClienteViewModel):
        super().__init__(master)
        self.master = master
        self.master.title("Sistema de Gestión de Alquiler de Autos")
        self.master.geometry("900x600")
        
        # Guardar referencias a los ViewModels
        self.cliente_viewmodel = cliente_viewmodel
        
        # --- Configuración del Dashboard Escalable ---
        self.dashboard_modules = [
            {
                "title": "Gestionar Clientes",
                "command": self.open_gestion_clientes,
                "view_name": "clientes" # Identificador único
            },
            {
                "title": "Gestionar Vehículos",
                "command": partial(self.open_dummy_feature, "Vehículos"),
                "view_name": "vehiculos"
            },
            {
                "title": "Gestionar Reservas",
                "command": partial(self.open_dummy_feature, "Reservas"),
                "view_name": "reservas"
            },
            {
                "title": "Gestionar Contratos",
                "command": partial(self.open_dummy_feature, "Contratos"),
                "view_name": "contratos"
            },
            {
                "title": "Gestionar Entregas",
                "command": partial(self.open_dummy_feature, "Entregas"),
                "view_name": "entregas"
            },
            {
                "title": "Gestionar Devoluciones",
                "command": partial(self.open_dummy_feature, "Devoluciones"),
                "view_name": "devoluciones"
            }
        ]
        
        self._create_widgets()

    def _create_widgets(self):
        main_frame = ttk.Frame(self.master, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Frame del Título
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(pady=(10, 30))
        ttk.Label(title_frame, text="Dashboard Principal", font=("Arial", 24, "bold"), foreground=PALETTE["primary"]).pack()
        
        # Frame de Botones (escalable)
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Configurar la cuadrícula para 3 columnas
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)
        buttons_frame.columnconfigure(2, weight=1)

        # Iterar sobre los módulos para crear botones dinámicamente
        for i, module in enumerate(self.dashboard_modules):
            row = i // 3  # Fila
            col = i % 3   # Columna
            
            btn = ttk.Button(
                buttons_frame,
                text=module["title"],
                command=module["command"]
            )
            btn.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
            buttons_frame.rowconfigure(row, weight=1) # Hacer que las filas se expandan


    def open_gestion_clientes(self):
        try:
            cliente_window = tk.Toplevel(self.master)
            ClienteView(cliente_window, self.cliente_viewmodel)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la ventana de clientes: {e}")

    def open_dummy_feature(self, module_name: str):
        """Placeholder para funcionalidades aún no migradas."""
        messagebox.showinfo(
            "En Desarrollo",
            f"El módulo '{module_name}' aún no ha sido migrado a la nueva arquitectura."
        )

# --- Punto de Entrada ---

if __name__ == "__main__":
    
    # 1. Intentar configurar dependencias
    cliente_viewmodel = setup_dependencies()
    
    if cliente_viewmodel:
        # 2. Crear la ventana raíz
        root = tk.Tk()
        
        # 3. Aplicar el tema oscuro centralizado
        setup_theme(root)
        
        # 4. Iniciar la aplicación
        app = MainApplication(root, cliente_viewmodel)
        root.mainloop()

