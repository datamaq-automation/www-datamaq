#!/bin/bash

echo "🚀 Ejecutando tests antes de hacer push..."
export PYTHONPATH=$PYTHONPATH:.
pytest --cov=src tests/
if [ $? -ne 0 ]; then
    echo "❌ Los tests fallaron. Abortando push."
    exit 1
fi
echo "✅ Todos los tests pasaron. Continuando con el push."
exit 0
