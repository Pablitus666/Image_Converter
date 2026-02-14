import threading
import os # Necesario para os.path.splitext
from typing import Callable, Optional
from PIL import Image, UnidentifiedImageError # Añadir para abrir imagen

from core.converter import convert_image
from core.validator import is_supported_image
from core.errors import (
    ConversionError,
    AlreadyInTargetFormatError,
    FileWriteError,
    UnsupportedFormatError,
    InvalidImageError,
)
from core.i18n import _ as i18n_translate # Usar un alias para evitar conflictos


class ConversionResult:
    """
    Objeto de resultado estándar para comunicación Controller → UI
    """
    def __init__(self, success: bool, message: str, output_path: Optional[str] = None):
        self.success = success
        self.message = message
        self.output_path = output_path


def handle_image_conversion(
    file_path: str,
    target_format: str
) -> ConversionResult:
    """
    Orquesta el flujo completo de conversión de imagen.
    """

    if not file_path:
        return ConversionResult(
            success=False,
            message=i18n_translate("error.file_not_provided")
        )

    if not is_supported_image(file_path):
        return ConversionResult(
            success=False,
            message=i18n_translate("error.unsupported_image_extension")
        )
    
    # --- Regla de Negocio: Impedir conversión de ICO a otros formatos ---
    _, input_ext = os.path.splitext(file_path)
    if input_ext.lower() == ".ico" and target_format.upper() != "ICO":
        return ConversionResult(
            success=False,
            message=i18n_translate("error.ico_conversion_not_allowed")
        )
    
    # --- Regla de Negocio: Impedir conversión de GIF a otros formatos (pérdida de animación/calidad) ---
    if input_ext.lower() == ".gif" and target_format.upper() != "GIF":
        return ConversionResult(
            success=False,
            message=i18n_translate("error.gif_conversion_not_allowed")
        )
    
    # --- Verificar si ya está en el formato de destino ---
    try:
        with Image.open(file_path) as img:
            from config.constants import FORMAT_MAPPING # Importar la constante centralizada
            # Normalizar el formato de destino para la validación y comparación
            normalized_target = target_format.upper()
            normalized_target_format_for_comparison = FORMAT_MAPPING.get(normalized_target, normalized_target)

            if img.format and img.format.upper() == normalized_target_format_for_comparison:
                return ConversionResult(
                    success=False,
                    message="La imagen ya se encuentra en el formato seleccionado."
                )
    except UnidentifiedImageError:
        return ConversionResult(
            success=False,
            message=i18n_translate("error.invalid_image_or_corrupt")
        )
    except Exception as e:
        # Capturar otros posibles errores al abrir la imagen para verificar el formato
        return ConversionResult(
            success=False,
            message=i18n_translate("error.unexpected_image_load") + f" {e}"
        )

    try:
        output_path = convert_image(
            source_path=file_path,
            target_format=target_format
        )

        return ConversionResult(
            success=True,
            message="Imagen convertida correctamente.",
            output_path=output_path
        )

    except AlreadyInTargetFormatError:
        return ConversionResult(
            success=False,
            message=i18n_translate("error.already_in_target_format")
        )

    except UnsupportedFormatError as e:
        return ConversionResult(
            success=False,
            message=str(e)
        )

    except FileWriteError as e:
        return ConversionResult(
            success=False,
            message=f"No se pudo guardar el archivo:\n{e}"
        )

    except InvalidImageError:
        return ConversionResult(
            success=False,
            message="El archivo no es una imagen válida o está dañado."
        )

    except Exception as e:
        return ConversionResult(
            success=False,
            message=i18n_translate("error.unexpected_conversion") + f" {e}"
        )


class ConversionController:
    """
    Controlador responsable de ejecutar conversiones en segundo plano
    y comunicar resultados a la interfaz mediante callbacks.
    """

    def __init__(self):
        self._lock = threading.Lock()
        self._is_running = False

    @property
    def is_running(self) -> bool:
        with self._lock:
            return self._is_running

    def start_conversion(
        self,
        source_path: str,
        target_format: str,
        on_success: Callable[[str], None],
        on_error: Callable[[str], None]
    ):
        with self._lock:
            if self._is_running:
                return
            self._is_running = True

        thread = threading.Thread(
            target=self._run_conversion,
            args=(source_path, target_format, on_success, on_error),
            daemon=True
        )
        thread.start()

    def _run_conversion(
        self,
        source_path: str,
        target_format: str,
        on_success: Callable[[str], None],
        on_error: Callable[[str], None]
    ):
        try:
            result = handle_image_conversion(source_path, target_format)

            try:
                if result.success:
                    on_success(result.output_path)
                else:
                    on_error(result.message)
            except Exception as callback_error:
                on_error(i18n_translate("error.ui_callback") + f" {callback_error}")

        finally:
            with self._lock:
                self._is_running = False