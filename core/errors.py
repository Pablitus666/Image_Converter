# core/errors.py

class ImageConverterError(Exception):
    """Error base de la aplicación."""
    pass

class ResourceNotFoundError(ImageConverterError):
    """Recurso no encontrado (imágenes, fuentes, etc)."""
    def __init__(self, path: str):
        super().__init__(_("error.resource_not_found") + f" {path}")
        self.path = path

class ImageLoadError(ImageConverterError):
    """Error al cargar o procesar una imagen."""
    pass

class ConversionError(ImageConverterError): # Heredar de ImageConverterError para una jerarquía consistente
    """Error base de conversión."""
    pass

class AlreadyInTargetFormatError(ConversionError):
    """La imagen ya está en el formato destino."""
    pass

class InvalidImageError(ConversionError):
    """La imagen es inválida o está corrupta."""
    pass

class UnsupportedFormatError(ConversionError):
    """Formato de salida no soportado."""
    pass

class FileWriteError(ConversionError):
    """No se pudo escribir el archivo convertido."""
    pass