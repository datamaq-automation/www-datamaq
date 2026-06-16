#!/bin/bash

# Inicio del cronómetro
start_time=$(date +%s)
echo "🚀 Ejecutando tests antes de hacer push... (Iniciado a las $(date +"%H:%M:%S"))"
export PYTHONPATH=$PYTHONPATH:.

# Ejecutamos pytest con cobertura y generamos un reporte en consola al final
pytest --cov=src --cov-report=term-missing tests/
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
