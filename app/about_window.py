import os
import tkinter as tk
from tkinter import Toplevel
from PIL import Image, ImageTk, ImageOps

from core.resources import resource_path
from config import constants
from core.image_manager import ImageManager
from app.dialogs import BaseDialog # Import BaseDialog
from core.i18n import _

class AboutWindow(BaseDialog): # Inherit from BaseDialog
    def __init__(self, parent, image_manager: ImageManager, translator, icon_path=None):
        super().__init__(parent) # Call BaseDialog's init
        self.image_manager = image_manager
        self._ = translator # Use the passed translator

        self.title(self._("Información"))
        # bg and resizable handled by BaseDialog
        # transient(parent) handled by BaseDialog

        self._create_widgets()
        width, height = map(int, constants.INFO_POPUP_SIZE.split('x'))
        self._center_popup(width=width, height=height) # Use BaseDialog's center_popup

    def _create_widgets(self):
        frame = tk.Frame(self, bg=constants.COLOR_PRIMARY)
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        robot_photo = self.image_manager.load("assets/images/robot.png", size=(120, 120), add_shadow_effect=False)
        img_label = tk.Label(frame, image=robot_photo, bg=constants.COLOR_PRIMARY, bd=0, highlightthickness=0)
        img_label.image = robot_photo
        img_label.grid(row=0, column=0, rowspan=3, padx=(0, 10), pady=5, sticky="nsew")

        message = tk.Label(
            frame,
            text=self._("about.credits"),
            justify="center",
            bg=constants.COLOR_PRIMARY,
            fg=constants.COLOR_TEXT,
            font=constants.FONT_POPUP_BOLD,
            anchor="center",
            wraplength=170
        )
        message.grid(row=0, column=1, padx=(0, 25), pady=(10, 10), sticky="nsew")

        # Use _create_image_button from BaseDialog
        boton_photo = self.image_manager.load("assets/images/boton.png", size=(120, 45),
                                              add_shadow_effect=True, shadow_offset=(5, 5), shadow_color=(1, 34, 50, 100))
        close_btn = self._create_image_button(frame, self._("Cerrar"), boton_photo, self.destroy)
        close_btn.grid(row=2, column=1, padx=(0, 10), pady=(5, 5), sticky="ew")

