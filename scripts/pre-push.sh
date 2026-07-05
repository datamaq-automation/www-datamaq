#!/bin/bash

# Inicio del cronómetro
start_time=$(date +%s)
echo "🚀 Validando compilación de CSS y tests antes de hacer push..."

# Compilar CSS
if command -v npm &> /dev/null; then
    echo "==> Compilando CSS consolidado con npm..."
    npm run build:css &> /dev/null
    
    # Verificar si index.css tiene cambios sin commitear
    if ! git diff --exit-code static/css/index.css &> /dev/null; then
        echo "❌ ERROR: El archivo static/css/index.css está desactualizado respecto a los fuentes."
        echo "👉 Corrí 'npm run build:css', agregá el archivo al commit ('git add static/css/index.css') y volvé a intentar."
        exit 1
    fi
    echo "✅ CSS validado y actualizado."
else
    echo "⚠️ Advertencia: npm no está instalado. No se pudo verificar la compilación de CSS."
fi
# Validar esquemas e integridad de YAMLs
echo "==> Auditando esquemas YAML de contenido..."
if [ -f "venv/bin/python" ]; then
    PYTHON="venv/bin/python"
else
    PYTHON="python3"
fi

$PYTHON scripts/validate_content.py
yaml_status=$?

if [ $yaml_status -ne 0 ]; then
    echo "❌ ERROR: Auditoría de esquemas YAML fallida. Corré 'venv/bin/python scripts/validate_content.py --fix' para reparar o revisar errores."
    exit 1
fi
echo "✅ Todos los esquemas YAML de contenido son válidos."

export PYTHONPATH=$PYTHONPATH:.

# Preferir pytest del entorno virtual si existe
if [ -f "venv/bin/pytest" ]; then
    PYTEST="venv/bin/pytest"
elif [ -f "./venv/bin/pytest" ]; then
    PYTEST="./venv/bin/pytest"
else
    PYTEST="pytest"
fi

# Ejecutamos pytest con cobertura, umbral del 85% y generamos un reporte en consola al final
$PYTEST --cov=src --cov-report=term-missing --cov-fail-under=85 tests/
status=$?

end_time=$(date +%s)
duration=$((end_time - start_time))

if [ $status -ne 0 ]; then
    echo "❌ Los tests fallaron tras ${duration}s. Abortando push."
    exit 1
fi

echo "✅ Todos los tests pasaron en ${duration}s."

# ---------------------------------------------------------------------------
# Auditoría responsive y de usabilidad táctil con Playwright
# ---------------------------------------------------------------------------
echo "==> Verificando auditoría responsive (Playwright)..."

# Verificar que playwright esté disponible
if ! $PYTHON -c "import playwright" 2>/dev/null; then
    echo "⚠️ Advertencia: Playwright no está instalado. Saltando auditoría responsive."
    echo "   Instalalo con: source venv/bin/activate && pip install -r requirements-dev.txt && playwright install chromium"
    echo "✅ Continuando con el push (sin auditoría responsive)."
    exit 0
fi

# Levantar el servidor de desarrollo temporalmente
SERVER_PID=""
PORT=8000
APP_MODULE="src.infrastructure.fastapi.app:app"

# Si hay algo en el puerto, lo liberamos (solo procesos del usuario actual)
if command -v lsof &> /dev/null; then
    PIDS=$(lsof -t -i:$PORT 2>/dev/null)
    if [ ! -z "$PIDS" ]; then
        echo "⚠️ Liberando puerto $PORT..."
        kill $PIDS 2>/dev/null || true
        sleep 1
    fi
fi

echo "==> Levantando servidor temporal en http://127.0.0.1:$PORT..."
PYTHONPATH=$PYTHONPATH:. $PYTHON -m uvicorn $APP_MODULE --host 127.0.0.1 --port $PORT --no-access-log &
SERVER_PID=$!

# Esperar a que el servidor esté saludable (máximo 30 segundos)
echo "==> Esperando que el servidor esté listo..."
server_ready=false
for i in $(seq 1 30); do
    if curl -s http://127.0.0.1:$PORT/health &> /dev/null || curl -s http://127.0.0.1:$PORT/ &> /dev/null; then
        server_ready=true
        break
    fi
    sleep 1
done

if [ "$server_ready" = false ]; then
    echo "❌ ERROR: El servidor no se levantó correctamente."
    if [ ! -z "$SERVER_PID" ]; then kill $SERVER_PID 2>/dev/null || true; fi
    exit 1
fi

# Ejecutar la auditoría responsive
$PYTHON scripts/audit_responsive.py --base-url http://127.0.0.1:$PORT
audit_status=$?

# Detener el servidor temporal
if [ ! -z "$SERVER_PID" ]; then
    kill $SERVER_PID 2>/dev/null || true
    wait $SERVER_PID 2>/dev/null || true
fi

end_time=$(date +%s)
duration=$((end_time - start_time))

if [ $audit_status -eq 0 ]; then
    echo "✅ Auditoría responsive superada en ${duration}s. Continuando con el push."
    exit 0
else
    echo "❌ La auditoría responsive falló tras ${duration}s. Abortando push."
    echo "👉 Corré manualmente 'source venv/bin/activate && python scripts/audit_responsive.py' para ver el detalle."
    exit 1
fi
