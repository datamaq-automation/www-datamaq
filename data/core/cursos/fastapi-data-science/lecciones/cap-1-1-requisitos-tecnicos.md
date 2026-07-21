### 1.1 Requisitos técnicos

Para seguir este curso necesitarás una computadora con sistema operativo Linux, macOS o Windows, acceso a una terminal de comandos y conexión a internet.

En este curso práctico aprenderás a construir, optimizar y desplegar APIs de Machine Learning y Ciencia de Datos listas para producción utilizando **FastAPI** y **Python**.

#### Requisitos de Software y Hardware

- **Sistema Operativo**:
  - **Linux**: Ubuntu 20.04+, Debian 11+, Fedora o cualquier distribución moderna. (Recomendado).
  - **macOS**: macOS 11 (Big Sur) o superior.
  - **Windows**: Windows 10 o 11 utilizando **WSL2** (Windows Subsystem for Linux con Ubuntu) para asegurar la compatibilidad con servidores de producción Linux.
- **Python**: Se requiere Python 3.10 o superior (se recomienda Python 3.12 para aprovechar las mejoras de rendimiento y la sintaxis actualizada de tipado).
- **Terminal de Comandos**: Bash o Zsh con utilidades básicas como `curl`, `git` y `tar`.
- **Editor de Código**: Visual Studio Code, PyCharm, Antigravity IDE o cualquier editor de tu preferencia con soporte para extensiones de Python y Pydantic.
- **Hardware Recomendado**: Al menos 8 GB de RAM (16 GB deseables para entrenar o cargar modelos pesados de Machine Learning en memoria).

#### Objetivos de Aprendizaje de la Sección A

1. Configurar un entorno de desarrollo profesional e aislado utilizando `pyenv` y `venv`.
2. Dominar las características fundamentales de Python moderno: **Type Hints**, **async/await** y estructuras de datos eficientes.
3. Crear tu primera API RESTful con endpoints GET, POST, PUT y DELETE usando decoradores de FastAPI.
4. Implementar schemas de datos robustos con **Pydantic V2** para validación automática y documentación OpenAPI (Swagger UI).
5. Aplicar el patrón de **Inyección de Dependencias** mediante `Depends` para modularizar la lógica de negocio y reutilizar servicios.

#### Verificación Inicial del Entorno

Abre tu terminal y ejecuta los siguientes comandos para verificar las herramientas instaladas:

```bash
# Verificar la versión de Git
git --version

# Verificar disponibilidad de cURL
curl --version

# Verificar versión por defecto de Python en el sistema
python3 --version
```

En las siguientes lecciones configuraremos la versión exacta de Python y aislaremos las dependencias necesarias para nuestro proyecto.
