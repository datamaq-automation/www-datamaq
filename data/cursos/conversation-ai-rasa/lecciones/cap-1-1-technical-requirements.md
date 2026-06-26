### 1.1 Requisitos técnicos para Rasa

Para poder desarrollar asistentes virtuales con Rasa en tu entorno local o en servidores, es necesario cumplir con ciertos requisitos de software y hardware:

- **Sistema Operativo**: Linux (Ubuntu 20.04+ recomendado), macOS o Windows 10/11 (utilizando WSL2 preferentemente).
- **Python**: Rasa requiere versiones específicas de Python (habitualmente entre Python 3.8 y Python 3.10, según la versión menor de Rasa). Se recomienda usar `pyenv` o `conda` para gestionar la versión exacta de Python.
- **Entorno Virtual**: Es fundamental instalar Rasa dentro de un entorno virtual aislado (`venv` o `conda env`) para evitar conflictos de dependencias con otras librerías de Python.
- **Herramientas de Compilación**: En sistemas Linux/macOS, podrías necesitar herramientas esenciales de compilación (`build-essential`, `g++`, etc.) para compilar componentes nativos que utilizan algunas librerías de Machine Learning (como TensorFlow).
- **Memoria RAM**: Se recomienda un mínimo de 8 GB de RAM (16 GB recomendado) ya que el entrenamiento de modelos de Deep Learning (como DIET o TED) requiere recursos considerables.
