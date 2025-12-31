# 🖼️ Image Converter v1.0.0 — Initial Stable Release

🎉 **Primera versión estable de Image Converter**, una aplicación de escritorio desarrollada en **Python** para la conversión rápida, segura y sencilla de imágenes mediante una **interfaz gráfica moderna**.

Este release marca una versión **completamente funcional, estable y lista para uso general**, así como para su distribución en forma de ejecutable.

---

## ✨ Características principales

* 📂 Carga de imágenes desde el explorador de archivos
* 👁️ Vista previa en tiempo real de la imagen seleccionada
* 🔄 Conversión entre múltiples formatos:

  * JPG / JPEG
  * PNG
  * WEBP
  * BMP
  * GIF
* ⚙️ Optimización automática según el formato de salida
* 🚀 Conversión en segundo plano (no bloquea la interfaz gráfica)
* 🧠 Manejo robusto de errores y advertencias personalizadas
* 🎨 Interfaz gráfica estilizada con identidad visual propia
* ⌨️ Atajos de teclado para mayor productividad
* 📦 Compatible con empaquetado mediante PyInstaller

---

## 🧰 Tecnologías utilizadas

* Python 3
* Tkinter (GUI)
* Pillow (PIL)
* Threading
* PyInstaller

---

## 🧠 Detalles técnicos

* Conversión segura de imágenes con transparencia (RGBA → RGB)
* Manejo correcto de recursos en modo desarrollo y ejecutable
* Gestión de estados para evitar acciones concurrentes
* Diseño enfocado en estabilidad, rendimiento y experiencia de usuario

---

## 🚀 Instalación

### Ejecutar desde código fuente

```bash
pip install pillow
python main.py
```

### Crear ejecutable

```bash
pyinstaller --onefile --windowed --add-data "images;images" main.py
```

---

## 📦 Archivos recomendados para adjuntar en el release

* `ImageConverter.exe` (Windows)
* `README.md`
* `LICENSE` (MIT)

---

## 👨‍💻 Autor

**Pablo Téllez A.**
📍 Tarija, Bolivia — 2025

---

⭐ Si este proyecto te resulta útil, considera dejar una estrella en el repositorio.
