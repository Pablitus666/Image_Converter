import tempfile
import pytest
import os # Import os for cleanup
from PIL import Image # AÑADIR ESTO

from core.converter import convert_image
from core.errors import (
    UnsupportedFormatError,
    InvalidImageError,
    AlreadyInTargetFormatError # Add this for a new test
)

def test_unsupported_format():
    with tempfile.NamedTemporaryFile(suffix=".png") as tmp:
        with pytest.raises(UnsupportedFormatError):
            convert_image(tmp.name, "TIFF")


def test_invalid_image():
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    tmp.write(b"NOT AN IMAGE")
    tmp.close()

    with pytest.raises(InvalidImageError):
        convert_image(tmp.name, "PNG")
    os.remove(tmp.name) # Clean up the invalid file


def test_already_in_target_format():
    # Create a temporary PNG image
    src = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    Image.new("RGB", (10, 10)).save(src.name, format="PNG")
    src.close()

    # Attempt to convert PNG to PNG, should raise AlreadyInTargetFormatError
    with pytest.raises(AlreadyInTargetFormatError):
        convert_image(src.name, "PNG")
    os.remove(src.name)
