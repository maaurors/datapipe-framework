#!/bin/bash
echo "🚀 DataPipe Framework - Instalación Multinube"

echo "1. Elige tu cloud:"
echo "   gcp  - Google Cloud Platform"
echo "   aws  - Amazon Web Services" 
echo "   azure - Microsoft Azure"

read -p "Ingresa tu cloud (gcp/aws/azure): " cloud

echo "📦 Configurando para: $cloud"
make init-cloud CLOUD=$cloud
make build-cloud CLOUD=$cloud

echo "✅ Framework listo para $cloud"
echo "📁 Proyecto creado en: clouds/$cloud/"
echo "🐳 Imagen construida: datapipe/loader-$cloud:latest"
