# src/ui/views/cliente_view.py
#
# Capa de IU (Vista).
# Contiene solo la lógica de la UI (Tkinter).

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
from src.domain.models.cliente import Cliente
from src.ui.viewmodels.cliente_viewmodel import ClienteViewModel
from src.ui.theme import PALETTE # <-- IMPORTAR PALETA

class ClienteView:
    def __init__(self, master: tk.Toplevel, view_model: ClienteViewModel):
        self.window = master
        self.view_model = view_model
        
        self.window.title("Gestión de Clientes")
        self.window.geometry("900x600")
        self.window.configure(bg=PALETTE["bg"]) # <-- APLICAR FONDO
        self.window.transient(master.master)
        self.window.grab_set()
        
        # Configurar grid para que la ventana se expanda
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        
        # Variables de control
        self.selected_id: Optional[int] = None
        self.nombre_var = tk.StringVar()
        self.apellido_var = tk.StringVar()
        self.dni_var = tk.StringVar()
        self.licencia_var = tk.StringVar()
        self.telefono_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.direccion_var = tk.StringVar()
        self.distrito_var = tk.StringVar()
        self.search_var = tk.StringVar()
        
        self.distritos = [
            "Huancayo", "El Tambo", "Chilca", "Sapallanga", "Huacrapuquio", "Viques", 
            "San Agustín de Cajas", "Hualhuas", "Sicaya", "Santo Domingo de Acobamba", 
            "Quilcas", "Pucará", "Cullhuas", "Chongos Alto", "Chicche", "Chupuro", 
            "Colca", "Mariscal Castilla", "Paca", "Pariahuanca", "Pilcomayo", 
            "Quichuay", "San Jerónimo de Tunán", "Saño", "Sincos", "Llocllapampa", 
            "Marco", "Masma", "Masma Chicche", "Mito", "Orcotuna", "Santa Rosa de Ocopa"
        ]
        
        self._create_widgets()
        
        # Suscribirse a las actualizaciones del ViewModel
        self.view_model.bind_to_updates(self.update_view)
        
        # Manejar el cierre de la ventana
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Carga inicial de datos
        self.view_model.cargar_clientes()
        
    def _create_widgets(self):
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # --- Formulario (Izquierda) ---
        form_frame = ttk.LabelFrame(main_frame, text="Datos del Cliente", padding="10")
        form_frame.grid(row=1, column=0, sticky="ns", padx=(0,10))
        
        form_grid = ttk.Frame(form_frame)
        form_grid.pack(fill="x")
        
        ttk.Label(form_grid, text="Nombre:").grid(row=0, column=0, sticky="w", pady=5)
        ttk.Entry(form_grid, textvariable=self.nombre_var, width=30).grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(form_grid, text="Apellido:").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Entry(form_grid, textvariable=self.apellido_var, width=30).grid(row=1, column=1, pady=5, padx=5)
        
        ttk.Label(form_grid, text="DNI:").grid(row=2, column=0, sticky="w", pady=5)
        ttk.Entry(form_grid, textvariable=self.dni_var, width=30).grid(row=2, column=1, pady=5, padx=5)
        
        ttk.Label(form_grid, text="Licencia:").grid(row=3, column=0, sticky="w", pady=5)
        ttk.Entry(form_grid, textvariable=self.licencia_var, width=30).grid(row=3, column=1, pady=5, padx=5)
        
        ttk.Label(form_grid, text="Teléfono:").grid(row=4, column=0, sticky="w", pady=5)
        ttk.Entry(form_grid, textvariable=self.telefono_var, width=30).grid(row=4, column=1, pady=5, padx=5)
        
        ttk.Label(form_grid, text="Email:").grid(row=5, column=0, sticky="w", pady=5)
        ttk.Entry(form_grid, textvariable=self.email_var, width=30).grid(row=5, column=1, pady=5, padx=5)
        
        ttk.Label(form_grid, text="Dirección:").grid(row=6, column=0, sticky="w", pady=5)
        ttk.Entry(form_grid, textvariable=self.direccion_var, width=30).grid(row=6, column=1, pady=5, padx=5)
        
        ttk.Label(form_grid, text="Distrito:").grid(row=7, column=0, sticky="w", pady=5)
        self.distrito_combo = ttk.Combobox(form_grid, textvariable=self.distrito_var, width=28, state="normal")
        self.distrito_combo['values'] = self.distritos
        self.distrito_combo.grid(row=7, column=1, pady=5, padx=5)
        # TODO: Re-implementar autocompletado si es necesario
        
        # Botones del Formulario
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill="x", pady=20)
        
        ttk.Button(button_frame, text="Guardar", command=self.on_save).pack(side="left", padx=5, expand=True, fill="x")
        ttk.Button(button_frame, text="Eliminar", command=self.on_delete).pack(side="left", padx=5, expand=True, fill="x")
        ttk.Button(button_frame, text="Limpiar", command=self.on_clear).pack(side="left", padx=5, expand=True, fill="x")

        # --- Lista (Derecha) ---
        list_frame = ttk.LabelFrame(main_frame, text="Lista de Clientes", padding="10")
        list_frame.grid(row=1, column=1, sticky="nsew")
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(1, weight=1)
        
        # Búsqueda
        search_frame = ttk.Frame(list_frame)
        search_frame.grid(row=0, column=0, sticky="ew", pady=(0,10))
        search_frame.columnconfigure(1, weight=1)
        
        ttk.Label(search_frame, text="Buscar:").grid(row=0, column=0, padx=(0,5))
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.grid(row=0, column=1, sticky="ew")
        search_entry.bind('<KeyRelease>', self.on_search)
        
        # Treeview
        columns = ("ID", "Nombre", "Apellido", "DNI", "Licencia", "Teléfono", "Email", "Distrito")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            if col == "ID":
                self.tree.column(col, width=40, stretch=tk.NO, anchor="center")
            elif col in ["DNI", "Licencia", "Teléfono"]:
                self.tree.column(col, width=100, stretch=tk.NO)
            else:
                self.tree.column(col, width=120)
        
        self.tree.grid(row=1, column=0, sticky="nsew")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Bind para selección
        self.tree.bind('<<TreeviewSelect>>', self.on_select_item)

    # --- Métodos de UI (Notifican al ViewModel) ---

    def on_save(self):
        success, message = self.view_model.guardar_cliente(
            id=self.selected_id,
            nombre=self.nombre_var.get(),
            apellido=self.apellido_var.get(),
            dni=self.dni_var.get(),
            licencia=self.licencia_var.get(),
            telefono=self.telefono_var.get(),
            email=self.email_var.get(),
            direccion=self.direccion_var.get(),
            distrito=self.distrito_var.get()
        )
        
        if success:
            messagebox.showinfo("Éxito", message)
            self.on_clear()
        else:
            messagebox.showerror("Error de Validación", message)

    def on_delete(self):
        if not self.selected_id:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para eliminar.")
            return
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este cliente?"):
            success = self.view_model.eliminar_cliente(self.selected_id)
            if success:
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo eliminar el cliente.")
            self.on_clear()

    def on_clear(self):
        self.view_model.seleccionar_cliente(None)

    def on_search(self, event=None):
        search_term = self.search_var.get()
        self.view_model.buscar_clientes(search_term)

    def on_select_item(self, event=None):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            selected_id = int(item['values'][0])
            
            # Buscar el objeto Cliente completo en el estado del ViewModel
            cliente_obj = next((c for c in self.view_model.clientes if c.id == selected_id), None)
            if cliente_obj:
                self.view_model.seleccionar_cliente(cliente_obj)
        
    def on_close(self):
        """
        Maneja el cierre de la ventana Toplevel.
        """
        # Darse de baja del viewmodel
        self.view_model.remove_observer(self.update_view)
        # Destruir la ventana
        self.window.destroy()

    # --- Métodos de Actualización (Llamados por el ViewModel) ---

    def update_view(self):
        """
        Actualiza la vista (Treeview y Formulario) cuando el
        ViewModel notifica un cambio de estado.
        """
        # Actualizar el Treeview
        self.tree.delete(*self.tree.get_children())
        for cliente in self.view_model.clientes:
            self.tree.insert("", "end", values=(
                cliente.id,
                cliente.nombre,
                cliente.apellido,
                cliente.dni,
                cliente.licencia,
                cliente.telefono,
                cliente.email,
                cliente.distrito
            ))
        
        # Actualizar el Formulario
        cliente = self.view_model.cliente_seleccionado
        if cliente:
            self.selected_id = cliente.id
            self.nombre_var.set(cliente.nombre)
            self.apellido_var.set(cliente.apellido)
            self.dni_var.set(cliente.dni)
            self.licencia_var.set(cliente.licencia)
            self.telefono_var.set(cliente.telefono)
            self.email_var.set(cliente.email)
            self.direccion_var.set(cliente.direccion)
            self.distrito_var.set(cliente.distrito)
        else:
            self.selected_id = None
            self.nombre_var.set("")
            self.apellido_var.set("")
            self.dni_var.set("")
            self.licencia_var.set("")
            self.telefono_var.set("")
            self.email_var.set("")
            self.direccion_var.set("")
            self.distrito_var.set("")
            
            # Limpiar selección del tree
            for item in self.tree.selection():
                self.tree.selection_remove(item)

