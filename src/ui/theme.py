# src/ui/theme.py
# (Versión consolidada y verificada - INCLUYE ESTILOS FALTANTES)

from tkinter import ttk

# Paleta de colores (Tema Oscuro de Alto Contraste)
PALETTE = {
    "bg": "#2E2E2E",          # Fondo principal (gris oscuro)
    "bg_light": "#3E3E3E",    # Fondo de widgets (gris medio)
    "fg": "#F0F0F0",          # Texto principal (blanco roto)
    "fg_dark": "#AAAAAA",     # Texto placeholder (gris)
    "primary": "#007ACC",     # Acento principal (azul brillante)
    "primary_light": "#009FFF", # Hover/Active
    "border": "#555555",       # Bordes
    "success": "#2ECC71"      # Color para éxito (ej. imagen cargada)
}

def setup_theme(root):
    """
    Configura el estilo ttk para toda la aplicación.
    """
    style = ttk.Style(root)
    style.theme_use('clam')

    # --- Configuraciones Globales ---
    style.configure(
        '.',  # Estilo raíz (todos los widgets)
        background=PALETTE["bg"],
        foreground=PALETTE["fg"],
        fieldbackground=PALETTE["bg_light"],
        bordercolor=PALETTE["border"],
        font=('Arial', 10),
        insertcolor=PALETTE["fg"] # Color del cursor en Entries
    )
    root.configure(bg=PALETTE["bg"])

    # --- Estilos Específicos ---

    # Frame y LabelFrame
    style.configure('TFrame', background=PALETTE["bg"])
    style.configure(
        'TLabel',
        background=PALETTE["bg"],
        foreground=PALETTE["fg"],
        font=('Arial', 10)
    )
    style.configure('TLabelFrame', background=PALETTE["bg"], bordercolor=PALETTE["border"], relief="solid", borderwidth=1)
    style.configure(
        'TLabelFrame.Label',
        background=PALETTE["bg"],
        foreground=PALETTE["fg"],
        font=('Arial', 11, 'bold')
    )

    # --- ESTILOS QUE FALTABAN (Causaban ventana en blanco) ---
    style.configure(
        "Heading.TLabel",
        background=PALETTE["bg"],
        foreground=PALETTE["primary"],
        font=('Arial', 16, 'bold')
    )
    style.configure(
        "Placeholder.TLabel",
        background=PALETTE["bg_light"], # Fondo del widget
        foreground=PALETTE["fg_dark"],
        font=('Arial', 9, 'italic'),
        anchor="center"
    )
    style.configure(
        "Success.TLabel",
        background=PALETTE["bg"],
        foreground=PALETTE["success"],
        font=('Arial', 9)
    )
    style.configure(
        "ImagePreview.TFrame",
        background=PALETTE["bg_light"],
        relief="solid",
        borderwidth=1,
        bordercolor=PALETTE["border"]
    )
    # --- FIN DE ESTILOS AÑADIDOS ---

    # Botón (TButton)
    style.configure(
        'TButton',
        background=PALETTE["primary"],
        foreground="#FFFFFF", # Blanco puro para mejor contraste
        bordercolor=PALETTE["primary"],
        font=('Arial', 10, 'bold'),
        padding=8,
        relief="flat"
    )
    style.map(
        'TButton',
        background=[('active', PALETTE["primary_light"]), ('disabled', PALETTE["border"])],
        foreground=[('disabled', PALETTE["bg_light"])],
        relief=[('pressed', 'sunken'), ('!pressed', 'flat')]
    )

    # Entry y Combobox
    style.configure(
        'TEntry',
        foreground=PALETTE["fg"],
        fieldbackground=PALETTE["bg_light"],
        bordercolor=PALETTE["border"],
        borderwidth=1,
        relief="flat"
    )
    style.map(
        'TEntry',
        bordercolor=[('focus', PALETTE["primary"])],
        relief=[('focus', 'solid')]
    )
    
    style.configure(
        'TCombobox',
        foreground=PALETTE["fg"],
        fieldbackground=PALETTE["bg_light"],
        bordercolor=PALETTE["border"],
        arrowcolor=PALETTE["fg"],
        background=PALETTE["bg_light"],
        relief="flat",
        borderwidth=1
    )
    style.map(
        'TCombobox',
        bordercolor=[('focus', PALETTE["primary"])],
        relief=[('focus', 'solid')]
    )
    # Arreglar el color de fondo del dropdown
    root.option_add('*TCombobox*Listbox.background', PALETTE["bg_light"])
    root.option_add('*TCombobox*Listbox.foreground', PALETTE["fg"])
    root.option_add('*TCombobox*Listbox.selectBackground', PALETTE["primary"])
    root.option_add('*TCombobox*Listbox.selectForeground', "#FFFFFF")

    # Treeview (Tabla)
    style.configure(
        'Treeview',
        rowheight=25,
        fieldbackground=PALETTE["bg_light"],
        background=PALETTE["bg_light"],
        foreground=PALETTE["fg"],
        borderwidth=0,
        relief="flat"
    )
    style.map('Treeview',
        background=[('selected', PALETTE["primary"])],
        foreground=[('selected', "#FFFFFF")]
    )

    style.configure(
        'Treeview.Heading',
        background=PALETTE["bg_light"],
        foreground=PALETTE["primary"],  # Texto primario
        font=('Arial', 10, 'bold'),
        relief="flat",
        padding=5
    )
    style.map('Treeview.Heading',
        background=[('active', PALETTE["border"])],
        relief=[('active', 'groove'), ('!active', 'flat')]
    )

    # Scrollbar
    style.configure(
        'Vertical.TScrollbar',
        background=PALETTE["bg"],
        troughcolor=PALETTE["bg_light"],
        bordercolor=PALETTE["bg"],
        arrowcolor=PALETTE["fg"],
        relief="flat"
    )
    style.map('Vertical.TScrollbar',
        background=[('active', PALETTE["border"])]
    )

