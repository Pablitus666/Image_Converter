# core/resources.py

import os
import sys
from typing import Optional

from core.errors import ResourceNotFoundError


def get_base_path() -> str:
    """
    Retorna la ruta base de recursos tanto en desarrollo
    como en ejecutables PyInstaller.
    """
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        # PyInstaller
        return sys._MEIPASS

    # Desarrollo: raíz del proyecto (no cwd)
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )


def resource_path(relative_path: str, *, must_exist: bool = True) -> str:
    """
    Construye una ruta absoluta a un recurso del proyecto.

    :param relative_path: Ruta relativa (ej: assets/images/icon.png)
    :param must_exist: Lanza error si el recurso no existe
    """
    base_path = get_base_path()
    full_path = os.path.normpath(os.path.join(base_path, relative_path))

    if must_exist and not os.path.exists(full_path):
        raise ResourceNotFoundError(full_path)

    return full_path


# ----------------------------
# Helpers especializados
# ----------------------------

def image_path(filename: str) -> str:
    return resource_path(os.path.join("assets", "images", filename))


def font_path(filename: str) -> str:
    return resource_path(os.path.join("assets", "fonts", filename))


def locale_path(filename: str) -> str:
    return resource_path(os.path.join("locales", filename), must_exist=False)