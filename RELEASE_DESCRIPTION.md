## 🚀 Image Converter – Release v1.1.0

Esta versión introduce **mejoras masivas de rendimiento, calidad de salida y experiencia de usuario**, consolidando a Image Converter como una herramienta de nivel profesional.

---

## ✨ Novedades destacadas v1.1.0

### 🚀 Rendimiento Extremo con Imágenes Gigantes

*   **UI No Bloqueante:** ¡Se acabó la espera! La carga de la vista previa de imágenes ahora se ejecuta en un **hilo secundario**. La interfaz permanece 100% receptiva, incluso con archivos de cientos de megapíxeles.
*   **Protección Anti-Crash Mejorada:** Se ha optimizado el manejo de imágenes de alta resolución para evitar por completo los errores de `DecompressionBomb`, permitiendo abrir archivos gigantes de forma segura.
*   **Procesamiento de Seguridad Acelerado:** El redimensionado preventivo ahora usa el algoritmo `BICUBIC`, que es hasta **4 veces más rápido** que `LANCZOS`, acelerando el tiempo de conversión de imágenes muy grandes sin una pérdida de calidad perceptible.

### ⚙️ Calidad de Salida Profesional

*   **Compresión Inteligente:** Se aplican configuraciones de compresión optimizadas y específicas para cada formato de salida:
    *   **JPEG:** Guardado progresivo con `quality=85` para máxima compatibilidad web y eficiencia.
    *   **PNG:** Nivel de compresión 9 (`compress_level=9`) para un tamaño de archivo mínimo sin perder calidad.
    *   **WEBP:** `method=6` para un ratio de compresión superior.
*   **Redimensionado Condicional:** La aplicación ahora es más inteligente y solo redimensiona cuando es necesario.
    *   **ICO:** Se redimensiona a un estándar de 256x256 para máxima compatibilidad, usando `LANCZOS` para preservar la calidad.
    *   **Otros formatos:** Mantienen su resolución original, evitando cualquier pérdida de calidad innecesaria.

### ✨ Instalador Mejorado

*   **Creación de Acceso Directo Opcional:** El instalador de Windows ahora es más profesional y permite al usuario decidir si desea crear un acceso directo en el escritorio.

---

## 🛡️ Correcciones v1.1.0

*   Se ha solucionado un bug que impedía que la interfaz de usuario se limpiara correctamente si ocurría un error durante la carga de una vista previa.

---
<br>

## 🚀 Image Converter – Release v1.0.0

Esta versión marca la **primera release estable, firmada y lista para producción** de **Image Converter**, una aplicación de escritorio profesional para la **conversión segura y validada de imágenes** en Windows.

El enfoque principal de esta release es:

* estabilidad
* experiencia de usuario
* validación estricta de archivos
* arquitectura modular mantenible
* distribución profesional y confiable

---

## ✨ Novedades destacadas

### 🧠 Validación avanzada de imágenes

* Verificación estricta de archivos de entrada.
* Solo se permiten imágenes válidas: **PNG, JPG, JPEG**.
* Prevención de errores comunes antes de iniciar cualquier procesamiento.

### 🖱️ Drag & Drop robusto y coherente

* Soporte estable para arrastrar imágenes directamente a la aplicación.
* Estados visuales claros y consistentes.
* Feedback inmediato ante archivos inválidos o no soportados.

### 🖼️ Conversión de imágenes segura y controlada

* Pipeline de procesamiento desacoplado.
* Manejo seguro de imágenes desde la carga hasta la salida.
* Resultados consistentes y compatibles con Windows.

### 📂 Acceso rápido a resultados

* Botón **“Abrir carpeta”** para acceder directamente a la ubicación del archivo generado.

### 🌍 Internacionalización (i18n)

* Sistema de traducciones basado en archivos JSON.
* Idioma por defecto: Español.
* Arquitectura preparada para ampliar idiomas sin modificar la lógica principal.

### 🖥️ Soporte HiDPI real

* Conciencia de DPI activada en Windows.
* Renderizado correcto en pantallas de alta resolución.
* Assets optimizados para escalado.

### 🧩 Arquitectura modular profesional

Separación clara entre:

* Interfaz gráfica (UI)
* Controlador de aplicación
* Validación de imágenes
* Procesamiento y conversión
* Utilidades y servicios

Esto garantiza un código mantenible, escalable y fácil de auditar.

### 🔐 Ejecutable firmado digitalmente

* El ejecutable (`.exe`) se distribuye **firmado con certificado digital**.
* Garantiza integridad y autenticidad del archivo.
* Reduce advertencias de Windows SmartScreen.
* Aumenta la confianza del usuario final.

### 📝 Logging interno

* Registro de eventos clave y errores.
* Facilita depuración, mantenimiento y evolución del proyecto.

---

## 🛡️ Correcciones y mejoras

* Manejo seguro de errores durante la carga y conversión.
* Prevención de estados inconsistentes en la interfaz.
* Restauración correcta del estado visual tras errores.

---

## 📦 Distribución

Esta versión se distribuye como:

* ✅ **Ejecutable (.exe) portable para Windows** (recomendado)

  * No requiere Python instalado
  * Entorno completamente embebido (PyInstaller one-file)
  * Mantiene Drag & Drop nativo
  * No modifica el sistema ni el registro

* 🧪 **Código fuente** para desarrolladores

---

## 🎯 Resultado

Con esta release, **Image Converter** se consolida como una aplicación:

* estable
* segura
* firmada digitalmente
* clara para el usuario final
* mantenible a nivel de código

Lista para uso real, distribución pública y futuras ampliaciones. 🚀
