import tkinter as tk
from tkinter import filedialog, StringVar
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk, UnidentifiedImageError

import os
import threading

from config import constants
from core.resources import image_path
from app.dialogs import WarningWindow
from app.about_window import AboutWindow
from core.image_manager import ImageManager
from core.i18n import _
from core.controller import ConversionController

class ImageConverterApp(TkinterDnD.Tk):
    def __init__(self, controller: ConversionController):
        super().__init__()
        self.withdraw()

        self.title(_(constants.WINDOW_TITLE))
        self.geometry(constants.WINDOW_SIZE)
        self.resizable(False, False)
        self.configure(bg=constants.COLOR_PRIMARY)

        self.icon_path = image_path("icon.ico")
        if os.path.exists(self.icon_path):
            self.iconbitmap(self.icon_path)

        # --- State Variables ---
        self.image_path = None
        self.preview_img = None
        self.warning_window = None
        self.info_window = None
        self.last_directory = "."
        self.ui_locked = False
        
        # --- Threading State for Preview Loading ---
        self.preview_thread_lock = threading.Lock()
        self.is_loading_preview = False

        self.format_var = StringVar(self)
        self.format_var.set(constants.OUTPUT_FORMATS[0])

        # --- Managers and Assets ---
        self.dpi_scale_factor = self.tk.call("tk", "scaling")
        self.image_manager = ImageManager(self.dpi_scale_factor)
        self.controller = controller
        self.load_assets()
        
        self.create_widgets()
        self.center_window()
        self.bind_shortcuts()
        self.bind_drag_drop()

        self.deiconify()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def load_assets(self):
        self.title_img = self.image_manager.load(image_path("titulo.png"), size=(300, 75), add_shadow_effect=True)
        self.boton_photo = self.image_manager.load(image_path("boton.png"), size=(constants.BUTTON_WIDTH, constants.BUTTON_HEIGHT), add_shadow_effect=True, shadow_offset=(5, 5), shadow_color=(1, 34, 50, 100))
        
        self.drag_drop_icon_photo = self.image_manager.load(image_path=image_path("drag_drop_icon.png"), size=(64, 64), add_top_padding=10, add_bottom_padding=20)
        hover_scale = 1.05
        hover_size = (int(64 * hover_scale), int(64 * hover_scale))
        self.drag_drop_icon_hover_photo = self.image_manager.load(image_path=image_path("drag_drop_icon.png"), size=hover_size, add_top_padding=10, add_bottom_padding=20)


    def create_widgets(self):
        title_label = tk.Label(self, image=self.title_img, bg=constants.COLOR_PRIMARY, cursor="hand2")
        title_label.pack(pady=(30, 10))
        title_label.bind("<Button-1>", lambda e: self.show_info_window())

        self.preview_frame = tk.Frame(self, width=280, height=280, bg=constants.COLOR_BACKGROUND_DRAG_DROP)
        self.preview_frame.pack_propagate(False)
        self.preview_frame.pack(pady=15)

        self.drop_area = tk.Label(self.preview_frame,
                                  text=_("Arrastra tu imagen aquí\n\u200b\no haz clic para seleccionar"),
                                  font=constants.FONT_BODY,
                                  bg=constants.COLOR_BACKGROUND_DRAG_DROP, fg=constants.COLOR_TEXT,
                                  width=35,
                                  relief="ridge", bd=4, cursor="hand2", anchor="center",
                                  highlightbackground=constants.COLOR_DROP_AREA_BORDER, highlightthickness=3,
                                  image=self.drag_drop_icon_photo,
                                  compound="top")
        self.drop_area.image = self.drag_drop_icon_photo
        self.drop_area.pack(fill="both", expand=True)

        self.status_label = tk.Label(self, text=_("Listo para convertir"), font=constants.FONT_STATUS_BOLD,
                                     fg=constants.COLOR_TEXT, bg=constants.COLOR_PRIMARY, wraplength=480,
                                     height=2, anchor="n")
        self.status_label.pack(pady=5)

        format_frame = tk.Frame(self, bg=constants.COLOR_PRIMARY)
        format_frame.pack(pady=10)
        tk.Label(format_frame, text=_("Convertir a:"), font=constants.FONT_LABEL_FORMAT_BOLD,
                 fg=constants.COLOR_TEXT, bg=constants.COLOR_PRIMARY).pack(side="left", padx=(0, 10))
        
        self.format_menu_widget = self._create_format_dropdown(format_frame)

        # New button layout using a grid
        buttons_frame = tk.Frame(self, bg=constants.COLOR_PRIMARY)
        buttons_frame.pack(pady=20) # Add some padding to the top of the button frame

        # Configure grid columns
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)

        # Convert Button (Left Column, Top Row)
        self.convert_btn = self.create_image_button(buttons_frame, _("Convertir"), self.start_conversion_thread, image=self.boton_photo)
        self.convert_btn.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        # Open Folder Button (Right Column, Top Row) - New button
        # I need a photo for open button, I'll use boton1.png
        open_folder_photo = self.image_manager.load(image_path("boton1.png"), size=(constants.BUTTON_WIDTH, constants.BUTTON_HEIGHT), add_shadow_effect=True, shadow_offset=(5, 5), shadow_color=(1, 34, 50, 100))
        self.open_folder_btn = self.create_image_button(buttons_frame, _("Abrir"), self.open_output_folder, image=open_folder_photo)
        self.open_folder_btn.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        # Clear Button (Left Column, Bottom Row)
        self.clear_btn = self.create_image_button(buttons_frame, _("Limpiar"), self.clear_image, image=self.boton_photo)
        self.clear_btn.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        # Exit Button (Right Column, Bottom Row)
        self.exit_btn = self.create_image_button(buttons_frame, _("Salir"), self.quit_app, image=self.boton_photo)
        self.exit_btn.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    def create_image_button(self, parent, text, command, image=None): # Added optional image parameter
        image_to_use = image if image is not None else self.boton_photo # Use provided image or default
        
        def command_wrapper():
            if self.ui_locked:
                return
            command()

        button = tk.Button(parent, text=text, image=image_to_use, compound="center",
                           font=constants.FONT_BUTTON_BOLD,
                           command=command_wrapper, bg=constants.COLOR_PRIMARY, fg=constants.COLOR_TEXT, bd=0,
                           cursor="hand2", highlightbackground=constants.COLOR_ACCENT, highlightthickness=2,
                           activebackground=constants.COLOR_PRIMARY, activeforeground=constants.COLOR_ACCENT)
        
        button.normal_image = image_to_use # Store the normal image

        def on_enter(e):
            if self.ui_locked:
                return
            e.widget.config(fg=constants.COLOR_ACCENT)

        def on_leave(e):
            # Always revert to default color, state check is implicitly handled by on_enter
            e.widget.config(fg=constants.COLOR_TEXT)

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        return button
        
    def _create_format_dropdown(self, parent):
        self.format_button = self.create_image_button(parent, self.format_var.get(), self._show_format_menu)
        self.format_button.pack(side="left")

        self.format_actual_menu = tk.Menu(parent, tearoff=0, bg=constants.COLOR_PRIMARY, fg=constants.COLOR_TEXT,
                                          font=(constants.FONT_FAMILY_MAIN, constants.FONT_SIZE_BODY))
        for choice in constants.OUTPUT_FORMATS:
            self.format_actual_menu.add_command(label=choice, command=lambda c=choice: self._select_format(c))
        return self.format_button

    def _show_format_menu(self):
        if self.ui_locked: return
        self.update_idletasks()
        x = self.format_button.winfo_rootx()
        y = self.format_button.winfo_rooty() + self.format_button.winfo_height()
        self.format_actual_menu.post(x, y)

    def _select_format(self, choice):
        self.format_var.set(choice)
        self.format_button.config(text=choice)
        
    def bind_shortcuts(self):
        self.bind("<Return>", lambda e: self.start_conversion_thread())
        self.bind("<Delete>", lambda e: self.clear_image())

    def bind_drag_drop(self):
        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind("<<Drop>>", self._handle_drop)
        self.drop_area.bind("<Button-1>", self.select_image)

        def on_drop_area_enter(e):
            if self.ui_locked: return
            self.drop_area.config(bg=constants.COLOR_BACKGROUND_DRAG_DROP_HOVER)

        self.drop_area.bind("<Enter>", on_drop_area_enter)
        self.drop_area.bind("<Leave>", lambda e: self.drop_area.config(bg=constants.COLOR_BACKGROUND_DRAG_DROP))
        self.drop_area.dnd_bind("<<DropEnter>>", self._on_drag_enter)
        self.drop_area.dnd_bind("<<DropLeave>>", self._on_drag_leave)

    def _is_valid_image_extension(self, path: str) -> bool:
        ext = os.path.splitext(path)[1].lower()
        return ext in constants.SUPPORTED_INPUT_EXTENSIONS

    def _on_drag_enter(self, event):
        if self.ui_locked: return
        self.drop_area.config(text=_("Suelta la imagen"), image=self.drag_drop_icon_hover_photo, font=constants.FONT_BODY_BOLD)
        self.drop_area.image = self.drag_drop_icon_hover_photo
        self.drop_area.config(bg=constants.COLOR_BACKGROUND_DRAG_DROP_HOVER)

    def _on_drag_leave(self, event):
        if self.ui_locked: return
        self.reset_drop_area_ui()

    def _handle_drop(self, event):
        if self.ui_locked: return
        files = self.tk.splitlist(event.data)
        if len(files) > 1:
            self.show_warning_window(_("warning.multiple_files_dropped"))
            return

        filepath = files[0].strip('{}')
        self.set_image(filepath)

    def select_image(self, event=None):
        if self.ui_locked: return
        filetypes = [(_("Archivos de imagen"), " ".join(constants.SUPPORTED_INPUT_EXTENSIONS)), (_("Todos los archivos"), "*.* ")]
        path = filedialog.askopenfilename(title=_("Seleccionar imagen"), filetypes=filetypes, initialdir=self.last_directory)
        if path:
            self.last_directory = os.path.dirname(path)
            self.set_image(path)

    def set_image(self, path: str):
        """
        Inicia el proceso de carga de la vista previa en un hilo separado
        para no bloquear la interfaz de usuario.
        """
        with self.preview_thread_lock:
            if self.is_loading_preview:
                return  # Ya hay una carga en curso

        if not self._is_valid_image_extension(path):
            self.show_warning_window(_("error.unsupported_image_extension"))
            return

        self.image_path = path
        self._set_ui_locked(True) # Bloquear UI al iniciar carga
        self.status_label.config(text=_("Cargando imagen..."))
        
        with self.preview_thread_lock:
            self.is_loading_preview = True

        # Iniciar el worker en un hilo daemon
        thread = threading.Thread(
            target=self._load_preview_worker,
            args=(path,),
            daemon=True
        )
        thread.start()

    def _load_preview_worker(self, path: str):
        """
        Worker que se ejecuta en un hilo separado para cargar y procesar
        la imagen para la vista previa.
        """
        img = None
        try:
            # Abrir la imagen. La protección contra DecompressionBomb se confía
            # a la configuración global de Image.MAX_IMAGE_PIXELS.
            img = Image.open(path)

            if img.format == 'JPEG':
                img.draft('thumbnails', (250, 250))

            img.thumbnail((250, 250), Image.Resampling.LANCZOS)
            
            # Crear el objeto PhotoImage aquí, que puede ser tardado
            preview_photo = ImageTk.PhotoImage(img)

            # Si todo fue exitoso, programar la actualización de la UI en el hilo principal
            self.after(0, self._update_preview_ui, preview_photo)

        except (IOError, UnidentifiedImageError):
            self.after(0, self._on_preview_error, _("error.invalid_image_or_corrupt"))
        
        except Exception as e:
            error_message = f'{_("error.unexpected_image_load")}\n{e}'
            self.after(0, self._on_preview_error, error_message)

        finally:
            if img:
                img.close()
            with self.preview_thread_lock:
                self.is_loading_preview = False

    def _update_preview_ui(self, preview_photo):
        """
        Callback para actualizar la UI con la nueva vista previa.
        Se ejecuta en el hilo principal.
        """
        self.preview_img = preview_photo
        self.drop_area.config(image=self.preview_img, text="")
        self.status_label.config(text=_("Imagen cargada correctamente ✅"))
        self._set_ui_locked(False) # Desbloquear UI al finalizar

    def _on_preview_error(self, message: str):
        """
        Callback para manejar errores durante la carga de la vista previa.
        Se ejecuta en el hilo principal.
        """
        # Inlined from clear_image to bypass the ui_locked check
        self.image_path = None
        self.preview_img = None
        self.reset_drop_area_ui()
        self.show_warning_window(message)
        self.status_label.config(text=_("Error al cargar la imagen"))
        self._set_ui_locked(False) # Desbloquear UI en caso de error

    def clear_image(self, event=None):
        if self.ui_locked: return
        self.image_path = None
        self.preview_img = None
        self.reset_drop_area_ui()
        self.status_label.config(text=_("Listo para convertir"))

    def reset_drop_area_ui(self):
        self.drop_area.config(text=_("Arrastra tu imagen aquí\n\u200b\no haz clic para seleccionar"), image=self.drag_drop_icon_photo, font=constants.FONT_BODY)
        self.drop_area.image = self.drag_drop_icon_photo
        self.drop_area.config(bg=constants.COLOR_BACKGROUND_DRAG_DROP)

    def start_conversion_thread(self, event=None):
        if self.controller.is_running:
            return

        if not self.image_path:
            self.show_warning_window(_("error.no_image_to_convert"))
            return

        self._set_ui_locked(True)
        self.status_label.config(text=_("Convirtiendo..."))
        self.update_idletasks()

        self.controller.start_conversion(
            source_path=self.image_path,
            target_format=self.format_var.get(),
            on_success=lambda result: self.after(0, self._on_conversion_success, result),
            on_error=lambda msg: self.after(0, self._on_conversion_error, msg)
        )

    def _on_conversion_success(self, result: str):
        # El caso "ALREADY_IN_FORMAT" ahora se maneja como un error,
        # por lo que on_success siempre recibe una ruta de archivo válida.
        self.status_label.config(
            text=_("✅ ¡Guardado como {file}!").format(file=os.path.basename(result))
        )

        self._set_ui_locked(False)

    def _on_conversion_error(self, message):
        self.show_warning_window(f'{_("error.conversion_failed_prefix")}\n{message}')
        self.status_label.config(text=_("❌ Falló la conversión"))
        self._set_ui_locked(False)

    def _set_ui_locked(self, locked: bool):
        """
        Locks or unlocks the UI without changing widget appearance.
        It sets a flag and changes the cursor.
        """
        self.ui_locked = locked
        cursor = "arrow" if locked else "hand2"

        # List of all interactive widgets
        widgets_to_toggle = [self.convert_btn, self.open_folder_btn, self.clear_btn, self.exit_btn, self.format_button, self.drop_area]

        for widget in widgets_to_toggle:
            widget.config(cursor=cursor)

    def show_info_window(self):
        if self.ui_locked: return
        if self.info_window and self.info_window.winfo_exists():
            self.info_window.lift()
            return
        self.info_window = AboutWindow(self, self.image_manager, _, self.icon_path)

    def show_warning_window(self, message):
        if self.warning_window and self.warning_window.winfo_exists():
            self.warning_window.destroy()  # Close existing warning window if open
        self.warning_window = WarningWindow(self, message, self.image_manager, _)
        self.warning_window.grab_set()  # Make it modal
        self.wait_window(self.warning_window)  # Wait for it to close

    def open_output_folder(self):
        if self.ui_locked: return
        if self.image_path:
            output_dir = os.path.dirname(self.image_path)
            try:
                os.startfile(output_dir) # Windows specific
            except Exception as e:
                self.show_warning_window(f'{_("error.open_output_folder_failed_prefix")}\n{e}')
        else:
            self.show_warning_window(_("error.no_conversion_done_yet"))

    def quit_app(self):
        self.destroy()