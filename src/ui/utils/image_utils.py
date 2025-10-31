# src/ui/utils/image_utils.py
import os
import shutil
import time
from tkinter import filedialog, messagebox, Toplevel
from typing import Optional, Dict, Tuple
from PIL import Image, ImageTk, UnidentifiedImageError # <-- Importaciones completas

class ImageManager:
    def __init__(self, parent: Toplevel, images_dir: str = "vehicle_images"):
        self.parent = parent # Para centrar el filedialog
        self.images_dir = os.path.join(os.getcwd(), images_dir)
        if not os.path.exists(self.images_dir):
            try: os.makedirs(self.images_dir)
            except OSError as e: print(f"Error al crear directorio de imágenes: {e}")
        
        # Caché para miniaturas
        self._image_cache: Dict[str, ImageTk.PhotoImage] = {}

    def select_and_copy_image(self) -> Optional[str]:
        """Abre un diálogo para seleccionar una imagen y la copia al directorio."""
        file_types = [("Imágenes", "*.jpg *.jpeg *.png *.gif *.bmp"), ("Todos", "*.*")]
        filename = filedialog.askopenfilename(
            parent=self.parent, # Usar el Toplevel como padre
            title="Seleccionar imagen del vehículo",
            filetypes=file_types
        )
        if not filename: return None

        try:
            # Validar y generar nuevo nombre
            with Image.open(filename) as img:
                img.verify() # Verifica si es una imagen válida
                # Usar formato detectado o extensión de archivo como fallback
                file_extension = (img.format or os.path.splitext(filename)[1][1:]).lower()
            
            timestamp = str(int(time.time()))
            # Asegurarse de que no haya un punto extra si la extensión ya lo tiene
            new_filename = f"vehicle_{timestamp}.{file_extension.lstrip('.')}"
            destination = os.path.join(self.images_dir, new_filename)
            
            # Copiar imagen
            shutil.copy2(filename, destination)
            return new_filename # Retorna el nombre relativo

        except UnidentifiedImageError:
            messagebox.showerror("Error", "El archivo seleccionado no es una imagen válida.", parent=self.parent)
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar imagen: {e}", parent=self.parent)
        return None

    def load_image_for_preview(self, image_name: str, size: Tuple[int, int] = (150, 150)) -> Optional[ImageTk.PhotoImage]:
        """Carga una imagen desde el directorio, la redimensiona y la cachea."""
        if not image_name: return None
        
        # Usar caché si está disponible
        if image_name in self._image_cache:
            return self._image_cache[image_name]

        full_path = os.path.join(self.images_dir, image_name)
        if not os.path.exists(full_path):
            print(f"Advertencia: No se encontró la imagen en {full_path}")
            return None
        
        try:
            with Image.open(full_path) as img:
                img.thumbnail(size) # Redimensiona (mantiene aspecto)
                photo_image = ImageTk.PhotoImage(img)
                self._image_cache[image_name] = photo_image # Guardar en caché
                return photo_image
        except Exception as e:
            print(f"Error al cargar miniatura: {e}")
            return None

    def clear_cache(self):
        """Limpia la caché de imágenes para liberar memoria."""
        print("Limpiando caché de ImageManager.")
        self._image_cache.clear()

