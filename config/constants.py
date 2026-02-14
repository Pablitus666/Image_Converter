# config/constants.py

# --- Colores y Estilo ---
COLOR_PRIMARY = "#023047"
COLOR_ACCENT = "#fcbf49"
COLOR_ACCENT_LIGHT = "#A1D6E2" # No usado en el original, pero mantenemos por consistencia
COLOR_TEXT = "white"
COLOR_DISABLED_TEXT = "#CCCCCC" # New: for disabled text
COLOR_DISABLED_BACKGROUND = "#011D29" # New: for disabled background
COLOR_PREVIEW_BG = "#0B1F2A"
COLOR_BUTTON_HOVER = "#fcbf49"
COLOR_BACKGROUND_DRAG_DROP = "#0B1F2A" # New default background for drag & drop area
COLOR_BACKGROUND_DRAG_DROP_HOVER = "#112F3C" # New hover background for drag & drop area
COLOR_DROP_AREA_BORDER = "#3FA9C4" # New border color for drag & drop area

# --- Tipografía ---
FONT_FAMILY_MAIN = "Inter"
FONT_SIZE_TITLE_MAIN = 22
FONT_SIZE_BODY = 12
FONT_SIZE_LABEL_FORMAT = 14
FONT_SIZE_STATUS = 12
FONT_SIZE_POPUP_TITLE = 14
FONT_SIZE_POPUP_BODY = 14
FONT_SIZE_BUTTON = 12
FONT_INFO = (FONT_FAMILY_MAIN, 14, "bold") # Added FONT_INFO as in Ico_Converter

FONT_BODY = (FONT_FAMILY_MAIN, FONT_SIZE_BODY) # Added non-bold FONT_BODY
FONT_BODY_BOLD = (FONT_FAMILY_MAIN, FONT_SIZE_BODY, "bold")
FONT_TITLE_MAIN_BOLD = (FONT_FAMILY_MAIN, FONT_SIZE_TITLE_MAIN, "bold")
FONT_LABEL_FORMAT_BOLD = (FONT_FAMILY_MAIN, FONT_SIZE_LABEL_FORMAT, "bold")
FONT_STATUS_BOLD = (FONT_FAMILY_MAIN, FONT_SIZE_STATUS, "bold")
FONT_BUTTON_BOLD = (FONT_FAMILY_MAIN, FONT_SIZE_BUTTON, "bold")
FONT_POPUP_BOLD = (FONT_FAMILY_MAIN, FONT_SIZE_POPUP_BODY, "bold")


# --- Ventana ---
WINDOW_TITLE = "Image Converter"
WINDOW_SIZE = "520x800" # Adjusted for more vertical space
WARNING_POPUP_SIZE = "400x190"
INFO_POPUP_SIZE = "370x230"

# --- Dimensiones de Widgets ---
PREVIEW_AREA_SIZE = 250 # Esto define el tamaño del frame, no de la imagen interna directamente
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 55 # Ajustado a las dimensiones del original boton.png

# --- Formatos ---
OUTPUT_FORMATS = ["JPG", "PNG", "WEBP", "BMP", "GIF", "ICO"] # ICO añadido como posibilidad futura
SUPPORTED_INPUT_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp", ".ico")

# --- ICO Sizes ---
ICON_SIZES = (
    (16, 16),
    (32, 32),
    (48, 48),
    (64, 64),
    (128, 128),
    (256, 256),
)

# --- Indicators ---
ALREADY_IN_FORMAT_INDICATOR = "FORMAT_ALREADY_MATCHES"

# --- Mapeo de formatos PIL (para comparación interna) ---
FORMAT_MAPPING = {
    "JPG": "JPEG",
    "JPEG": "JPEG",
    "PNG": "PNG",
    "WEBP": "WEBP",
    "BMP": "BMP",
    "GIF": "GIF",
    "ICO": "ICO",
}

