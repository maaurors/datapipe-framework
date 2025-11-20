#!/bin/bash
echo "Configurando Cloud Migrator..."

if ! command -v poetry &> /dev/null; then
    echo "Instalando Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
    export PATH="$HOME/.local/bin:$PATH"
fi

echo "Instalando dependencias..."
poetry install

echo "Configuración completada"
echo ""
echo "Comandos disponibles:"
echo "  poetry run migrate-table --cloud gcp --table clientes"
echo "  poetry run migrate-table --cloud aws --table ventas"
