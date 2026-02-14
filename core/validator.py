import os
from config.constants import SUPPORTED_INPUT_EXTENSIONS

def is_supported_image(file_path: str) -> bool:
    """
    Valida si el archivo tiene una extensión de imagen soportada.
    """
    if not file_path or not os.path.isfile(file_path):
        return False
    _, ext = os.path.splitext(file_path)
    return ext.lower() in SUPPORTED_INPUT_EXTENSIONS
