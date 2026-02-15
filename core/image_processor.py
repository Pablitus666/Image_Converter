from PIL import Image
import math
import logging

# Configure logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Aumentamos el límite de Pillow pero de forma controlada
# 400 millones de píxeles (ej. 20,000 x 20,000) es un límite muy generoso
Image.MAX_IMAGE_PIXELS = 400_000_000

MAX_PROCESSING_DIMENSION = 8000      # dimensión máxima por lado

def open_and_resize_if_needed(path: str) -> Image.Image:
    """
    Abre una imagen y la redimensiona si excede las dimensiones máximas
    para evitar errores de DecompressionBomb y uso excesivo de memoria.
    """
    img = Image.open(path)
    width, height = img.size

    # Si alguna dimensión es demasiado grande, redimensionar
    if width > MAX_PROCESSING_DIMENSION or height > MAX_PROCESSING_DIMENSION:
        # Calcular el factor de escala para mantener la proporción
        scale_factor = min(
            MAX_PROCESSING_DIMENSION / width,
            MAX_PROCESSING_DIMENSION / height
        )

        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)

        logging.info(
            f"Imagen redimensionada automáticamente de "
            f"{width}x{height} a {new_width}x{new_height}"
        )

        # Redimensionar con un filtro de alta calidad pero rápido para seguridad
        img = img.resize(
            (new_width, new_height),
            Image.Resampling.BICUBIC
        )

    return img
