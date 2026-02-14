import json
import sys
from pathlib import Path
from typing import Dict
from core.resources import locale_path # Importar locale_path

class I18n:
    def __init__(self, default_language: str = "es") -> None:
        self.language = default_language
        self.translations: Dict[str, str] = {}

    def _base_path(self) -> Path:
        if getattr(sys, "frozen", False):
            # Running in a PyInstaller bundle
            return Path(sys._MEIPASS)
        # Running as a normal script
        return Path(__file__).resolve().parent.parent

    # No longer needed due to locale_path helper
    # def _locale_dir(self) -> Path:
    #     # El directorio 'locales' está dentro del directorio base del proyecto
    #     return self._base_path() / "locales"

    def load(self, language: str) -> None:
        self.language = language
        path = Path(locale_path(f"{language}.json")) # Usar locale_path helper

        try:
            with path.open(encoding="utf-8") as f:
                self.translations = json.load(f)
            
        except FileNotFoundError:
            print(f"WARNING: Archivo de idioma no encontrado: {path}")
            self.translations = {}
        except json.JSONDecodeError:
            print(f"ERROR: Error de formato en archivo de idioma: {path}")
            self.translations = {}

    def translate(self, message: str) -> str:
        return self.translations.get(message, message)


# --- API pública ---
_i18n = I18n()

def load_translations(language: str) -> None:
    _i18n.load(language)

def _(message: str) -> str:
    return _i18n.translate(message)