import time
import os
import tempfile
from PIL import Image

from core.controller import ConversionController
from core.errors import AlreadyInTargetFormatError, InvalidImageError, UnsupportedFormatError
from core.i18n import _ # Para usar en aserciones de mensajes

# Helper para crear archivos temporales de imagen para los tests
def create_temp_image_for_controller(mode="RGB", fmt="PNG", content=None):
    pil_fmt = {"JPG": "JPEG", "PNG": "PNG", "GIF": "GIF", "ICO": "ICO", "BMP": "BMP", "WEBP": "WEBP"}.get(fmt.upper(), fmt)
    if content:
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=f".{fmt.lower()}")
        tmp.write(content)
        tmp.close()
        return tmp.name
    else:
        img = Image.new(mode, (100, 100), color=(255, 0, 0, 255) if mode == "RGBA" else (255, 0, 0))
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=f".{fmt.lower()}")
        img.save(tmp.name, format=pil_fmt)
        return tmp.name


def test_controller_success(mocker):
    controller = ConversionController()
    
    # Mocks para saltar validaciones tempranas y asegurar que el archivo existe
    # Mockear convert_image como es importado en core.controller
    mocker.patch("core.controller.convert_image", return_value="/fake/output.png")
    # Mockear is_supported_image como es importado en core.controller
    mocker.patch("core.controller.is_supported_image", return_value=True)
    # Mockear os.path.isfile como es importado en core.controller
    mocker.patch("core.controller.os.path.isfile", return_value=True) 
    
    # Crear un mock de objeto Image con un formato controlable para Image.open
    mock_image_instance = mocker.MagicMock()
    mock_image_instance.format = "JPEG" # Default format diferente al target_format para evitar AlreadyInTargetFormatError
    mock_image_instance.copy.return_value = mock_image_instance # .copy() devuelve una copia de sí mismo

    # Mockear PIL.Image.open como es importado en core.controller
    mock_open_result = mocker.MagicMock()
    mock_open_result.__enter__.return_value = mock_image_instance
    mock_open_result.__exit__.return_value = None
    mocker.patch("core.controller.Image.open", return_value=mock_open_result)

    result_holder = {}

    controller.start_conversion(
        source_path="input.png",
        target_format="PNG",
        on_success=lambda r: result_holder.update(result=r),
        on_error=lambda e: result_holder.update(error=e),
    )

    time.sleep(0.5)  # permitir que el hilo termine (aumentado para mayor robustez)

    assert controller.is_running is False
    assert result_holder["result"] == "/fake/output.png"
    assert "error" not in result_holder


def test_controller_error_during_conversion(mocker):
    controller = ConversionController()

    # Mocks para saltar validaciones tempranas y asegurar que el archivo existe
    mocker.patch("core.controller.is_supported_image", return_value=True)
    mocker.patch("core.controller.os.path.isfile", return_value=True)

    # Mockear convert_image para que lance una excepción
    mocker.patch("core.controller.convert_image", side_effect=RuntimeError("Error de conversión simulado"))
    
    # Crear un mock de objeto Image con un formato controlable
    mock_image_instance = mocker.MagicMock()
    mock_image_instance.format = "PNG" # Simular el formato de la imagen abierta
    mock_image_instance.copy.return_value = mock_image_instance # Añadir mock para .copy()

    # Crear un mock para Image.open que devuelva el mock_image_instance
    mock_open_result = mocker.MagicMock()
    mock_open_result.__enter__.return_value = mock_image_instance
    mock_open_result.__exit__.return_value = None
    mocker.patch("core.controller.Image.open", return_value=mock_open_result)

    result_holder = {}

    controller.start_conversion(
        source_path="input.png",
        target_format="JPG",
        on_success=lambda r: result_holder.update(result=r),
        on_error=lambda e: result_holder.update(error=e),
    )

    time.sleep(0.5)  # permitir que el hilo termine (aumentado para mayor robustez)

    assert controller.is_running is False
    assert "result" not in result_holder
    assert _("error.unexpected_conversion") + " Error de conversión simulado" in result_holder["error"]


def test_controller_already_in_target_format(mocker):
    controller = ConversionController()
    
    # Mocks para saltar validaciones tempranas y asegurar que el archivo existe
    mocker.patch("core.controller.is_supported_image", return_value=True)
    mocker.patch("core.controller.os.path.isfile", return_value=True)

    # Crear un mock de objeto Image con un formato controlable
    mock_image_instance = mocker.MagicMock()
    mock_image_instance.format = "PNG" # Simular el formato destino
    mock_image_instance.copy.return_value = mock_image_instance # .copy() devuelve una copia de sí mismo

    # Crear un mock para Image.open que devuelva el mock_image_instance
    mock_open_result = mocker.MagicMock()
    mock_open_result.__enter__.return_value = mock_image_instance
    mock_open_result.__exit__.return_value = None
    mocker.patch("core.controller.Image.open", return_value=mock_open_result)

    result_holder = {}

    controller.start_conversion(
        source_path="input.png",
        target_format="PNG",
        on_success=lambda r: result_holder.update(result=r),
        on_error=lambda e: result_holder.update(error=e),
    )

    time.sleep(0.5)

    assert controller.is_running is False
    assert "result" not in result_holder
    assert "La imagen ya se encuentra en el formato seleccionado." == result_holder["error"]


def test_controller_unsupported_input_extension(mocker):
    controller = ConversionController()
    mocker.patch("core.controller.is_supported_image", return_value=False) # Simular extensión no soportada
    mocker.patch("core.controller.os.path.isfile", return_value=True) # El archivo "existe" pero no es soportado

    result_holder = {}

    controller.start_conversion(
        source_path="input.txt", # Archivo no soportado
        target_format="PNG",
        on_success=lambda r: result_holder.update(result=r),
        on_error=lambda e: result_holder.update(error=e),
    )

    time.sleep(0.5)

    assert controller.is_running is False
    assert "result" not in result_holder
    assert _("error.unsupported_image_extension") in result_holder["error"]

def test_controller_invalid_image_content(mocker):
    controller = ConversionController()
    mocker.patch("core.controller.is_supported_image", return_value=True)
    mocker.patch("core.controller.os.path.isfile", return_value=True) # Asegurar que el archivo existe

    # Crear un mock para Image.open que simule el lanzamiento de InvalidImageError
    mock_open_result = mocker.MagicMock()
    mock_open_result.__enter__.side_effect = InvalidImageError("Contenido de imagen inválido")
    mock_open_result.__exit__.return_value = None # Asegurarse de que el __exit__ funcione
    mocker.patch("core.controller.Image.open", return_value=mock_open_result)

    result_holder = {}

    controller.start_conversion(
        source_path="corrupt.jpg",
        target_format="PNG",
        on_success=lambda r: result_holder.update(result=r),
        on_error=lambda e: result_holder.update(error=e),
    )

    time.sleep(0.5)

    assert controller.is_running is False
    assert "result" not in result_holder
    assert "Contenido de imagen inválido" in result_holder["error"]

def test_controller_ico_conversion_restriction(mocker):
    controller = ConversionController()
    mocker.patch("core.controller.is_supported_image", return_value=True)
    mocker.patch("core.controller.os.path.isfile", return_value=True) # Asegurar que el archivo existe
    
    # Crear un mock de objeto Image con formato ICO
    mock_image_instance = mocker.MagicMock()
    mock_image_instance.format = "ICO"
    mock_image_instance.copy.return_value = mock_image_instance

    # Crear un mock para Image.open que devuelva el mock_image_instance
    mock_open_result = mocker.MagicMock()
    mock_open_result.__enter__.return_value = mock_image_instance
    mock_open_result.__exit__.return_value = None
    mocker.patch("core.controller.Image.open", return_value=mock_open_result)

    result_holder = {}

    controller.start_conversion(
        source_path="icon.ico",
        target_format="JPG", # Intento de convertir ICO a JPG
        on_success=lambda r: result_holder.update(result=r),
        on_error=lambda e: result_holder.update(error=e),
    )

    time.sleep(0.5)

    assert controller.is_running is False
    assert "result" not in result_holder
    assert _("error.ico_conversion_not_allowed") in result_holder["error"]

def test_controller_gif_conversion_restriction(mocker):
    controller = ConversionController()
    mocker.patch("core.controller.is_supported_image", return_value=True)
    mocker.patch("core.controller.os.path.isfile", return_value=True) # Asegurar que el archivo existe
    
    # Crear un mock de objeto Image con formato GIF
    mock_image_instance = mocker.MagicMock()
    mock_image_instance.format = "GIF"
    mock_image_instance.copy.return_value = mock_image_instance

    # Crear un mock para Image.open que devuelva el mock_image_instance
    mock_open_result = mocker.MagicMock()
    mock_open_result.__enter__.return_value = mock_image_instance
    mock_open_result.__exit__.return_value = None
    mocker.patch("core.controller.Image.open", return_value=mock_open_result)

    result_holder = {}

    controller.start_conversion(
        source_path="animated.gif",
        target_format="PNG", # Intento de convertir GIF a PNG
        on_success=lambda r: result_holder.update(result=r),
        on_error=lambda e: result_holder.update(error=e),
    )

    time.sleep(0.5)

    assert controller.is_running is False
    assert "result" not in result_holder
    assert _("error.gif_conversion_not_allowed") in result_holder["error"]
