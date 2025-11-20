#!/bin/bash
echo "DataPipe Framework - Instalacion Multi-Cloud"

# Verificar Docker
if ! docker version > /dev/null 2>&1; then
    echo "Error: Docker no esta ejecutandose. Por favor inicia Docker Desktop."
    exit 1
fi

# Configuracion interactiva
read -p "Ingresa tu cloud (gcp/aws/azure): " cloud
read -p "Ingresa nombre de la tabla: " table_name
read -p "Ingresa modo de carga (full/incremental): " load_mode

echo "Configurando para:"
echo "   Cloud: $cloud"
echo "   Tabla: $table_name" 
echo "   Modo: $load_mode"

# Crear estructura
make init-cloud CLOUD=$cloud TABLE_NAME=$table_name LOAD_MODE=$load_mode

# Construir generadores
echo "Construyendo generadores..."
make build-generators

# Probar generadores
echo "Probando generadores..."
make test-generators TABLE_NAME=$table_name

echo "Framework listo para $cloud"
echo "Estructura creada en: clouds/$cloud/"
echo "Proyecto creado en: projects/${cloud}_${table_name}/"
echo "Generadores construidos y probados"
echo ""
echo "Proximos pasos:"
echo "   1. Configurar conexion Oracle si es necesario"
echo "   2. Ejecutar generadores especificos"
echo "   3. Revisar archivos generados en projects/"
