# core/converter.py
from PIL import Image, ImageOps, UnidentifiedImageError
import os

from config import constants
from core.errors import (
    AlreadyInTargetFormatError,
    FileWriteError,
    UnsupportedFormatError,
    InvalidImageError,
)

# -------------------------------------------------------------------
# Constantes de formato (importadas)
# -------------------------------------------------------------------
from config.constants import FORMAT_MAPPING


def convert_image(source_path: str, target_format: str) -> str:
    """
    Convierte una imagen a un formato de destino y la guarda en el
    directorio original.

    Args:
        source_path (str): Ruta del archivo de imagen original.
        target_format (str): Formato destino ("PNG", "JPG", etc.).

    Returns:
        str: Ruta del archivo de salida.
    """

    normalized_target = target_format.upper()

    if normalized_target not in FORMAT_MAPPING:
        raise UnsupportedFormatError(
            f"El formato de salida '{target_format}' no está soportado."
        )

    try:
        with Image.open(source_path) as img:
            original_format = (img.format or "").upper()
            image = img.copy()
    except (IOError, UnidentifiedImageError) as e:
        raise InvalidImageError(
            f"No se pudo abrir la imagen '{source_path}': {e}"
        ) from e

    target_pil_format = FORMAT_MAPPING[normalized_target]

    # --- Validación: ya está en el formato destino ---
    if original_format == target_pil_format:
        raise AlreadyInTargetFormatError(
            f"La imagen ya está en formato {target_pil_format}."
        )

    # ----------------------------------------------------------------
    # Preparación de ruta de salida
    # ----------------------------------------------------------------

    source_dir = os.path.dirname(source_path)
    base_name = os.path.splitext(os.path.basename(source_path))[0]
    output_ext = normalized_target.lower()

    output_path_base = os.path.join(source_dir, f"{base_name}_converted")
    output_path = f"{output_path_base}.{output_ext}"

    counter = 0
    while os.path.exists(output_path):
        counter += 1
        output_path = f"{output_path_base}_{counter}.{output_ext}"

    # ----------------------------------------------------------------
    # Procesamiento de imagen
    # ----------------------------------------------------------------

    img_to_save = ImageOps.exif_transpose(image)

    save_options = {}

    # Formatos sin transparencia
    if output_ext in ("jpeg", "jpg", "bmp"):
        if img_to_save.mode in ("RGBA", "LA", "P"):
            img_to_save = img_to_save.convert("RGB")

        if output_ext in ("jpeg", "jpg"):
            save_options = {
                "quality": 90,
                "subsampling": -1,
            }

    # PNG
    elif output_ext == "png":
        save_options = {"compress_level": 4}

    # WEBP
    elif output_ext == "webp":
        save_options = {
            "quality": 90,
            "lossless": False,
        }

    # ICO
    elif output_ext == "ico":
        if img_to_save.mode != "RGBA":
            img_to_save = img_to_save.convert("RGBA")

        save_options = {
            "sizes": constants.ICON_SIZES
        }

    # ----------------------------------------------------------------
    # Guardado
    # ----------------------------------------------------------------

    try:
        save_format = "jpeg" if output_ext == "jpg" else output_ext
        img_to_save.save(output_path, format=save_format, **save_options)
    except OSError as e:
        raise FileWriteError(
            f"Error del sistema de archivos al guardar la imagen: {e}"
        ) from e
    except Exception as e:
        raise FileWriteError(
            f"Error inesperado al guardar la imagen convertida: {e}"
        ) from e

    return output_path