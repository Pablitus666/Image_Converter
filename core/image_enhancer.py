from PIL import Image, ImageChops, ImageOps # Import ImageOps

def add_shadow(image: Image.Image, offset: tuple[int, int] = (2, 2), shadow_color: tuple[int, int, int, int] = (150, 150, 150, 60)) -> Image.Image:
    """
    Añade un efecto de sombra a una imagen, creando una silueta desplazada.
    
    Args:
        image (Image.Image): La imagen PIL de entrada.
        offset (tuple[int, int]): El desplazamiento (x, y) de la sombra.
        shadow_color (tuple[int, int, int, int]): El color de la sombra en RGBA.
        
    Returns:
        Image.Image: Una nueva imagen PIL con la sombra aplicada.
    """
    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    alpha_mask = image.split()[-1]
    r, g, b, a = shadow_color

    shadow_img_rgb = Image.new('RGB', image.size, (r, g, b))
    
    scaled_alpha_mask = alpha_mask.point(lambda p: int(p * (a / 255.0)))
    
    final_shadow_image = shadow_img_rgb.copy()
    final_shadow_image.putalpha(scaled_alpha_mask)

    # Calcular el tamaño del nuevo lienzo para centrar la imagen original y acomodar la sombra
    # El lienzo debe ser lo suficientemente grande para la imagen original más el desplazamiento en todas las direcciones
    # Si offset es (dx, dy), el ancho total será original.width + abs(dx) para cada lado = original.width + 2*abs(dx)
    # y lo mismo para la altura.
    # Esto asegura que la imagen original pueda ser pegada en (abs(dx), abs(dy)) y aún haya espacio
    # para que la sombra se extienda fuera de ella.
    canvas_width = image.width + abs(offset[0]) * 2
    canvas_height = image.height + abs(offset[1]) * 2
    
    enhanced_image = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))

    # Posición para pegar la imagen original (centrada en el lienzo)
    original_paste_x = abs(offset[0])
    original_paste_y = abs(offset[1])

    # Posición para pegar la sombra (desplazada desde la posición de la imagen original)
    shadow_paste_x = original_paste_x + offset[0]
    shadow_paste_y = original_paste_y + offset[1]

    # Pegar la sombra
    enhanced_image.paste(final_shadow_image, (shadow_paste_x, shadow_paste_y), final_shadow_image)

    # Pegar la imagen original
    enhanced_image.paste(image, (original_paste_x, original_paste_y), image)

    return enhanced_image

def create_disabled_image(image: Image.Image) -> Image.Image:
    """
    Crea una versión visualmente deshabilitada de una imagen PIL.
    Desatura y atenúa la imagen con un overlay semitransparente.
    """
    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    # Desaturar (grayscale, then back to RGBA)
    grayscale_image = ImageOps.grayscale(image)
    grayscale_image_rgba = grayscale_image.convert("RGBA")
    
    # Blend with a semi-transparent black overlay
    overlay_color = (0, 0, 0, 80) # Semi-transparent black (80/255 alpha)
    black_overlay = Image.new("RGBA", image.size, overlay_color)
    
    # Alpha compose to dim the grayscale image
    final_disabled_image = Image.alpha_composite(grayscale_image_rgba, black_overlay)
    
    return final_disabled_image

