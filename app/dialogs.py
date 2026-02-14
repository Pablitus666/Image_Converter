import os
import tkinter as tk
from tkinter import Toplevel
from PIL import Image, ImageTk

from core.resources import image_path
from config import constants
from core.image_manager import ImageManager
from core.i18n import _

class BaseDialog(Toplevel):
    """Base class for custom dialogs."""
    def __init__(self, parent):
        super().__init__(parent)
        self.withdraw()  # Hide until fully configured

        self.parent = parent
        self.config(bg=constants.COLOR_PRIMARY)
        self.resizable(False, False)
        self.transient(parent)

        icon_path = image_path("icon.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)

    def _center_popup(self, width, height):
        self.update_idletasks()
        x = (self.parent.winfo_screenwidth() // 2) - (width // 2)
        y = (self.parent.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.deiconify() # Show centered window

    def _create_image_button(self, parent, text, image, command=None):
        button = tk.Button(parent, text=text, image=image, compound="center",
                           font=constants.FONT_BUTTON_BOLD, command=command,
                           bg=constants.COLOR_PRIMARY, fg=constants.COLOR_TEXT, bd=0, cursor="hand2",
                           highlightbackground=constants.COLOR_ACCENT, highlightthickness=2,
                           activebackground=constants.COLOR_PRIMARY, activeforeground=constants.COLOR_ACCENT)
        button.bind("<Enter>", lambda e: button.config(fg=constants.COLOR_ACCENT))
        button.bind("<Leave>", lambda e: button.config(fg=constants.COLOR_TEXT))
        return button

class WarningWindow(BaseDialog):
    def __init__(self, parent, message, image_manager: ImageManager, translator):
        super().__init__(parent)
        self.image_manager = image_manager
        self._ = translator
        self.title(self._("Advertencia"))
        
        self.update_idletasks()
        self.parent.update_idletasks()

        label = tk.Label(self, text=message, font=constants.FONT_POPUP_BOLD,
                         fg=constants.COLOR_TEXT, bg=constants.COLOR_PRIMARY, wraplength=360, justify="center")
        label.pack(pady=(25, 10), fill="both", expand=True)

        self.boton_photo = self.image_manager.load("assets/images/boton.png", size=(100, 35),
                                                    add_shadow_effect=True, shadow_offset=(5, 5), shadow_color=(1, 34, 50, 100))
        ok_button = self._create_image_button(self, self._("Aceptar"), self.boton_photo, self.destroy)
        ok_button.pack(pady=(0, 20))
        
        width, height = map(int, constants.WARNING_POPUP_SIZE.split('x'))
        self._center_popup(width=width, height=height)
