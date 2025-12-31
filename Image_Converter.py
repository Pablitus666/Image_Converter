

import os
import sys
import tkinter as tk
from tkinter import filedialog, Toplevel, PhotoImage, OptionMenu, StringVar
from PIL import Image, ImageTk
import threading

# --- Constantes de Estilo y Configuración ---
BG_COLOR = "#023047"
ACCENT_COLOR = "#fcbf49"
LIGHT_BLUE_ACCENT = "#A1D6E2"
TEXT_COLOR = "white"
FONT_FAMILY = "Comic Sans MS"
PREVIEW_BG = "#1b1b1b"
OUTPUT_FORMATS = ["JPG", "PNG", "WEBP", "BMP", "GIF"]

def resource_path(relative_path):
    """ Obtiene la ruta absoluta del recurso, para desarrollo y para el ejecutable PyInstaller. """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class ImageConverterApp(tk.Tk):
    """
    Una aplicación de escritorio para convertir formatos de imagen con una interfaz gráfica,
    soportando selección de archivos y varias opciones de salida.
    """
    def __init__(self):
        super().__init__()
        self.withdraw()

        self.title("Image Converter")
        self.geometry("520x780")
        self.resizable(False, False)
        self.configure(bg=BG_COLOR)

        self.icon_path = resource_path(os.path.join("images", "icon.ico"))
        if os.path.exists(self.icon_path):
            self.iconbitmap(self.icon_path)

        # --- Variables de Estado ---
        self.image_path = None
        self.original_image = None
        self.preview_img = None
        self.warning_window = None
        self.info_window = None
        self.last_directory = "."
        self.is_converting = False
        self.format_var = StringVar(self)
        self.format_var.set(OUTPUT_FORMATS[0])

        self.load_assets()
        self.create_widgets()
        self.center_window()
        self.bind_shortcuts()

        self.deiconify()

    def center_window(self):
        """ Centra la ventana principal en la pantalla. """
        self.update_idletasks()
        width, height = self.winfo_width(), self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def load_assets(self):
        """ Carga recursos gráficos como imágenes para botones. """
        boton_path = resource_path(os.path.join("images", "boton.png"))
        self.boton_photo = None
        if os.path.exists(boton_path):
            img = Image.open(boton_path).resize((150, 55), Image.LANCZOS)
            self.boton_photo = ImageTk.PhotoImage(img)

    def _create_format_dropdown(self, parent):
        """ Crea un botón con imagen que simula un menú desplegable para la selección de formato. """
        self.format_button = self.create_image_button(parent, self.format_var.get(), self._show_format_menu)
        self.format_button.pack(side="left")

        self.format_actual_menu = tk.Menu(parent, tearoff=0, bg=BG_COLOR, fg=TEXT_COLOR, font=(FONT_FAMILY, 12))
        for choice in OUTPUT_FORMATS:
            self.format_actual_menu.add_command(label=choice, command=lambda c=choice: self._select_format(c))
        return self.format_button # Return the button for consistency with previous format_menu

    def _show_format_menu(self):
        """ Muestra el menú desplegable de formatos en la posición del botón. """
        # Get the current position of the button
        x = self.format_button.winfo_rootx()
        y = self.format_button.winfo_rooty() + self.format_button.winfo_height()
        self.format_actual_menu.post(x, y)

    def _select_format(self, choice):
        """ Actualiza la variable de formato y el texto del botón. """
        self.format_var.set(choice)
        self.format_button.config(text=choice)

    def create_widgets(self):
        """ Construye y posiciona todos los widgets de la GUI. """
        tk.Label(self, text="Image Converter", font=(FONT_FAMILY, 22, "bold"), fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=15)

        self.preview_frame = tk.Frame(self, width=250, height=250, bg=PREVIEW_BG)
        self.preview_frame.pack_propagate(False)
        self.preview_frame.pack(pady=10)

        self.drop_area = tk.Label(self.preview_frame, text="🖼️ Haz clic para seleccionar", font=(FONT_FAMILY, 12),
                                  bg=PREVIEW_BG, fg=TEXT_COLOR, relief="ridge", bd=4, cursor="hand2",
                                  highlightbackground=ACCENT_COLOR, highlightthickness=3)
        self.drop_area.pack(fill="both", expand=True)
        self.drop_area.bind("<Button-1>", self.select_image)
        self.drop_area.bind("<Enter>", lambda e: self.drop_area.config(bg="#2a2a2a"))
        self.drop_area.bind("<Leave>", lambda e: self.drop_area.config(bg=PREVIEW_BG))

        self.status_label = tk.Label(self, text="Listo para convertir", font=(FONT_FAMILY, 12, "bold"), fg=TEXT_COLOR,
                                     bg=BG_COLOR, wraplength=480, height=2, anchor="n")
        self.status_label.pack(pady=5)

        format_frame = tk.Frame(self, bg=BG_COLOR)
        format_frame.pack(pady=10)
        tk.Label(format_frame, text="Convertir a:", font=(FONT_FAMILY, 14, "bold"), fg=TEXT_COLOR, bg=BG_COLOR).pack(side="left", padx=(0, 10))
        
        self.format_menu = self._create_format_dropdown(format_frame)

        if self.boton_photo:
            self.convert_btn = self.create_image_button(self, "Convertir", self.start_conversion_thread)
            self.convert_btn.pack(pady=(15, 5))
            self.clear_btn = self.create_image_button(self, "Limpiar", self.clear_image)
            self.clear_btn.pack(pady=5)
            self.info_btn = self.create_image_button(self, "Información", self.show_info)
            self.info_btn.pack(pady=5)
            self.exit_btn = self.create_image_button(self, "Salir", self.quit)
            self.exit_btn.pack(pady=(5, 15))
        else:
            self.convert_btn = tk.Button(self, text="Convertir", command=self.start_conversion_thread)
            self.convert_btn.pack(pady=(15, 5))
            self.clear_btn = tk.Button(self, text="Limpiar", command=self.clear_image)
            self.clear_btn.pack(pady=5)
            self.info_btn = tk.Button(self, text="Información", command=self.show_info)
            self.info_btn.pack(pady=5)
            self.exit_btn = tk.Button(self, text="Salir", command=self.quit)
            self.exit_btn.pack(pady=5)

    def create_image_button(self, parent, text, command):
        """ Fábrica para crear botones con el estilo de la aplicación. """
        button = tk.Button(parent, text=text, image=self.boton_photo, compound="center", font=(FONT_FAMILY, 12, "bold"),
                           command=command, bg=BG_COLOR, fg=TEXT_COLOR, bd=0, cursor="hand2",
                           highlightbackground=ACCENT_COLOR, highlightthickness=2,
                           activebackground=BG_COLOR, activeforeground=ACCENT_COLOR)
        button.bind("<Enter>", lambda e: button.config(fg=ACCENT_COLOR))
        button.bind("<Leave>", lambda e: button.config(fg=TEXT_COLOR))
        return button

    def bind_shortcuts(self):
        """ Asigna atajos de teclado a funciones. """
        self.bind("<Return>", lambda e: self.start_conversion_thread())
        self.bind("<Delete>", lambda e: self.clear_image())

    def select_image(self, event=None):
        """ Abre un diálogo para seleccionar un archivo de imagen. """
        if self.is_converting: return
        filetypes = [("Archivos de imagen", "*.png *.jpg *.jpeg *.bmp *.gif *.webp"), ("Todos los archivos", "*.* ")]
        path = filedialog.askopenfilename(title="Seleccionar imagen", filetypes=filetypes, initialdir=self.last_directory)
        if path:
            self.last_directory = os.path.dirname(path)
            self.set_image(path)

    def set_image(self, path):
        """ Carga y muestra una vista previa de la imagen seleccionada. """
        try:
            self.status_label.config(text="Cargando imagen...")
            self.update_idletasks()
            self.image_path = path
            self.original_image = Image.open(path)
            preview = self.original_image.copy()
            preview.thumbnail((250, 250), Image.LANCZOS)
            self.preview_img = ImageTk.PhotoImage(preview)
            self.drop_area.config(image=self.preview_img, text="")
            self.status_label.config(text="Imagen cargada correctamente ✅")
        except Exception as e:
            self.clear_image()
            self.show_custom_warning(f"Error al cargar imagen:\n{e}")

    def clear_image(self, event=None):
        """ Restablece la vista previa de la imagen y el estado del programa. """
        if self.is_converting: return
        self.image_path = None
        self.original_image = None
        self.preview_img = None
        self.drop_area.config(image="", text="🖼️ Haz clic para seleccionar")
        self.status_label.config(text="Listo para convertir")

    def start_conversion_thread(self, event=None):
        """ Inicia el proceso de conversión en un hilo separado para no bloquear la GUI. """
        if self.is_converting:
            return
        if not self.original_image:
            self.show_custom_warning("Por favor, carga una imagen antes de convertir.")
            return
        
        self.is_converting = True
        self.toggle_widgets_state("disabled")
        self.status_label.config(text="Convirtiendo...")
        self.update_idletasks()

        thread = threading.Thread(target=self._execute_conversion)
        thread.daemon = True
        thread.start()

    def _execute_conversion(self):
        """
        Lógica de conversión que se ejecuta en un hilo secundario.
        No debe interactuar directamente con widgets de Tkinter.
        """
        try:
            source_dir = os.path.dirname(self.image_path)
            name = os.path.splitext(os.path.basename(self.image_path))[0]
            output_format = self.format_var.get().lower()
            output_path = os.path.join(source_dir, f"{name}_convertido.{output_format}")

            image_to_save = self.original_image.copy()
            if output_format in ['jpg', 'jpeg'] and image_to_save.mode in ('RGBA', 'LA', 'P'):
                image_to_save = image_to_save.convert('RGB')

            save_options = {}
            if output_format in ['jpg', 'jpeg']:
                save_options['quality'] = 95
            elif output_format == 'webp':
                save_options['quality'] = 100
                save_options['lossless'] = True
            elif output_format == 'png':
                save_options['compress_level'] = 1

            image_to_save.save(output_path, format=self.format_var.get(), **save_options)
            
            result_message = f"✅ ¡Guardado como {os.path.basename(output_path)}!"
            self.after(0, self._on_conversion_complete, result_message, False)

        except Exception as e:
            error_message = f"Error al convertir:\n{e}"
            self.after(0, self._on_conversion_complete, error_message, True)

    def _on_conversion_complete(self, message, is_error):
        """
        Se ejecuta en el hilo principal para actualizar la GUI de forma segura
        una vez que la conversión ha terminado.
        """
        if is_error:
            self.show_custom_warning(message)
            self.status_label.config(text="❌ Falló la conversión")
        else:
            self.status_label.config(text=message)
        
        self.is_converting = False
        self.toggle_widgets_state("normal")

    def toggle_widgets_state(self, state):
        """ Activa o desactiva los widgets interactivos durante la conversión. """
        self.convert_btn.config(state=state)
        self.clear_btn.config(state=state)
        self.format_button.config(state=state)
        self.drop_area.config(cursor="arrow" if state == "disabled" else "hand2")

    def show_custom_warning(self, message):
        """ Muestra una ventana emergente de advertencia personalizada. """
        if self.warning_window and self.warning_window.winfo_exists():
            self.warning_window.lift()
            return
        self.warning_window = Toplevel(self)
        self.warning_window.title("Advertencia")
        self.warning_window.configure(bg=BG_COLOR)
        self.warning_window.resizable(False, False)
        self.warning_window.transient(self)
        if os.path.exists(self.icon_path): self.warning_window.iconbitmap(self.icon_path)
        
        tk.Label(self.warning_window, text=message, font=(FONT_FAMILY, 14, "bold"), fg=TEXT_COLOR, bg=BG_COLOR, wraplength=360, justify="center").pack(pady=(25, 15), padx=20)
        
        def close_warning():
            self.warning_window.destroy()
            self.warning_window = None
        
        if self.boton_photo:
            ok_button = tk.Button(self.warning_window, text="Aceptar", image=self.boton_photo, compound="center", font=(FONT_FAMILY, 11, "bold"),
                                  command=close_warning, bg=BG_COLOR, fg=TEXT_COLOR, bd=0, cursor="hand2",
                                  highlightbackground=ACCENT_COLOR, highlightthickness=2,
                                  activebackground=BG_COLOR, activeforeground=ACCENT_COLOR)
            ok_button.bind("<Enter>", lambda e: ok_button.config(fg=ACCENT_COLOR))
            ok_button.bind("<Leave>", lambda e: ok_button.config(fg=TEXT_COLOR))
            ok_button.pack(pady=(0, 20))
        else:
            tk.Button(self.warning_window, text="Aceptar", command=close_warning).pack(pady=(0,20))
        
        self.center_popup(self.warning_window, 400, 190)

    def show_info(self):
        """ Muestra la ventana de información del desarrollador. """
        if self.info_window and self.info_window.winfo_exists():
            self.info_window.lift()
            return
        self.info_window = Toplevel(self)
        self.info_window.title("Información")
        self.info_window.config(bg=BG_COLOR)
        self.info_window.resizable(0, 0)
        self.info_window.transient(self)
        if os.path.exists(self.icon_path): self.info_window.iconbitmap(self.icon_path)

        frame = tk.Frame(self.info_window, bg=BG_COLOR)
        frame.pack(pady=10, padx=10)

        img_path = resource_path(os.path.join("images", "robot.png"))
        if os.path.exists(img_path):
            img = PhotoImage(file=img_path)
            img_label = tk.Label(frame, image=img, bg=BG_COLOR)
            img_label.image = img
            img_label.grid(row=0, column=0, padx=10, pady=5, rowspan=3)

        tk.Label(frame, text="Desarrollado por: \nPablo Téllez A.\n\nTarija - 2025.", justify="center", bg=BG_COLOR, fg=TEXT_COLOR, font=(FONT_FAMILY, 14, "bold")).grid(row=0, column=1, padx=8, pady=10, sticky="n")
        
        if self.boton_photo:
            close_btn = tk.Button(frame, text="Cerrar", image=self.boton_photo, compound="center", font=(FONT_FAMILY, 12, "bold"),
                                  command=self.info_window.destroy, bg=BG_COLOR, fg=TEXT_COLOR, bd=0, cursor="hand2",
                                  highlightbackground=ACCENT_COLOR, highlightthickness=2,
                                  activebackground=BG_COLOR, activeforeground=ACCENT_COLOR)
            close_btn.bind("<Enter>", lambda e: close_btn.config(fg=ACCENT_COLOR))
            close_btn.bind("<Leave>", lambda e: close_btn.config(fg=TEXT_COLOR))
            close_btn.grid(row=2, column=1, padx=10, pady=(0, 5), sticky="n")
        else:
            tk.Button(frame, text="Cerrar", command=self.info_window.destroy).grid(row=2, column=1, padx=10, pady=(0, 5), sticky="n")

        self.center_popup(self.info_window, 370, 230)

    def center_popup(self, window, width, height):
        """ Centra una ventana emergente relativa a la ventana principal. """
        self.update_idletasks() 
        x = self.winfo_x() + (self.winfo_width() // 2) - (width // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

if __name__ == "__main__":
    app = ImageConverterApp()
    app.mainloop()
