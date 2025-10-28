# src/ui/theme.py
#
# Módulo centralizado para la configuración de estilos y tema de la aplicación.

from tkinter import ttk

# Paleta de colores (Tema Oscuro de Alto Contraste)
PALETTE = {
    "bg": "#2E2E2E",          # Fondo principal (gris oscuro)
    "bg_light": "#3E3E3E",    # Fondo de widgets (gris medio)
    "fg": "#F0F0F0",          # Texto principal (blanco roto)
    "primary": "#007ACC",     # Acento principal (azul brillante)
    "primary_light": "#009FFF", # Hover/Active
    "border": "#555555"       # Bordes
}

def setup_theme(root):
    """
    Configura el estilo ttk para toda la aplicación.
    """
    style = ttk.Style(root)
    
    # Usar el tema 'clam' como base, es el más personalizable
    style.theme_use('clam')

    # --- Configuración Global ---
    style.configure(
        '.',  # Estilo raíz (todos los widgets)
        background=PALETTE["bg"],
        foreground=PALETTE["fg"],
        fieldbackground=PALETTE["bg_light"],
        bordercolor=PALETTE["border"],
        font=('Arial', 11)
    )
    
    # Configurar la ventana raíz
    root.configure(bg=PALETTE["bg"])

    # --- Estilos Específicos ---

    # Frame y LabelFrame
    style.configure('TFrame', background=PALETTE["bg"])
    style.configure('TLabel', background=PALETTE["bg"], foreground=PALETTE["fg"])
    style.configure('TLabelFrame', background=PALETTE["bg"], bordercolor=PALETTE["border"])
    style.configure(
        'TLabelFrame.Label',
        background=PALETTE["bg"],
        foreground=PALETTE["primary"],
        font=('Arial', 12, 'bold')
    )

    # Botón (TButton)
    style.configure(
        'TButton',
        background=PALETTE["primary"],
        foreground=PALETTE["fg"],
        bordercolor=PALETTE["primary"],
        font=('Arial', 11, 'bold'),
        padding=10
    )
    style.map(
        'TButton',
        background=[('active', PALETTE["primary_light"]), ('disabled', PALETTE["border"])],
        foreground=[('disabled', PALETTE["bg_light"])]
    )

    # Entry y Combobox
    style.configure(
        'TEntry',
        foreground=PALETTE["fg"],
        fieldbackground=PALETTE["bg_light"],
        bordercolor=PALETTE["border"],
        insertcolor=PALETTE["fg"] # Color del cursor
    )
    style.map('TEntry', bordercolor=[('focus', PALETTE["primary"])])

    # Treeview (Tabla)
    style.configure(
        'Treeview',
        rowheight=25,
        fieldbackground=PALETTE["bg_light"],
        background=PALETTE["bg_light"],
        foreground=PALETTE["fg"]
    )
    style.map('Treeview', background=[('selected', PALETTE["primary"])])

    style.configure(
        'Treeview.Heading',
        background=PALETTE["primary"],
        foreground=PALETTE["fg"],
        font=('Arial', 11, 'bold')
    )
    style.map('Treeview.Heading', background=[('active', PALETTE["primary_light"])])

    # Scrollbar
    style.configure('Vertical.TScrollbar', background=PALETTE["bg_light"], troughcolor=PALETTE["bg"], arrowcolor=PALETTE["fg"])
