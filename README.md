# 🖼️ Image Converter

Aplicación de escritorio profesional para **convertir imágenes entre distintos formatos**, desarrollada en Python con **Tkinter**, enfocada en ofrecer una experiencia moderna, segura y robusta para usuarios finales y entornos profesionales.

---

![Status](https://img.shields.io/badge/status-stable-brightgreen)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)
![GUI](https://img.shields.io/badge/GUI-Tkinter-blueviolet)
![Drag & Drop](https://img.shields.io/badge/feature-Drag%20%26%20Drop-orange)
![Executable](https://img.shields.io/badge/.exe-signed-success)
![License](https://img.shields.io/github/license/Pablitus666/Image_Converter)

---

![Social Preview](assets/images/Preview.png)

---

## ✨ Características principales

* 🎯 **Conversión rápida y confiable de imágenes**
  * Soporta formatos comunes de imagen de forma segura.

* 🚀 **Manejo optimizado de imágenes gigantes**
  * **Protección Anti-Crash:** Evita errores `DecompressionBomb` al procesar imágenes de muy alta resolución.
  * **UI sin bloqueos:** La carga de la vista previa se ejecuta en un hilo separado, manteniendo la interfaz fluida y receptiva en todo momento.

* ⚙️ **Procesamiento inteligente de imágenes**
  * **Compresión optimizada:** Aplica configuraciones de compresión específicas para cada formato (JPEG progresivo, máxima compresión en PNG) para un equilibrio ideal entre calidad y peso.
  * **Redimensionado condicional:** Ajusta automáticamente el tamaño de las imágenes para formatos con restricciones (ej. ICO a 256x256), manteniendo la máxima calidad en los demás.

* 🖱️ **Drag & Drop intuitivo**
  * Arrastra imágenes directamente a la aplicación.
  * Estados visuales claros durante la conversión.

* 🧠 **Validación inteligente de archivos**
  * Rechazo automático de archivos no compatibles.
  * Solo se procesan imágenes válidas.

* 🚫 **Protección contra errores comunes**
  * Manejo controlado de excepciones.
  * Mensajes claros y comprensibles para el usuario.

* 🌍 **Internacionalización (i18n)**
  * Sistema de traducciones basado en JSON.
  * Idioma por defecto: Español (extensible).

* 🖼️ **UI optimizada para HiDPI**
  * Conciencia de DPI en Windows.
  * Interfaz preparada para pantallas de alta resolución.

* 🧩 **Arquitectura modular**
  * Separación clara entre UI, controladores y lógica de conversión.
  * Código mantenible y escalable.

* 📂 **Acceso rápido a resultados**
  * Apertura directa de la carpeta de salida.

* 📝 **Logging interno**
  * Registro de eventos y errores para depuración.

* 🔐 **Ejecutable `.exe` firmado digitalmente**
  * Compatible con Windows 10 / 11
  * No requiere instalación de Python ni dependencias externas
  * Drag & Drop completamente funcional

---

## 🗂️ Formatos soportados

### ✅ Imágenes de entrada

* `.png`
* `.jpg` / `.jpeg`
* `.bmp`
* `.webp`
* `.gif` (conversión a otros formatos no permitida para evitar pérdida de animación)
* `.ico` (conversión a otros formatos no permitida)

### ❌ Archivos rechazados

* Archivos no reconocidos como imagen
* Archivos corruptos o inválidos

---

## 🖥 Interfaz de usuario

**Image Converter** cuenta con una interfaz gráfica moderna basada en Tkinter, diseñada para ofrecer claridad visual y una experiencia profesional.

### Elementos destacados

* 🎯 Área Drag & Drop central
* 🖱️ Selección manual de archivos
* 🪟 Ventanas modales personalizadas
* 🧠 Mensajes claros y no ambiguos
* 🖥️ Soporte completo HiDPI (Windows 10 / 11)

La estética es **minimalista, funcional y orientada a productividad**.

---

## 📷 Capturas de pantalla

<p align="center">
  <img src="assets/images/screenshot.png" alt="Vista previa de la aplicación" width="600"/>
</p>

---

## ▶️ Ejecución

### Opción 1: Desde código fuente (desarrolladores)

Requisitos:

* 🐍 Python **3.11**
* Entorno virtual activo

```bash
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

---

### Opción 2: Instalador Windows (.exe) – recomendado

El proyecto se distribuye como **Instalador Windows firmado**, listo para instalar en el sistema.

#### Ventajas

* ✅ No requiere Python instalado
* ✅ Drag & Drop funcional tras la instalación
* ✅ Assets incluidos
* ✅ Instalación sencilla mediante asistente
* ✅ Ofrece **creación opcional** de acceso directo en el escritorio
* ✅ Listo para usar inmediatamente tras la instalación

⬇️ El instalador se publica en la sección **[Releases](https://github.com/Pablitus666/Image_Converter/releases)** del repositorio, dentro de un archivo ZIP que contiene:

* `Image_Converter_Setup.exe` – Instalador Windows firmado  
* `README.txt` – Instrucciones básicas de instalación

#### Instrucciones para el usuario final

1. Descargar el archivo ZIP desde la sección **Releases**.  
2. Extraer su contenido a una carpeta temporal.  
3. Ejecutar `Image_Converter_Setup.exe` y seguir las indicaciones del instalador.  
4. Durante la instalación, podrás decidir si deseas crear un acceso directo en el escritorio.
5. ¡Listo! La aplicación está instalada y lista para usar.

> ⚠️ Nota: Este **instalador no es portable**. Es necesario ejecutar el asistente de instalación para que la aplicación funcione correctamente y se cree el acceso directo de la Aplicación en el escritorio.

---

## 🛠️ Información de compilación

El ejecutable fue construido utilizando:

* 🐍 Python 3.11
* 📄 PyInstaller (one-file)
* 🪟 Windows SDK (signtool)
* 🔐 Firma digital con timestamp

---

## 📁 Estructura del proyecto

```
Image_Converter/
├─ app/
│  ├─ controller.py
│  ├─ dialogs.py
│  └─ main_window.py
│
├─ assets/
│  ├─ fonts/
│  └─ images/
│
├─ core/
│  ├─ image_converter.py
│  ├─ image_validator.py
│  ├─ image_processor.py
│  └─ logger.py
│
├─ locales/
│  ├─ es.json
│  └─ en.json
│
├─ main.py
├─ requirements.txt
├─ README.md
└─ RELEASE_DESCRIPTION.md
```

---

## 🛠️ Requisitos técnicos

* 🐍 Python **3.11**
* 🪟 Windows 10 / 11
* 🖥️ x64

---

## 📦 Dependencias principales

```txt
pillow
tkinterdnd2
```

---

## 🔐 Seguridad y confianza

El ejecutable distribuido está **firmado digitalmente**, lo que garantiza:

* ✔ Integridad
* ✔ Autenticidad
* ✔ Menos advertencias de SmartScreen
* ✔ Mayor confianza del usuario

---

## 📦 Portabilidad

* No modifica el registro
* No instala dependencias
* No crea carpetas del sistema
* Puede ejecutarse desde USB

---

## 👨‍💻 Autor

**Pablo Téllez**  
Desarrollador de Software  

📍 Tarija, Bolivia <img src="https://flagcdn.com/w20/bo.png" width="20"/> 
📧 [pharmakoz@gmail.com](mailto:pharmakoz@gmail.com) 

© 2026 — Image Converter

---

## ⭐ Estado del proyecto

✔ Estable
✔ En producción
✔ Uso profesional

---

## 📄 Licencia

Distribuido bajo licencia **MIT**.
