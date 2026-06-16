#!/bin/bash

echo "🚀 Ejecutando tests antes de hacer push..."
export PYTHONPATH=$PYTHONPATH:.

# Ejecutamos pytest con cobertura y generamos un reporte en consola al final
if pytest --cov=src --cov-report=term-missing tests/; then
    echo "✅ Todos los tests pasaron. Continuando con el push."
    exit 0
else
    echo "❌ Los tests fallaron. Abortando push."
    exit 1
fi
