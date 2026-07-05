### 1.1 Technical requirements

> **Nota importante sobre versionado**
> Este curso utiliza **Rasa Open Source 2.x** como material de referencia. Rasa Technologies ha orientado el desarrollo activo hacia Rasa Pro y CALM, por lo que Rasa Open Source 3.x se encuentra en modo mantenimiento. Esto no invalida lo que aprenderás aquí: los conceptos de NLU, Core, stories, rules, slots, forms y custom actions siguen siendo los mismos, aunque la sintaxis haya evolucionado en versiones posteriores.

Para desarrollar asistentes virtuales con Rasa en tu entorno local o en servidores, es necesario cumplir con ciertos requisitos de software y hardware:

- **Sistema Operativo**: Linux (Ubuntu 20.04+ recomendado), macOS o Windows 10/11 (utilizando WSL2 preferentemente).
- **Python**: Rasa 2.x requiere versiones específicas de Python (habitualmente entre Python 3.7 y Python 3.8, según la versión menor). Se recomienda usar `pyenv` o `conda` para gestionar la versión exacta.
- **Entorno Virtual**: Es fundamental instalar Rasa dentro de un entorno virtual aislado (`venv` o `conda env`) para evitar conflictos de dependencias.
- **Herramientas de Compilación**: En sistemas Linux/macOS, podrías necesitar herramientas esenciales de compilación (`build-essential`, `g++`, etc.) para compilar componentes nativos de algunas librerías de Machine Learning.
- **Memoria RAM**: Se recomienda un mínimo de 8 GB de RAM (16 GB recomendado) ya que el entrenamiento de modelos de Deep Learning requiere recursos considerables.

#### Objetivos de aprendizaje
- Conocer los requisitos mínimos para instalar Rasa 2.x.
- Entender por qué es necesario un entorno virtual aislado.
- Reconocer la advertencia de versionado del curso.

#### Ejercicio práctico
1. Crea un entorno virtual con Python 3.8:
   ```bash
   python3.8 -m venv venv-rasa
   source venv-rasa/bin/activate
   ```
2. Instala Rasa 2.x:
   ```bash
   pip install -U pip
   pip install rasa==2.8.25
   ```
3. Verifica la versión instalada:
   ```bash
   rasa --version
   ```

#### Resumen
En esta lección revisamos los requisitos técnicos para trabajar con Rasa 2.x y destacamos que el curso usa esta versión como referencia pedagógica. En la próxima lección veremos qué papel juega el Machine Learning dentro de Rasa, sin salirnos del contexto del cotizador de instalaciones eléctricas.
