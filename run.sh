#!/bin/bash

# Detener proceso ocupando el puerto 8000
PORT=8000
PIDS=$(lsof -t -i:$PORT)
if [ ! -z "$PIDS" ]; then
  echo "Deteniendo procesos en puerto $PORT"
  kill -9 $PIDS
fi

VENV_DIR="venv"

if [ ! -d "$VENV_DIR" ]; then
  echo "Entorno virtual no encontrado. Creando $VENV_DIR..."
  python3 -m venv "$VENV_DIR"
  echo "Instalando dependencias desde requirements.txt..."
  "$VENV_DIR/bin/pip" install -r requirements.txt
fi

source "$VENV_DIR/bin/activate"

if ! python3 -c "import uvicorn" 2>/dev/null; then
  echo "Dependencias no encontradas. Instalando desde requirements.txt..."
  pip install -r requirements.txt
fi

export PYTHONPATH=$PYTHONPATH:$(pwd)
python3 -m uvicorn src.infrastructure.fastapi.app:app --reload
