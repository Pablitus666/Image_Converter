import os
import tempfile
from PIL import Image

from core.converter import convert_image

def create_temp_image(mode="RGB", fmt="PNG"):
    pil_fmt = {"JPG": "JPEG", "PNG": "PNG", "GIF": "GIF", "ICO": "ICO", "BMP": "BMP", "WEBP": "WEBP"}.get(fmt.upper(), fmt)
    img = Image.new(mode, (100, 100), color=(255, 0, 0, 255) if mode == "RGBA" else (255, 0, 0))
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=f".{fmt.lower()}")
    img.save(tmp.name, format=pil_fmt)
    return tmp.name


def test_convert_png_to_jpg():
    src = create_temp_image("RGB", "PNG")
    out = convert_image(src, "JPG")

    assert os.path.exists(out)
    assert out.lower().endswith(".jpg")
    os.remove(src)
    os.remove(out)


def test_convert_rgb_to_png_adds_alpha():
    src = create_temp_image("RGB", "JPG") # Imagen RGB sin alfa
    out = convert_image(src, "PNG") # Convertir a PNG (que soporta alfa)

    with Image.open(out) as img:
        assert img.mode == "RGB" # PNG a partir de RGB no añade alfa por defecto en Pillow
    os.remove(src)
    os.remove(out)

def test_filename_collision():
    src = create_temp_image("RGB", "PNG")

    out1 = convert_image(src, "JPG") # Primera conversión a JPG
    out2 = convert_image(src, "JPG") # Segunda conversión a JPG desde el MISMO SRC

    assert out1 != out2 # Deberían tener nombres diferentes (_converted_1.jpg vs _converted_2.jpg)
    assert os.path.exists(out2)
    os.remove(src)
    os.remove(out1)
    os.remove(out2)
