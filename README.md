# DataPipe Framework

Framework profesional para migración de datos desde Oracle a múltiples clouds (GCP, AWS, Azure) utilizando una arquitectura moderna basada en Docker, AVRO y Poetry.

## 🚀 Características

- **Multi-Cloud Nativo**: Soporte de primera clase para GCP (BigQuery), AWS (Redshift) y Azure (Synapse).
- **Arquitectura AVRO-First**: Todos los datos se extraen en formato AVRO con schema evolution y compresión Snappy.
- **Dockerizado**: Componentes aislados y portables (Extractor, Loader) con imágenes optimizadas (<200MB).
- **Gestión de Dependencias**: Uso de Poetry para builds reproducibles y seguros.
- **Generadores Automáticos**:
  - Schemas AVRO y JSON (BigQuery)
  - DAGs de Airflow
  - Scripts SQL
- **Configuración Centralizada**: Todo el proyecto se define en un simple `config.yaml`.

## 📋 Requisitos Previos

- Python 3.11+
- Docker
- Poetry (`curl -sSL https://install.python-poetry.org | python3 -`)

## ⚡ Quick Start

### 1. Instalación

```bash
git clone https://github.com/maaurors/datapipe-framework.git
cd datapipe-framework
poetry install
```

### 2. Crear un Nuevo Proyecto

```bash
# Inicializar proyecto para GCP
poetry run datapipe init migracion-ventas --cloud gcp
```

### 3. Configurar

Edita `migracion-ventas/config.yaml` con tus credenciales y tablas:

```yaml
project:
  name: "migracion-ventas"
  
source:
  connection:
    host: "${ORACLE_HOST}"
    service_name: "ORCL"

tables:
  - name: "VENTAS_2024"
    load_mode: "incremental"
```

### 4. Generar Artefactos

```bash
# Generar schemas AVRO
poetry run datapipe generate schema VENTAS_2024 --config migracion-ventas/config.yaml

# Generar DAG de Airflow
poetry run datapipe generate dag VENTAS_2024 --config migracion-ventas/config.yaml
```

### 5. Build y Deploy

```bash
# Construir imágenes Docker
make build

# Desplegar DAGs a tu entorno Airflow
cp dags/* $AIRFLOW_HOME/dags/
```

## 📚 Documentación

- [Guía de Inicio Rápido](docs/getting-started.md)
- [Configuración Multi-Cloud](docs/multi-cloud.md)
- [Schemas AVRO y Tipos de Datos](docs/avro-schemas.md)
- [Arquitectura Docker](docs/docker-architecture.md)

## 🏗 Estructura del Proyecto

```
datapipe-framework/
├── src/                # Código fuente del framework
├── docker/             # Dockerfiles (Base, Extractor, Loader)
├── templates/          # Templates Jinja2 (DAGs, Configs)
├── schemas/            # Schemas generados (AVRO/JSON)
├── dags/               # DAGs generados
└── pyproject.toml      # Dependencias y configuración
```
