# core/fonts.py
import platform
import ctypes
import os
import sys # Añadir para resource_path
from pathlib import Path

# Usar el resource_path del proyecto actual, no el de Ico_Converter
from core.resources import resource_path as project_resource_path

def load_font(font_path: str) -> None:
    if platform.system() == "Windows":
        try:
            FR_PRIVATE = 0x10
            FR_NOT_ENUM = 0x20
            # Convert Path object to string for ctypes
            ctypes.windll.gdi32.AddFontResourceExW(str(font_path), FR_PRIVATE | FR_NOT_ENUM, 0)
        except Exception as e:
            print(f"Error cargando fuente {font_path}: {e}")

def unload_font(font_path: str) -> None:
    if platform.system() == "Windows":
        try:
            FR_PRIVATE = 0x10
            FR_NOT_ENUM = 0x20
            # Convert Path object to string for ctypes
            ctypes.windll.gdi32.RemoveFontResourceExW(str(font_path), FR_PRIVATE | FR_NOT_ENUM, 0)
        except Exception as e:
            print(f"Error descargando fuente {font_path}: {e}")
