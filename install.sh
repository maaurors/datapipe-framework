#!/bin/bash
echo "Instalando DataPipe Framework..."

# Verificar que Docker esté instalado
if ! command -v docker &> /dev/null; then
    echo "Error: Docker no está instalado. Instala Docker Desktop primero."
    exit 1
fi

# Verificar que Git esté instalado
if ! command -v git &> /dev/null; then
    echo "Error: Git no está instalado."
    exit 1
fi

# Instalar cookiecutter si no existe
if ! command -v cookiecutter &> /dev/null; then
    echo "Instalando cookiecutter..."
    pip3 install cookiecutter
fi

echo "✅ Prerrequisitos verificados"

# Construir las imágenes Docker
echo "Construyendo imágenes Docker..."
docker build -t datapipe/schema-generator:latest generators/schema-generator/
docker build -t datapipe/table-generator:latest generators/table-generator/
docker build -t datapipe/procedure-generator:latest generators/procedure-generator/
docker build -t datapipe/dag-generator:latest generators/dag-generator/

echo "✅ DataPipe Framework instalado correctamente"
echo ""
echo "Para crear un nuevo proyecto:"
echo "  make init"
echo ""
echo "Para ver todos los comandos:"
echo "  make help"
