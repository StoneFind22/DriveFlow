# src/ui/views/vehiculo_view.py
# (Versión consolidada y verificada - CORRIGE HERENCIA, CIERRE y CARGA)
import tkinter as tk
from tkinter import ttk, messagebox
import os
from typing import Optional, Dict, Tuple
from PIL import Image, ImageTk
from src.domain.models.vehiculo import Vehiculo
from src.ui.viewmodels.vehiculo_viewmodel import VehiculoViewModel
from src.ui.utils.image_utils import ImageManager # <-- Importado   
from src.ui.theme import PALETTE

class VehiculoView(ttk.Frame): # <-- CORREGIDO: Heredar de ttk.Frame
    def __init__(self, master, viewmodel: VehiculoViewModel):
        super().__init__(master, style="TFrame")
        self.view_model = viewmodel
        self.image_manager = ImageManager(master) # <-- Activado, pasar Toplevel

        # --- Variables Tkinter ---
        self.selected_id: Optional[int] = None
        self.marca_var = tk.StringVar(); self.modelo_var = tk.StringVar()
        self.anio_var = tk.StringVar(); self.placa_var = tk.StringVar()
        self.tipo_var = tk.StringVar(); self.estado_var = tk.StringVar()
        self.precio_var = tk.StringVar(); self.kilometraje_var = tk.StringVar()
        self.garantia_var = tk.StringVar(value="S/ 0.00")
        self.imagen_path_var = tk.StringVar()
        self.search_var = tk.StringVar(); self.filter_var = tk.StringVar(value="Todos")
        self._inicializando = True
        self._current_image_tk: Optional[ImageTk.PhotoImage] = None # Para mantener referencia

        self.create_widgets()
        self.view_model.bind_to_updates(self.update_ui)
        self.view_model.cargar_datos_iniciales()
        self._inicializando = False

        self.bind("<Destroy>", self.on_destroy)

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.columnconfigure(0, weight=1); self.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1); main_frame.rowconfigure(1, weight=1)

        ttk.Label(main_frame, text="Gestión de Vehículos", style="Heading.TLabel").grid(row=0, column=0, columnspan=2, pady=(0,20), sticky="w")

        # --- Formulario ---
        form_frame = ttk.LabelFrame(main_frame, text="Datos del Vehículo", padding="10")
        form_frame.grid(row=1, column=0, sticky="ns", padx=(0,10))
        form_frame.columnconfigure(1, weight=1)
        
        campos = [("Marca:", self.marca_var), ("Modelo:", self.modelo_var),
                  ("Año:", self.anio_var), ("Placa:", self.placa_var)]
        for i, (texto, variable) in enumerate(campos):
            ttk.Label(form_frame, text=texto).grid(row=i, column=0, sticky="w", pady=2)
            ttk.Entry(form_frame, textvariable=variable).grid(row=i, column=1, pady=2, padx=(5,0), sticky="ew")

        ttk.Label(form_frame, text="Tipo:").grid(row=4, column=0, sticky="w", pady=2)
        self.tipo_combo = ttk.Combobox(form_frame, textvariable=self.tipo_var, state="readonly")
        self.tipo_combo.grid(row=4, column=1, pady=2, padx=(5,0), sticky="ew")
        self.tipo_combo.bind('<<ComboboxSelected>>', self.on_tipo_selected)
        
        ttk.Label(form_frame, text="Estado:").grid(row=5, column=0, sticky="w", pady=2)
        self.estado_combo = ttk.Combobox(form_frame, textvariable=self.estado_var, state="readonly")
        self.estado_combo.grid(row=5, column=1, pady=2, padx=(5,0), sticky="ew")
        
        campos_num = [("Precio/Día:", self.precio_var), ("Kilometraje:", self.kilometraje_var),
                      ("Garantía:", self.garantia_var)]
        for i, (texto, variable) in enumerate(campos_num, start=6):
            ttk.Label(form_frame, text=texto).grid(row=i, column=0, sticky="w", pady=2)
            state = "readonly" if texto == "Garantía:" else "normal"
            ttk.Entry(form_frame, textvariable=variable, state=state).grid(row=i, column=1, pady=2, padx=(5,0), sticky="ew")

        # --- Sección Imagen (Activada) ---
        ttk.Label(form_frame, text="Imagen:").grid(row=9, column=0, sticky="nw", pady=(5,2))
        image_controls_frame = ttk.Frame(form_frame); image_controls_frame.grid(row=9, column=1, pady=2, padx=(5,0), sticky="ew")
        image_controls_frame.columnconfigure(0, weight=1)
        
        self.imagen_label = ttk.Label(image_controls_frame, text="Sin imagen", style="Success.TLabel", anchor="w")
        self.imagen_label.grid(row=0, column=0, sticky="ew")
        
        self.image_preview_frame = ttk.Frame(form_frame, style="ImagePreview.TFrame", width=154, height=154)
        self.image_preview_frame.grid(row=10, column=0, columnspan=2, pady=(5,10))
        self.image_preview_label = ttk.Label(self.image_preview_frame, text="Sin imagen", style="Placeholder.TLabel")
        self.image_preview_label.place(relx=0.5, rely=0.5, anchor="center") # Centrar placeholder
        
        ttk.Button(form_frame, text="Seleccionar Imagen", command=self.select_image).grid(row=11, column=0, columnspan=2, pady=5, sticky="ew")
        
        # Botones Formulario
        button_frame = ttk.Frame(form_frame); button_frame.grid(row=12, column=0, columnspan=2, pady=(15,5))
        ttk.Button(button_frame, text="Guardar", command=self.on_save).pack(side="left", padx=5, fill="x", expand=True)
        ttk.Button(button_frame, text="Limpiar", command=self.clear_form).pack(side="left", padx=5, fill="x", expand=True)
        ttk.Button(button_frame, text="Eliminar", command=self.on_delete).pack(side="left", padx=5, fill="x", expand=True)

        # --- Lista ---
        list_frame = ttk.LabelFrame(main_frame, text="Lista de Vehículos", padding="10")
        list_frame.grid(row=1, column=1, sticky="nsew")
        list_frame.columnconfigure(0, weight=1); list_frame.rowconfigure(1, weight=1)
        
        filter_search_frame = ttk.Frame(list_frame); filter_search_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0,10))
        filter_search_frame.columnconfigure(1, weight=1); filter_search_frame.columnconfigure(3, weight=1)
        ttk.Label(filter_search_frame, text="Buscar:").grid(row=0, column=0, padx=(0,5))
        search_entry = ttk.Entry(filter_search_frame, textvariable=self.search_var); search_entry.grid(row=0, column=1, sticky="ew")
        search_entry.bind('<KeyRelease>', self.on_search_or_filter)
        ttk.Label(filter_search_frame, text="Filtrar estado:").grid(row=0, column=2, padx=(10,5))
        self.filter_combo = ttk.Combobox(filter_search_frame, textvariable=self.filter_var, state="readonly"); self.filter_combo.grid(row=0, column=3, sticky="ew")
        self.filter_combo.bind('<<ComboboxSelected>>', self.on_search_or_filter)
        
        columns = ("ID", "Marca", "Modelo", "Año", "Placa", "Tipo", "Estado", "Precio/Día")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        col_config = [
            ("ID", 40, "center", tk.NO), ("Marca", 80, "w", tk.YES), ("Modelo", 100, "w", tk.YES),
            ("Año", 50, "center", tk.NO), ("Placa", 80, "w", tk.NO), ("Tipo", 80, "w", tk.NO),
            ("Estado", 80, "w", tk.NO), ("Precio/Día", 80, "e", tk.NO)
        ]
        for col, width, anchor, stretch in col_config:
            self.tree.heading(col, text=col); self.tree.column(col, width=width, anchor=anchor, stretch=stretch)
        self.tree.grid(row=1, column=0, sticky="nsew")
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview); scrollbar.grid(row=1, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.bind('<<TreeviewSelect>>', self.on_select_item)

    def on_destroy(self, event):
        if event.widget == self:
            print("VehiculoView: Iniciando destrucción...")
            try:
                if hasattr(self, 'view_model') and self.view_model:
                     self.view_model.remove_observer(self.update_ui)
                     print("VehiculoView: Observador eliminado.")
                if hasattr(self, 'image_manager') and self.image_manager:
                   self.image_manager.clear_cache() # <-- Activado
                   print("VehiculoView: Caché de imagen limpiada.")
            except Exception as e:
                print(f"Error durante on_destroy en VehiculoView: {e}")

    def on_save(self):
        data_dict = {
            'marca': self.marca_var.get(), 'modelo': self.modelo_var.get(),
            'anio': self.anio_var.get(), 'placa': self.placa_var.get(),
            'tipo_nombre': self.tipo_combo.get(), 'estado_nombre': self.estado_combo.get(),
            'precio_por_dia': self.precio_var.get(), 'kilometraje': self.kilometraje_var.get(),
            'imagen_path': self.imagen_path_var.get()
        }
        success, message = self.view_model.guardar_vehiculo(self.selected_id, data_dict)
        if success: messagebox.showinfo("Éxito", message, parent=self); self.clear_form()
        else: messagebox.showerror("Error", message, parent=self)

    def on_delete(self):
        if not self.selected_id: messagebox.showwarning("Advertencia", "Seleccione vehículo.", parent=self); return
        if messagebox.askyesno("Confirmar", "¿Eliminar este vehículo?", parent=self):
            if self.view_model.eliminar_vehiculo(self.selected_id):
                messagebox.showinfo("Éxito", "Eliminado.", parent=self); self.clear_form()
            else: messagebox.showerror("Error", "No se pudo eliminar.", parent=self)

    def clear_form(self): self.view_model.seleccionar_vehiculo(None)

    def on_select_item(self, event=None):
        selection = self.tree.selection()
        if selection:
            try:
                selected_id = int(selection[0]) # IID es el ID del vehículo
                vehiculo_obj = next((v for v in self.view_model.vehiculos if v.id == selected_id), None)
                if vehiculo_obj: self.view_model.seleccionar_vehiculo(vehiculo_obj)
            except ValueError: print(f"Error: IID no válido: {selection[0]}")

    def on_search_or_filter(self, event=None):
        if self._inicializando: return
        self.view_model.buscar_y_filtrar_vehiculos(self.search_var.get(), self.filter_var.get())

    def on_tipo_selected(self, event=None):
        tipo_obj = next((t for t in self.view_model.tipos if t.nombre_tipo == self.tipo_var.get()), None)
        self.garantia_var.set(f"S/ {tipo_obj.garantia_base:.2f}" if tipo_obj else "S/ 0.00")

    def select_image(self):
        if hasattr(self, 'image_manager') and self.image_manager:
            new_image_name = self.image_manager.select_and_copy_image()
            if new_image_name:
                self.imagen_path_var.set(new_image_name)
                self.imagen_label.config(text=new_image_name)
                self._show_image_preview(new_image_name)
        else:
            messagebox.showerror("Error", "ImageManager no está inicializado.", parent=self)

    def _show_image_preview(self, image_name: Optional[str]):
         if hasattr(self, 'image_manager') and self.image_manager:
            photo = self.image_manager.load_image_for_preview(image_name or "")
            if photo:
                self._current_image_tk = photo # Mantener referencia
                self.image_preview_label.config(image=photo, text="") # Mostrar imagen
                self.image_preview_label.image = photo # Referencia extra
            else:
                self._current_image_tk = None
                self.image_preview_label.config(image=None, text="Sin imagen")
                self.image_preview_label.image = None
         else:
             self.image_preview_label.config(image=None, text="Error: No Mgr")

    def update_ui(self):
        print("VehiculoView: Recibida notificación, actualizando UI...")
        if not self.winfo_exists(): print("VehiculoView: UI destruida, cancelando."); return

        try:
            nombres_tipos = tuple(t.nombre_tipo for t in self.view_model.tipos if hasattr(t, 'nombre_tipo'))
            if self.tipo_combo['values'] != nombres_tipos: self.tipo_combo['values'] = nombres_tipos
        except Exception as e: print(f"Error actualizando combo Tipos: {e}")

        try:
            nombres_estados = tuple(e.nombre_estado for e in self.view_model.estados if hasattr(e, 'nombre_estado'))
            if self.estado_combo['values'] != nombres_estados: self.estado_combo['values'] = nombres_estados
            valores_filtro = ("Todos",) + nombres_estados
            if self.filter_combo['values'] != valores_filtro: self.filter_combo['values'] = valores_filtro
        except Exception as e: print(f"Error actualizando combo Estados/Filtro: {e}")

        try:
            current_selection = self.tree.selection()
            self.tree.delete(*self.tree.get_children())
            for vehiculo in self.view_model.vehiculos:
                tipo_nombre = getattr(getattr(vehiculo, 'tipo', None), 'nombre_tipo', 'Error')
                estado_nombre = getattr(getattr(vehiculo, 'estado', None), 'nombre_estado', 'Error')
                
                self.tree.insert("", "end", iid=vehiculo.id, values=(
                    vehiculo.id or "?", getattr(vehiculo, 'marca', 'N/A'),
                    getattr(vehiculo, 'modelo', 'N/A'), getattr(vehiculo, 'anio', 'N/A'),
                    getattr(vehiculo, 'placa', 'N/A'), tipo_nombre, estado_nombre,
                    f"{getattr(vehiculo, 'precio_por_dia', 0.0):.2f}"
                ))
            if current_selection and self.tree.exists(current_selection[0]):
                 self.tree.selection_set(current_selection[0])
        except Exception as e: print(f"Error crítico actualizando Treeview: {e}")

        try:
            if self.filter_var.get() != self.view_model.filter_estado_nombre:
                 self.filter_var.set(self.view_model.filter_estado_nombre)
        except Exception as e: print(f"Error actualizando var filtro: {e}")

        vehiculo_sel = self.view_model.vehiculo_seleccionado
        if vehiculo_sel:
            if self.selected_id != vehiculo_sel.id:
                self.selected_id = vehiculo_sel.id
                print(f"VehiculoView: Rellenando formulario para ID {self.selected_id}")
                self.marca_var.set(getattr(vehiculo_sel, 'marca', '')); self.modelo_var.set(getattr(vehiculo_sel, 'modelo', ''))
                self.anio_var.set(str(getattr(vehiculo_sel, 'anio', ''))); self.placa_var.set(getattr(vehiculo_sel, 'placa', ''))
                self.tipo_var.set(getattr(getattr(vehiculo_sel, 'tipo', None), 'nombre_tipo', ''))
                self.estado_var.set(getattr(getattr(vehiculo_sel, 'estado', None), 'nombre_estado', ''))
                self.precio_var.set(f"{getattr(vehiculo_sel, 'precio_por_dia', 0.0):.2f}")
                self.kilometraje_var.set(str(getattr(vehiculo_sel, 'kilometraje', '') or ''))
                self.garantia_var.set(f"S/ {getattr(getattr(vehiculo_sel, 'tipo', None), 'garantia_base', 0.0):.2f}")
                img_p = getattr(vehiculo_sel, 'imagen_path', '') or ''
                self.imagen_path_var.set(img_p)
                self.imagen_label.config(text=img_p or "Sin imagen")
                self._show_image_preview(img_p)

                sel_id_str = str(self.selected_id)
                if self.tree.exists(sel_id_str) and (not self.tree.selection() or self.tree.selection()[0] != sel_id_str):
                    self.tree.selection_set(sel_id_str); self.tree.focus(sel_id_str); self.tree.see(sel_id_str)
        else:
             if self.selected_id is not None:
                print("VehiculoView: Limpiando formulario.")
                self.selected_id = None
                self.marca_var.set(""); self.modelo_var.set(""); self.anio_var.set("")
                self.placa_var.set(""); self.tipo_var.set(""); self.estado_var.set("")
                self.precio_var.set(""); self.kilometraje_var.set("")
                self.garantia_var.set("S/ 0.00"); self.imagen_path_var.set("")
                self.imagen_label.config(text="Sin imagen")
                self._show_image_preview(None) # <-- Reactivado
                if self.tree.selection(): self.tree.selection_remove(self.tree.selection()[0])
        print("VehiculoView: Actualización UI completada.")

