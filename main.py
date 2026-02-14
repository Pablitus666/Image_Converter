# main.py
import sys

from core.controller import ConversionController
from app.main_window import ImageConverterApp
from core.fonts import load_font, unload_font
from core.i18n import load_translations
from core.resources import resource_path


# -------------------------------------------------------------------
# Configuración global
# -------------------------------------------------------------------

load_translations("es")

FONT_PATHS = [
    resource_path("assets/fonts/InterVariable.ttf"),
]


# -------------------------------------------------------------------
# Punto de entrada
# -------------------------------------------------------------------

def main():
    # Cargar fuentes personalizadas
    for font_path in FONT_PATHS:
        load_font(font_path)

    # Inicializar controlador (core logic)
    controller = ConversionController()

    # Inicializar ventana principal e inyectar controller
    app = ImageConverterApp(controller)

    try:
        app.mainloop()
    finally:
        # Limpieza de recursos (especialmente útil en Windows)
        for font_path in FONT_PATHS:
            unload_font(font_path)


if __name__ == "__main__":
    main()
