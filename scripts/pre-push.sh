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

if [ $status -eq 0 ]; then
    echo "✅ Todos los tests pasaron en ${duration}s. Continuando con el push."
    exit 0
else
    echo "❌ Los tests fallaron tras ${duration}s. Abortando push."
    exit 1
fi
