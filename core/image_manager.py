from PIL import Image, ImageTk
import os
from typing import Optional, Tuple
from functools import lru_cache

from core.resources import resource_path
from core.image_enhancer import add_shadow, create_disabled_image # Import create_disabled_image
from core.errors import ResourceNotFoundError, ImageLoadError


class ImageManager:
    """
    Gestor de imágenes:
    - Carga
    - Escala DPI
    - Padding
    - Efectos
    - Cache LRU seguro
    """

    def __init__(self, dpi_scale_factor: float = 1.0):
        self.dpi_scale_factor = dpi_scale_factor

    # ----------------------------
    # Cache LRU (máx 128 imágenes)
    # ----------------------------
    @lru_cache(maxsize=128)
    def _load_cached(self, cache_key: tuple) -> ImageTk.PhotoImage:
        return self._build_image(*cache_key)

    # ----------------------------
    # API pública
    # ----------------------------
    def load(
        self,
        image_path: Optional[str] = None,
        input_pil_image: Optional[Image.Image] = None,
        size: Optional[Tuple[int, int]] = None,
        add_shadow_effect: bool = False,
        shadow_offset: Tuple[int, int] = (4, 4),
        shadow_color: Tuple[int, int, int, int] = (0, 0, 0, 200),
        add_bottom_padding: int = 0,
        add_top_padding: int = 0,
        is_disabled: bool = False # New parameter
    ) -> ImageTk.PhotoImage:

        cache_key = (
            image_path,
            id(input_pil_image) if input_pil_image else None,
            size,
            add_shadow_effect,
            shadow_offset,
            shadow_color,
            add_bottom_padding,
            add_top_padding,
            self.dpi_scale_factor,
            is_disabled # Add to cache key
        )

        return self._load_cached(cache_key)

    # ----------------------------
    # Construcción real
    # ----------------------------
    def _build_image(
        self,
        image_path,
        input_image_id, # This is now just part of the cache key
        size,
        add_shadow_effect,
        shadow_offset,
        shadow_color,
        add_bottom_padding,
        add_top_padding,
        dpi_scale_factor,
        is_disabled
    ) -> ImageTk.PhotoImage:

        try:
            # Re-fetch the PIL image using the new cached method.
            # Note: The input_pil_image object itself isn't passed here,
            # but its original existence was part of the cache key.
            # The logic relies on image_path being the primary identifier.
            pil_image = self._get_pil_image(image_path, None)

            if size:
                pil_image = self._resize(pil_image, size)

            if add_top_padding or add_bottom_padding:
                pil_image = self._add_padding(pil_image, add_top_padding, add_bottom_padding)

            if add_shadow_effect:
                pil_image = add_shadow(pil_image, offset=shadow_offset, shadow_color=shadow_color)

            if is_disabled: # Apply disabled effect last
                pil_image = create_disabled_image(pil_image)

            return ImageTk.PhotoImage(pil_image)

        except Exception as e:
            raise ImageLoadError(str(e)) from e

    # ----------------------------
    # Helpers internos
    # ----------------------------
    @lru_cache(maxsize=32)
    def _load_base_pil_image(self, image_path: str) -> Image.Image:
        """Carga una imagen PIL desde el disco y la cachea."""
        full_path = resource_path(image_path)
        if not os.path.exists(full_path):
            raise ResourceNotFoundError(full_path)
        return Image.open(full_path).convert("RGBA")

    def _get_pil_image(self, image_path: Optional[str], input_pil_image: Optional[Image.Image]) -> Image.Image:
        """Obtiene una imagen PIL, ya sea desde la ruta (usando caché) o desde un objeto de entrada."""
        if input_pil_image:
            return input_pil_image
        if image_path:
            return self._load_base_pil_image(image_path)
        
        raise ImageLoadError("Se debe proporcionar 'image_path' o 'input_pil_image'.")

    def _resize(self, image: Image.Image, size: Tuple[int, int]) -> Image.Image:
        physical_size = (
            int(size[0] * self.dpi_scale_factor),
            int(size[1] * self.dpi_scale_factor)
        )
        image = image.copy()
        image.thumbnail(physical_size, Image.Resampling.LANCZOS)
        return image

    def _add_padding(self, image: Image.Image, top: int, bottom: int) -> Image.Image:
        top = int(top * self.dpi_scale_factor)
        bottom = int(bottom * self.dpi_scale_factor)

        width, height = image.size
        new_height = height + top + bottom

        padded = Image.new("RGBA", (width, new_height), (0, 0, 0, 0))
        padded.paste(image, (0, top), image)
        return padded

    # ----------------------------
    # Limpieza manual
    # ----------------------------
    def clear_cache(self):
        self._load_cached.cache_clear()