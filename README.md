# Cloud Data Pipeline Framework


Framework profesional para migración de datos desde Oracle a múltiples clouds (GCP, AWS, Azure).

## Características

- Migración unificada a GCP, AWS y Azure
- Gestión de dependencias con Poetry
- Interfaz de línea de comandos simple
- Configuración por ambiente
- Extensible y modular
- Generación automática de schemas
- Testing local con docker-compose
- Portable
- Versionado con Docker image tags

## Quick Start

### Opción 1: Con Make (existente)
```bash
make build-generators
make init

### Modos de Ejecución:

```bash
# Modo local (testing)
poetry run migrate-table --cloud gcp --table clientes --env dev --execution-mode local

# Modo cloud (producción - serverless)
poetry run migrate-table --cloud gcp --table clientes --env prd --execution-mode cloud
