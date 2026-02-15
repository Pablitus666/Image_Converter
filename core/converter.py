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
from core.image_processor import open_and_resize_if_needed

# -------------------------------------------------------------------
# Constantes de formato (importadas)
# -------------------------------------------------------------------
from config.constants import FORMAT_MAPPING


def _save_with_format_settings(img: Image.Image, output_path: str, output_format: str):
    """
    Guarda la imagen con configuraciones de compresión optimizadas
    según el formato de salida.
    """
    output_format = output_format.upper()
    # PIL usa 'JPEG' para archivos .jpg
    save_format = "JPEG" if output_format == "JPG" else output_format

    save_options = {}

    # --- Preparar imagen y opciones según el formato ---

    if output_format in ("JPEG", "JPG"):
        # Convertir a RGB si tiene canal alfa para evitar errores en JPEG
        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGB")
        save_options = {
            "quality": 85,
            "optimize": True,
            "progressive": True
        }

    elif output_format == "PNG":
        save_options = {
            "optimize": True,
            "compress_level": 9  # Máxima compresión sin pérdida
        }

    elif output_format == "WEBP":
        save_options = {
            "quality": 85,
            "method": 6  # Mejor compresión (más lento)
        }

    elif output_format == "ICO":
        # El formato ICO necesita un modo que soporte transparencia
        if img.mode != "RGBA":
            img = img.convert("RGBA")
        save_options = {
            "sizes": constants.ICON_SIZES
        }
    
    elif output_format == "BMP":
        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGB")

    # --- Guardado ---
    try:
        img.save(output_path, format=save_format, **save_options)
    except OSError as e:
        raise FileWriteError(
            f"Error del sistema de archivos al guardar la imagen: {e}"
        ) from e
    except Exception as e:
        raise FileWriteError(
            f"Error inesperado al guardar la imagen convertida: {e}"
        ) from e




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

    img = None  # Inicializar para asegurar que exista en el bloque finally
    try:
        # Usa la nueva función para abrir y redimensionar si es necesario
        img = open_and_resize_if_needed(source_path)
        original_format = (img.format or "").upper()
        image = img.copy()
    except (IOError, UnidentifiedImageError) as e:
        raise InvalidImageError(
            f"No se pudo abrir la imagen '{source_path}': {e}"
        ) from e
    finally:
        # Cerrar el manejador del archivo de la imagen original si se abrió
        if img:
            img.close()

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
    # Procesamiento y Guardado
    # ----------------------------------------------------------------

    # Transponer la imagen si tiene metadatos de orientación EXIF
    img_to_save = ImageOps.exif_transpose(image)

    # --- Redimensionado Condicional ---
    # Si el formato destino es ICO, redimensionar a un tamaño estándar.
    if normalized_target == "ICO":
        # Usar LANCZOS para un redimensionado de alta calidad
        img_to_save = img_to_save.resize((256, 256), Image.Resampling.LANCZOS)

    # --- Guardado Inteligente ---
    # Usar la nueva función que aplica la compresión optimizada por formato
    _save_with_format_settings(img_to_save, output_path, normalized_target)

    return output_path