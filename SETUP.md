# Configuración para el equipo - Cloud Migrator

## Instalación en 3 pasos:

### 1. Clonar el proyecto:
```bash
git clone https://github.com/maaurors/datapipe-framework.git
cd datapipe-framework

#2. Instalar Poetry (si no está instalado):
curl -sSL https://install.python-poetry.org | python3 -
export PATH="$HOME/.local/bin:$PATH"

3. Instalar dependencias y usar:
poetry install
poetry run migrate-table --cloud gcp --table clientes

Comandos útiles:
# Migrar a diferentes clouds:
poetry run migrate-table --cloud aws --table ventas
poetry run migrate-table --cloud azure --table productos

# Entrar al entorno virtual:
poetry shell

export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc


#!/bin/bash
echo "Configurando Cloud Migrator..."

# Verificar si Poetry está instalado
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
